#!/usr/bin/env python3
"""Release pipeline for the next-trainer-pi-agent plugin (F2-1).

Modes
  check   - version-point consistency across the plugin source, vendoring
            sync gate green, compat.json counts match the tree, and whether
            the platform zips are up to date with the current sources.
  assets  - generate the release artifact set (remote-base catalog + trust +
            sha256 manifest + ready-to-run publish command) from BUILT platform
            zips. Never publishes: writing to a git host is done by a human in
            the formal workspace with the emitted command.

Both modes are safe to run anywhere (including this backup zone). Building the
zips themselves stays a separate explicit step (`--build` shells out to the
plugin's build-all-platforms.py from the project snapshot working tree).

Usage:
  python scripts/release.py check
  python scripts/release.py assets --remote-base https://github.com/OWNER/REPO/releases/download/v<ver> [--build]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = "next-trainer-pi-agent"
PLUGIN_SRC = REPO / "plugin" / PLUGIN
COMPAT = REPO / "compat.json"


def project_root(cli: str | None) -> Path:
    import os
    raw = cli or os.environ.get("NEXT_TRAINER_PROJECT_ROOT") or str(REPO.parent / "project")
    return Path(raw).resolve()


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def project_python(root: Path) -> str:
    """Project scripts import mikazuki (pydantic etc.) — must run in the project venv."""
    for cand in (root / ".venv-dev/Scripts/python.exe", root / ".venv-dev/bin/python",
                 root / ".venv/Scripts/python.exe", root / ".venv/bin/python"):
        if cand.is_file():
            return str(cand)
    return sys.executable


def version_points() -> dict[str, str | None]:
    pts: dict[str, str | None] = {}
    m = re.search(r'PLUGIN_VERSION = "([^"]+)"', read_text(PLUGIN_SRC / "launcher/src/main.ts"))
    pts["launcher PLUGIN_VERSION"] = m.group(1) if m else None
    try:
        pts["pi-package version"] = json.loads(read_text(PLUGIN_SRC / "pi-package/package.json"))["version"]
    except Exception:
        pts["pi-package version"] = None
    try:
        pts["source plugin.json"] = json.loads(read_text(PLUGIN_SRC / "plugin.json"))["version"]
    except Exception:
        pts["source plugin.json"] = None
    for script in ("build-pi-web-package.py", "build-marketplace-catalog.py"):
        m = re.search(r'^VERSION = "([^"]+)"', read_text(PLUGIN_SRC / "scripts" / script), re.M)
        pts[f"scripts/{script}"] = m.group(1) if m else None
    return pts


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path | None = None) -> int:
    print("+ " + " ".join(str(c) for c in cmd))
    return subprocess.call([str(c) for c in cmd], cwd=str(cwd) if cwd else None)


def compat_counts() -> tuple[list[str], list[str], list[str]]:
    kn = sorted(str(p.relative_to(REPO / "assets/knowledge")).replace("\\", "/")
                for p in (REPO / "assets/knowledge").rglob("*.md"))
    tp = sorted(p.name for p in (REPO / "assets/templates").glob("*.toml"))
    sk = sorted(p.parent.name for p in (REPO / "assets/skills").rglob("SKILL.md"))
    return kn, tp, sk


def mode_check(root: Path) -> int:
    rc = 0
    pts = version_points()
    for name, ver in pts.items():
        print(f"[version] {name}: {ver}")
    values = {v for v in pts.values() if v}
    if len(values) != 1 or None in pts.values():
        rc = 1
        print("[version] FAIL: version points inconsistent or missing", file=sys.stderr)

    if run([project_python(root), str(REPO / "scripts/sync-to-project.py"), "--check"], cwd=root) != 0:
        rc = 1
        print("[sync] FAIL: vendored snapshot drifts from agent-assets", file=sys.stderr)

    compat = json.loads(read_text(COMPAT)) if COMPAT.is_file() else {}
    kn, tp, sk = compat_counts()
    for label, actual, declared in (
        ("knowledgeDocs", len(kn), compat.get("knowledgeDocs")),
        ("templates", len(tp), compat.get("templates")),
        ("skills", len(sk), len(compat.get("skills") or [])),
    ):
        if declared is not None and declared != actual:
            rc = 1
            print(f"[compat] FAIL: {label} declared={declared} actual={actual}", file=sys.stderr)
        else:
            print(f"[compat] {label}: {actual}")

    zips = sorted((root / "plugin-packages" / PLUGIN / "dist-marketplace/packages").glob(f"{PLUGIN}-*.zip"))
    src_newest = max((p.stat().st_mtime for p in PLUGIN_SRC.rglob("*") if p.is_file()), default=0)
    if not zips:
        print("[zips] WARN: no platform zips found under the project snapshot dist-marketplace/packages")
    for z in zips:
        stale = z.stat().st_mtime < src_newest
        print(f"[zips] {z.name}  {z.stat().st_size/1e6:.1f} MB"
              + ("  [STALE: older than current sources — rebuild before publish]" if stale else ""))
    print("check:", "PASS" if rc == 0 else "FAIL")
    return rc


def mode_assets(root: Path, remote_base: str, build: bool) -> int:
    pts = version_points()
    values = {v for v in pts.values() if v}
    if len(values) != 1 or None in pts.values():
        print("[version] FAIL: fix version points before release assets", file=sys.stderr)
        return 1
    version = next(iter(values))

    if build:
        rc = run([project_python(root), root / "plugin-packages" / PLUGIN / "scripts/build-all-platforms.py"], cwd=root)
        if rc != 0:
            return rc

    snap_dist = root / "plugin-packages" / PLUGIN / "dist-marketplace"
    zips = sorted((snap_dist / "packages").glob(f"{PLUGIN}-{version}-*.zip"))
    if not zips:
        print(f"[zips] FAIL: no {PLUGIN}-{version}-*.zip built; run with --build first", file=sys.stderr)
        return 1
    if not remote_base.startswith("https://"):
        print("[remote-base] FAIL: must be a plain HTTPS URL", file=sys.stderr)
        return 1

    out = REPO / "dist-release" / f"v{version}"
    rc = run([project_python(root), snap_dist.parent / "scripts/build-marketplace-catalog.py",
              "--remote-base", remote_base.rstrip("/"), "--out-dir", out], cwd=root)
    if rc != 0:
        return rc
    for name in ("catalog.json", "trust.json"):
        if not (out / name).is_file():
            print(f"[catalog] FAIL: {name} missing in {out}", file=sys.stderr)
            return 1

    manifest = {
        "plugin": PLUGIN,
        "version": version,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "remoteBase": remote_base.rstrip("/"),
        "assets": [
            {"file": p.name, "size": p.stat().st_size, "sha256": sha256_file(p)}
            for p in sorted(list(out.glob("*.json")) + zips)
        ],
        "note": "publish is a human action in the formal workspace; see publish-command.txt",
    }
    (out / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (out / "publish-command.txt").write_text(
        "# run in the FORMAL workspace, from a directory that can stage the assets\n"
        "# 1) copy platform zips next to catalog.json/trust.json in a staging dir\n"
        "# 2) create the release:\n"
        f"gh release create v{version} \\\n"
        f"  {PLUGIN}-{version}-win32-x64.zip {PLUGIN}-{version}-linux-x64.zip \\\n"
        "  catalog.json trust.json \\\n"
        f'  --title "{PLUGIN} v{version}" --notes "<changelog>"\n',
        encoding="utf-8",
    )
    print(f"assets: {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=("check", "assets"))
    ap.add_argument("--project-root")
    ap.add_argument("--remote-base", default="", help="release asset URL base (assets mode)")
    ap.add_argument("--build", action="store_true", help="assets mode: run the dual-platform build first")
    args = ap.parse_args()
    root = project_root(args.project_root)
    if args.mode == "check":
        return mode_check(root)
    if not args.remote_base:
        ap.error("assets mode requires --remote-base https://...")
    return mode_assets(root, args.remote_base, args.build)


if __name__ == "__main__":
    raise SystemExit(main())

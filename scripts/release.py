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
  business-data - package the managed content release (knowledge/templates/
            skills -> trainer-assets-<assetsVersion>.zip + signed
            assets-index.json, F3-3 channel). Decoupled from plugin versions.

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
import hmac
import io
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = "next-trainer-pi-agent"
PLUGIN_SRC = REPO / "plugin" / PLUGIN
COMPAT = REPO / "compat.json"

# The managed-assets channel signs with the SAME dev HMAC key as the marketplace
# catalog (see plugin/.../scripts/build-marketplace-catalog.py and the host's
# trust.canonical_assets_index_payload). Kept in sync deliberately; the matching
# trust.json ships inside the release bundle only.
PUBLISHER = "next-trainer-project"
_DEV_KEY_ID = "dev-local-signing"
_DEV_KEY_HEX = "6e6578742d747261696e65722d6c6f63616c2d746573742d7369676e696e672d6b6579"


def _resolve_signing() -> tuple[str, str]:
    """Release signing key: env pair > key file > dev default.

    The key file is a JSON {"keyId": str, "keyHex": str} that must live
    OUTSIDE every git repository (workspace .release-signing/signing-key.json
    by convention, pointed to by MIKAZUKI_RELEASE_SIGNING_FILE). Rotation
    policy: never re-sign published artifacts; cut a NEW release with the new
    key and ship the dual-key trust.json so operators pinned on the old key
    can migrate, then revoke the old key id in a later trust.json.
    """
    import os
    key_id = os.environ.get("MIKAZUKI_RELEASE_SIGNING_KEY_ID", "").strip()
    key_hex = os.environ.get("MIKAZUKI_RELEASE_SIGNING_KEY_HEX", "").strip().casefold()
    if not (key_id or key_hex):
        key_file = os.environ.get("MIKAZUKI_RELEASE_SIGNING_FILE", "").strip()
        if key_file:
            payload = json.loads(Path(key_file).read_text(encoding="utf-8"))
            key_id, key_hex = str(payload["keyId"]), str(payload["keyHex"]).casefold()
    if key_id or key_hex:
        if not (key_id and re.fullmatch(r"[0-9a-f]{64,}", key_hex)):
            raise SystemExit(
                "release signing requires key id + >=32-byte hex key "
                "(MIKAZUKI_RELEASE_SIGNING_KEY_ID/_HEX or MIKAZUKI_RELEASE_SIGNING_FILE)"
            )
        if key_id != _DEV_KEY_ID:
            print(f"[signing] release key: {key_id}")
        return key_id, key_hex
    return _DEV_KEY_ID, _DEV_KEY_HEX


SIGNING_KEY_ID, SIGNING_KEY_HEX = _resolve_signing()
_ASSETS_SIGNED_FIELDS = (
    "schemaVersion", "assetsVersion", "file", "url", "size", "sha256",
    "generatedAt", "publisherId", "signingKeyId",
)


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

    compat = json.loads(read_text(COMPAT)) if COMPAT.is_file() else {}
    compat_pin = (compat.get("plugin") or {}).get("version")
    if compat_pin and values and compat_pin not in values:
        rc = 1
        print(f"[version] FAIL: compat.json pins plugin {compat_pin}, sources say {sorted(values)}", file=sys.stderr)
    else:
        print(f"[version] compat.json plugin: {compat_pin}")

    if run([project_python(root), str(REPO / "scripts/sync-to-project.py"), "--check"], cwd=root) != 0:
        rc = 1
        print("[sync] FAIL: vendored snapshot drifts from agent-assets", file=sys.stderr)

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
    cmd = [project_python(root), snap_dist.parent / "scripts/build-marketplace-catalog.py",
           "--remote-base", remote_base.rstrip("/"), "--out-dir", out]
    # Rotation support: forward the dual-key transition trust extra file
    # (same {keys:{id:{publisherId,keyHex}}} shape) so the emitted trust.json
    # lets hosts pinned on the previous key keep verifying the new release.
    import os
    extra_keys_file = os.environ.get("MIKAZUKI_TRUST_EXTRA_KEYS_FILE", "").strip()
    if extra_keys_file:
        cmd += ["--trust-extra-keys-file", extra_keys_file]
    rc = run(cmd, cwd=root)
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


def mode_business_data(root: Path, remote_base: str) -> int:
    """Package the managed business-data release (F3-3 channel).

    Emits trainer-assets-<assetsVersion>.zip (knowledge/ + templates/ +
    skills/ trees with an embedded MANIFEST.json) plus a signed
    assets-index.json whose canonical envelope byte-matches the host's
    trust.canonical_assets_index_payload. Content releases are decoupled from
    plugin versions: bump compat.json assetsVersion and publish a new
    assets-<version> tag; installed clients pull it without a plugin upgrade.
    """
    compat = json.loads(read_text(COMPAT)) if COMPAT.is_file() else {}
    assets_version = str(compat.get("assetsVersion") or "")
    if not re.fullmatch(r"[0-9A-Za-z._-]{1,64}", assets_version):
        print("[assetsVersion] FAIL: compat.json carries no usable assetsVersion", file=sys.stderr)
        return 1
    if not remote_base.startswith("https://"):
        print("[remote-base] FAIL: must be a plain HTTPS URL", file=sys.stderr)
        return 1

    files: dict[str, Path] = {}
    for namespace in ("knowledge", "templates", "skills"):
        base = REPO / "assets" / namespace
        if not base.is_dir():
            continue
        for member in sorted(base.rglob("*")):
            if member.is_file():
                rel = namespace + "/" + str(member.relative_to(base)).replace("\\", "/")
                files[rel] = member
    if not files:
        print("[tree] FAIL: no business-data files found under assets/", file=sys.stderr)
        return 1

    out = REPO / "dist-release" / f"assets-{assets_version}"
    out.mkdir(parents=True, exist_ok=True)
    zip_name = f"trainer-assets-{assets_version}.zip"
    zip_path = out / zip_name
    entries = [
        {"path": rel, "sha256": sha256_file(path), "size": path.stat().st_size}
        for rel, path in sorted(files.items())
    ]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr("MANIFEST.json", json.dumps({"assetsVersion": assets_version, "files": entries}, indent=1, sort_keys=True))
        for rel, path in sorted(files.items()):
            archive.write(path, rel)

    index = {
        "schemaVersion": 1,
        "assetsVersion": assets_version,
        "file": zip_name,
        "url": remote_base.rstrip("/") + "/" + zip_name,
        "size": zip_path.stat().st_size,
        "sha256": sha256_file(zip_path),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publisherId": PUBLISHER,
        "signingKeyId": SIGNING_KEY_ID,
    }
    body = {key: index.get(key) for key in _ASSETS_SIGNED_FIELDS}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    index["signature"] = hmac.new(bytes.fromhex(SIGNING_KEY_HEX), canonical, hashlib.sha256).hexdigest()
    index_path = out / "assets-index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"[package] {zip_path.name}: {len(files)} files, {zip_path.stat().st_size} bytes")
    print(f"[index]   {index_path.name} (assetsVersion {assets_version})")

    # Byte-exactness proof against the host verifier itself, when importable.
    trust_file = root / "plugin-packages" / PLUGIN / "dist-marketplace" / "trust.json"
    # Self-check must verify against a trust root holding the ACTIVE key (and,
    # during a rotation, the predecessor too), not the vendored dev-only file.
    trust_keys = {SIGNING_KEY_ID: {"publisherId": PUBLISHER, "keyHex": SIGNING_KEY_HEX}}
    if SIGNING_KEY_ID != _DEV_KEY_ID:
        trust_keys[_DEV_KEY_ID] = {"publisherId": PUBLISHER, "keyHex": _DEV_KEY_HEX}
    probe_trust = out / "trust-transition.json" if SIGNING_KEY_ID != _DEV_KEY_ID else trust_file
    if SIGNING_KEY_ID != _DEV_KEY_ID:
        probe_trust.write_text(
            json.dumps(
                {
                    "keys": trust_keys,
                    "revokedKeys": [],
                    "note": "Key rotation transition trust root: active release key + predecessor dev key; revoke the old id after operators migrate.",
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
    if trust_file.is_file():
        probe = (
            "import json, sys\n"
            "from pathlib import Path\n"
            "from mikazuki.plugin_marketplace.trust import load_trust_root\n"
            "index = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))\n"
            "load_trust_root(Path(sys.argv[2])).verify_assets_index(index)\n"
            "print('[self-check] host verify_assets_index: OK')\n"
        )
        result = subprocess.run(
            [project_python(root), "-c", probe, str(index_path), str(probe_trust)],
            capture_output=True, text=True, cwd=str(root),
        )
        if result.returncode != 0:
            print("[self-check] FAIL: host rejected the signed index\n" + result.stdout + result.stderr, file=sys.stderr)
            return 1
        print(result.stdout.strip())
    else:
        print("[self-check] WARN: no dist-marketplace/trust.json to verify against; skipped")

    (out / "publish-command.txt").write_text(
        "# business-data channel release (immutable tag per assetsVersion)\n"
        f"gh release create assets-{assets_version} \\\n"
        f"  {zip_name} assets-index.json \\\n"
        f'  --title "trainer assets {assets_version}" --notes "<content changelog>"\n'
        "# client side: NEXT_TRAINER_ASSETS_INDEX_URL=<this release>/assets-index.json\n",
        encoding="utf-8",
    )
    print(f"business-data: {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=("check", "assets", "business-data"))
    ap.add_argument("--project-root")
    ap.add_argument("--remote-base", default="", help="release asset URL base (assets / business-data mode)")
    ap.add_argument("--build", action="store_true", help="assets mode: run the dual-platform build first")
    args = ap.parse_args()
    root = project_root(args.project_root)
    if args.mode == "check":
        return mode_check(root)
    if not args.remote_base:
        ap.error(f"{args.mode} mode requires --remote-base https://...")
    if args.mode == "business-data":
        return mode_business_data(root, args.remote_base)
    return mode_assets(root, args.remote_base, args.build)


if __name__ == "__main__":
    raise SystemExit(main())

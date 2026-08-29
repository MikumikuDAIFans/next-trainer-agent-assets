#!/usr/bin/env python3
"""One-way vendoring sync: agent-assets -> main project plugin snapshot.

Maps (content is owned by this repo; the snapshot is generated, never edited):

    plugin/next-trainer-pi-agent/**        -> <project>/plugin-packages/next-trainer-pi-agent/**
    assets/knowledge/**                    -> .../next-trainer-pi-agent/seeds/knowledge/**
    assets/templates/**                    -> .../next-trainer-pi-agent/seeds/templates/**
    assets/skills/**                       -> .../next-trainer-pi-agent/seeds/skills/**

After a write run the snapshot gets a ``VENDORED-FROM.json`` provenance file
(source repo, commit, dirty flag, UTC timestamp). ``--check`` reports drift
(missing / changed / stray files) without writing and exits 1 — use it as the
vendoring gate in CI or before any project commit touching the plugin tree.

Build artifacts inside the snapshot (node_modules, .next, dist, runtime, bin,
dist-marketplace, ...) are never copied, compared, or pruned.

Usage:
    python scripts/sync-to-project.py [--project-root PATH] [--check] [--verbose]

Env NEXT_TRAINER_PROJECT_ROOT overrides --project-root (lowest priority:
default sibling ``../project`` of this repo).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "next-trainer-pi-agent"
SNAPSHOT_REL = Path("plugin-packages") / PLUGIN_NAME
PROVENANCE_NAME = "VENDORED-FROM.json"

# (source dir under this repo, target subdir under the snapshot)
CONTENT_MAPS = [
    (Path("plugin") / PLUGIN_NAME, Path(".")),
    (Path("assets") / "knowledge", Path("seeds") / "knowledge"),
    (Path("assets") / "templates", Path("seeds") / "templates"),
    # Skills ride the SAME managed-content channel as knowledge/templates
    # (F3-0 decision 1): seeded into the data root, then copied by the
    # launcher to <dataRoot>/pi-agent/skills (the pi SDK user-scope discovery
    # dir). They must NOT live under pi-package/ — the SDK would then load
    # BOTH a package copy and the managed copy.
    (Path("assets") / "skills", Path("seeds") / "skills"),
]

# Name-based artifact/junk segments, excluded at any depth.
EXCLUDED_SEGMENTS = {
    ".git", ".next", ".bun-cache", ".pytest_cache", ".runtime", ".turbo",
    "__pycache__", "dist", "dist-marketplace", "node_modules",
}
# Locally generated files inside otherwise-synced source dirs (git-ignored in
# both repos; never vendored).
EXCLUDED_FILE_SUFFIXES = (".tsbuildinfo",)
EXCLUDED_FILE_NAMES = {"next-env.d.ts"}
# Build-provisioned roots, excluded only at the top of each mapped tree
# (pi-web/bin/*.js is real tracked source and must be synced).
ROOT_EXCLUDED_SEGMENTS = {"bin", "runtime"}


def _excluded_file(name: str) -> bool:
    return name in EXCLUDED_FILE_NAMES or name.endswith(EXCLUDED_FILE_SUFFIXES)


def walk_pruned(root: Path):
    """Yield (rel_posix, file_path) under root, pruning excluded dirs before descent."""
    stack: list[tuple[Path, tuple[str, ...]]] = [(root, ())]
    while stack:
        cur, prefix = stack.pop()
        try:
            entries = sorted(cur.iterdir(), key=lambda p: p.name)
        except OSError:
            continue
        for entry in entries:
            rel = prefix + (entry.name,)
            if any(part in EXCLUDED_SEGMENTS for part in rel) or (len(rel) == 1 and rel[0] in ROOT_EXCLUDED_SEGMENTS):
                continue
            if entry.is_dir():
                stack.append((entry, rel))
            elif entry.is_file() and not _excluded_file(entry.name):
                yield "/".join(rel), entry


def expected_map() -> dict[str, Path]:
    files: dict[str, Path] = {}
    for src_dir, target_dir in CONTENT_MAPS:
        src_root = REPO_ROOT / src_dir
        if not src_root.is_dir():
            continue
        for rel_posix, path in walk_pruned(src_root):
            files[(target_dir / rel_posix).as_posix()] = path
    return files


def snapshot_files(snapshot: Path) -> set[str]:
    if not snapshot.is_dir():
        return set()
    return {rel for rel, _ in walk_pruned(snapshot) if rel != PROVENANCE_NAME}


def repo_state() -> tuple[str, bool]:
    def run(*args: str) -> str:
        return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                              capture_output=True, text=True).stdout.strip()
    return run("rev-parse", "HEAD"), bool(run("status", "--porcelain"))


def resolve_project_root(cli: str | None) -> Path:
    root = cli or os.environ.get("NEXT_TRAINER_PROJECT_ROOT", "") or str(REPO_ROOT.parent / "project")
    return Path(root).resolve()


def _content_equal(src: Path, dst: Path) -> bool:
    """Content equality ignoring line-ending style.

    The project tracks the snapshot with git's default text handling, so a
    checkout can materialise files with CRLF while agent-assets stores LF.
    That is autocrlf noise, not drift; compare on CRLF-normalised bytes so the
    gate flags real content changes only. Writes still copy source bytes
    verbatim; this only relaxes the comparison, matching git's text semantics.
    """
    def norm(data: bytes) -> bytes:
        return data.replace(b"\r\n", b"\n")
    try:
        return norm(src.read_bytes()) == norm(dst.read_bytes())
    except OSError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-root")
    parser.add_argument("--check", action="store_true", help="report drift only, exit 1 on drift")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    snapshot = project_root / SNAPSHOT_REL
    if not project_root.is_dir() or not (project_root / "mikazuki").is_dir():
        print(f"error: {project_root} does not look like the Next Trainer project root", file=sys.stderr)
        return 2

    expected = expected_map()
    actual = snapshot_files(snapshot)
    missing = sorted(set(expected) - actual)
    stray = sorted(actual - set(expected))
    changed = []
    for rel, src in sorted(expected.items()):
        dst = snapshot / rel
        if rel in actual and not _content_equal(src, dst):
            changed.append(rel)

    drift = missing or changed or stray
    if args.check:
        for group, items in (("missing", missing), ("changed", changed), ("stray", stray)):
            for rel in items:
                print(f"[{group}] {SNAPSHOT_REL / rel}")
        if drift:
            print(f"vendoring drift: {len(missing)} missing, {len(changed)} changed, {len(stray)} stray", file=sys.stderr)
            return 1
        print("vendored snapshot is in sync")
        return 0

    written = 0
    # Byte-EXACT for writes: a line-ending change IS a content change for the
    # shipped tree (a CRLF-corrupted WSL script once passed the normalized
    # comparison and survived two syncs until it exploded the linux build).
    # The normalized comparison above only relaxes the --check gate against
    # git autocrlf noise in the working copy.
    changed_bytes = [
        rel
        for rel, src in sorted(expected.items())
        if (snapshot / rel).is_file() and src.read_bytes() != (snapshot / rel).read_bytes()
    ]
    for rel in missing + changed_bytes:
        src, dst = expected[rel], snapshot / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        written += 1
        if args.verbose:
            print(f"[copy] {rel}")
    removed = 0
    for rel in stray:
        (snapshot / rel).unlink()
        removed += 1
        if args.verbose:
            print(f"[prune] {rel}")

    commit, dirty = repo_state()
    provenance = {
        "source": "agent-assets",
        "repoPath": str(REPO_ROOT),
        "commit": commit,
        "dirty": dirty,
        "syncedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": "scripts/sync-to-project.py",
        "files": len(expected),
    }
    (snapshot / PROVENANCE_NAME).write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    print(f"sync done: {written} written, {removed} pruned, snapshot={snapshot}")
    print(f"provenance: agent-assets @ {commit[:12]}{'' if not dirty else ' (dirty)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

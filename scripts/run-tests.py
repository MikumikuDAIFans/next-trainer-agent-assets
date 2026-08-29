#!/usr/bin/env python3
"""Run agent-assets' own test suite with the project host toolchain.

The plugin manifest pins validate against the host's PluginManifest model
(host contract per compat.json hostCompatibility), so the runner uses the
project venv's python+pytest when available, with PYTHONPATH set to the
project root. Override the host location with NEXT_TRAINER_PROJECT_ROOT.

Usage: python scripts/run-tests.py [pytest args...]
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def project_root() -> Path:
    raw = os.environ.get("NEXT_TRAINER_PROJECT_ROOT", "").strip() or str(REPO.parent / "project")
    return Path(raw).resolve()


def project_python(root: Path) -> str:
    for cand in (root / ".venv-dev/Scripts/python.exe", root / ".venv-dev/bin/python",
                 root / ".venv/Scripts/python.exe", root / ".venv/bin/python"):
        if cand.is_file():
            return str(cand)
    return sys.executable


def main() -> int:
    root = project_root()
    if not (root / "mikazuki").is_dir():
        print(f"project host not found at {root}; set NEXT_TRAINER_PROJECT_ROOT", file=sys.stderr)
        return 2
    py = project_python(root)
    env = dict(os.environ, NEXT_TRAINER_PROJECT_ROOT=str(root), PYTHONPATH=str(root))
    args = [py, "-m", "pytest", str(REPO / "tests"), *sys.argv[1:]]
    print("+ " + " ".join(args))
    return subprocess.call(args, cwd=str(REPO), env=env)


if __name__ == "__main__":
    raise SystemExit(main())

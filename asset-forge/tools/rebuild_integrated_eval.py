"""Populate the integrated assets/eval mirror from reviewed eval rows."""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
source = root / "data" / "eval-drafts" / "eval-candidates" / "knowledge-citation-migration-rows.jsonl"
dest = root / "assets" / "eval" / "knowledge-citation-seeds.jsonl"
if not source.exists():
    raise SystemExit(f"source missing: {source}")
if dest.exists():
    raise SystemExit(f"refusing to overwrite existing destination: {dest}")
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes(source.read_bytes())
print(f"created {dest} rows={sum(1 for line in dest.read_text(encoding='utf-8').splitlines() if line.strip())}")

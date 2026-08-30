"""Compare integrated template bytes with the frozen pre-accident manifest."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
frozen = root / "governance" / "migration-preview-20260830" / "migration-manifest.json"
templates = root / "assets" / "templates"
out = root / "governance" / "evidence" / "stage-4" / "recovery-hash-ledger.json"
manifest = json.loads(frozen.read_text(encoding="utf-8"))
old = {}
for op in manifest.get("operations", []):
    if op.get("kind") in {"template", "template-evidence"}:
        old[Path(op["source"].replace("\\", "/")).name] = op["sha256"]
rows = []
for name, old_hash in sorted(old.items()):
    path = templates / name
    if not path.exists():
        status, new_hash = "missing", None
    else:
        new_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        text = path.read_text(encoding="utf-8", errors="replace")
        status = "byte-exact-recovered" if new_hash == old_hash else ("reconstructed" if ("reconstructed-2026-08-30" in text or "2026-08-30-reconstructed" in text) else "present-nonmatching-unclassified")
    rows.append({"file": name, "oldFrozenSha256": old_hash, "currentSha256": new_hash, "status": status})
summary = {"files": len(rows), "byteExactRecovered": sum(r["status"] == "byte-exact-recovered" for r in rows), "reconstructed": sum(r["status"] == "reconstructed" for r in rows), "missing": sum(r["status"] == "missing" for r in rows), "rows": rows}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
print(json.dumps({k: summary[k] for k in ("files", "byteExactRecovered", "reconstructed", "missing")}, ensure_ascii=False))

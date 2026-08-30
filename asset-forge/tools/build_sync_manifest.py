"""Build a describe-only manifest for future one-way synchronization.

No copy, overwrite, delete, commit, or push is performed. Targets are checked
against the formal asset repository and every operation is create/append only.
"""
from __future__ import annotations
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
FORMAL = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
OUT = ROOT / "sync" / "sync-manifest.json"
PREFIXES = ("assets/knowledge/", "assets/templates/", "assets/eval/")

def sha(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main() -> int:
    if FORMAL is None:
        raise SystemExit("usage: build_sync_manifest.py <AgentAssetsRoot> <formal-agent-assets-root>")
    ops, problems = [], []
    for kind, base, target_base in (("knowledge", ROOT/"assets/knowledge", "assets/knowledge"), ("template", ROOT/"assets/templates", "assets/templates")):
        if not base.exists():
            continue
        for src in sorted(base.rglob("*")):
            if not src.is_file(): continue
            rel = src.relative_to(base).as_posix()
            target = f"{target_base}/{rel}"
            if not target.startswith(PREFIXES): problems.append(f"target outside whitelist: {target}")
            if (FORMAL / target).exists(): problems.append(f"target already exists: {target}")
            ops.append({"op":"create","source":src.relative_to(ROOT).as_posix(),"target":target,"sha256":sha(src),"size":src.stat().st_size,"kind":kind})
    eval_file = ROOT / "assets/eval/knowledge-citation-seeds.jsonl"
    if eval_file.exists():
        lines = [x for x in eval_file.read_text(encoding="utf-8").splitlines() if x.strip()]
        target = "assets/eval/knowledge-citation-seeds.jsonl"
        existing = set()
        formal_eval = FORMAL / target
        if formal_eval.exists():
            for line in formal_eval.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try: existing.add(json.loads(line).get("id"))
                    except json.JSONDecodeError: problems.append(f"invalid formal eval row: {target}")
        new_lines = []
        for line in lines:
            try:
                if json.loads(line).get("id") not in existing: new_lines.append(line)
            except json.JSONDecodeError: problems.append(f"invalid staging eval row: {target}")
        if new_lines:
            ops.append({"op":"append","source":eval_file.relative_to(ROOT).as_posix(),"target":target,"rows":len(new_lines),"sha256":sha(eval_file),"kind":"eval","rowIds":[json.loads(x).get("id") for x in new_lines]})
    manifest = {"schemaVersion":1,"generatedAt":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"sourceRoot":str(ROOT),"targetRepo":str(FORMAL),"execution":"NONE — describe-only; no sync/copy/overwrite/delete/commit/push","whitelist":list(PREFIXES),"operations":ops,"problems":problems}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n")
    print(json.dumps({"ops":len(ops),"problems":problems,"result":"pass" if not problems else "fail"},ensure_ascii=False))
    return 1 if problems else 0
if __name__ == "__main__": raise SystemExit(main())

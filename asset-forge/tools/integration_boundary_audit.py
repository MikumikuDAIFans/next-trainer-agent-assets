"""Audit the integrated staging tree for unsafe paths and forbidden actions."""
from __future__ import annotations
import json, re, sys, subprocess
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve()
FORMAL=[Path(x).resolve() for x in sys.argv[2:]]
BAD_DRIVE=re.compile(r"(?i)(?:Path\(\s*r?['\"]|['\"])[A-Z]:[\\/]")
SECRET=re.compile(r"(?i)(api[_-]?key\s*[:=]|token\s*[:=]\s*[A-Za-z0-9]|cookie\s*[:=]|password\s*[:=])")
def main()->int:
    failures=[]; scanned=0
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(str(p).startswith(str(f)) for f in FORMAL): continue
        scanned += 1
        if p.suffix.lower() in {".json",".jsonl",".toml",".py"}:
            try: text=p.read_text(encoding="utf-8")
            except UnicodeDecodeError: continue
            if p.suffix.lower() == ".py" and BAD_DRIVE.search(text):
                failures.append(f"absolute drive path: {p.relative_to(ROOT)}")
            if SECRET.search(text) and p.suffix.lower() not in {".py"}:
                failures.append(f"credential-looking text: {p.relative_to(ROOT)}")
    for formal in FORMAL:
        if formal.exists() and (formal / ".git").exists():
            result = subprocess.run(["git", "-C", str(formal), "status", "--porcelain"], capture_output=True, text=True)
            if result.stdout.strip(): failures.append(f"formal repository dirty: {formal}")
    report={"scanned":scanned,"failures":failures,"result":"pass" if not failures else "fail","formalReposChecked":[str(x) for x in FORMAL]}
    out=ROOT/"governance/evidence/integration-boundary-audit.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n")
    print(json.dumps({"scanned":scanned,"failures":failures,"result":report["result"]},ensure_ascii=False)); return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())

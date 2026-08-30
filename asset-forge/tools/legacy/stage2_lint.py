"""Stage 2 candidate knowledge lint.

Checks (per governance "知识候选验证"):
  U1 file is declared in knowledge-manifest.jsonl
  U2 UTF-8 without BOM; first line is a '# ' title
  U3 header trio present in first 12 lines: - Version: / - Scope: / - Evidence status:
  U4 an "- Aliases" search-keyword line exists
  U5 "## Sources" section exists and contains at least one evidence entry
  U6 "## Boundaries" section exists
  C1 every markdown relative link resolves to an on-disk file inside the candidate root
     (external links must carry an explicit scheme)
  S1 no machine drive paths (X:/ placeholders are allowed), no user-profile paths
  S2 no credential-looking strings (api key/token/cookie/password patterns)
Exit 0 only when all scanned files pass.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HEADER_KEYS = ("- Version:", "- Scope:", "- Evidence status:")
BAD_PATH = re.compile(r"(?i)\b(?![Xx]:)[A-Z]:[\\/]")
# Require a non-letter boundary before "users/" so URLs such as
# "diffusers/en" are not mistaken for a local user-profile path.
PROFILE_PATH = re.compile(r"(?i)(?<![A-Za-z])users[\\/][^\\/]+|[\\/]home[\\/][^\\/]+")
CRED = re.compile(r"(?i)(api[_-]?key[ \t]*[:=]|token[ \t]*[:=][ \t]*[A-Za-z0-9]|cookie[ \t]*[:=]|password[ \t]*[:=])")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")


def lint_file(md: Path, root: Path, manifest_ids: set[str]) -> list[str]:
    problems: list[str] = []
    raw = md.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("U2: file has UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"U2: not valid UTF-8: {exc}"]
    rel = md.relative_to(root).as_posix()
    if rel not in manifest_ids:
        problems.append("U1: not declared in knowledge-manifest.jsonl")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        problems.append("U2: first line is not a '# ' title")
    head = "\n".join(lines[:12])
    for key in HEADER_KEYS:
        if key not in head:
            problems.append(f"U3: missing header line '{key}'")
    if "- Aliases" not in text:
        problems.append("U4: missing '- Aliases' search-keyword line")
    if "## Sources" not in text:
        problems.append("U5: missing '## Sources' section")
    else:
        sources = text.split("## Sources", 1)[1].split("\n## ", 1)[0]
        if not re.search(r"(?m)^\s*[-*\d].+", sources.strip()):
            problems.append("U5: '## Sources' section is empty")
    if "## Boundaries" not in text:
        problems.append("U6: missing '## Boundaries' section")
    base = md.parent
    for target in LINK.findall(text):
        if "://" in target:
            continue
        resolved = (base / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            problems.append(f"C1: relative link escapes candidate root: {target}")
            continue
        if not resolved.exists():
            problems.append(f"C1: broken internal link: {target}")
    if BAD_PATH.search(text):
        problems.append("S1: machine drive path found (use X:/ placeholders)")
    if PROFILE_PATH.search(text):
        problems.append("S1: user profile path found")
    if CRED.search(text):
        problems.append("S2: credential-looking string found")
    return problems


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    cand_root = root / "04_知识库候选"
    manifest_path = cand_root / "knowledge-manifest.jsonl"
    if not manifest_path.exists():
        print("manifest missing; run tools/stage2_build_coverage_matrix.py first")
        return 2
    manifest = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    manifest_ids = {rec["doc_id"] for rec in manifest}
    failing = 0
    scanned = 0
    for md in sorted(cand_root.rglob("*.md")):
        if md.name == "README.md":
            continue
        scanned += 1
        problems = lint_file(md, cand_root, manifest_ids)
        status = "ok" if not problems else "FAIL"
        print(f"[{status}] {md.relative_to(cand_root).as_posix()}")
        for p in problems:
            print(f"    {p}")
        if problems:
            failing += 1
    manifest_missing_files = [
        rec["doc_id"] for rec in manifest
        if rec["status"] == "candidate" and not (cand_root / rec["path"]).exists()
    ]
    print(json.dumps({
        "scanned": scanned,
        "failing": failing,
        "manifestCandidates": sum(1 for r in manifest if r["status"] == "candidate"),
        "manifestCandidatesNotYetWritten": len(manifest_missing_files),
    }, ensure_ascii=False))
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())

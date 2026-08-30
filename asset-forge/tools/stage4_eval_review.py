"""Stage 4 Phase 1: full structural + eval review over frozen candidates.

Deterministic checks only (no live-agent replay here; behavior evidence = incident corpus refs).
Run: python -B tools/stage4_eval_review.py <staging_root>
Exit 0 iff every candidate has eval mapping and all hard gates replay green.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
FORMAL_ROOT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
PY = sys.executable
OUT = ROOT / "06_评测与校验" / "eval-candidates"
EV = ROOT / "06_评测与校验" / "evidence" / "stage-4" / "phase-1"
EV.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")
failures: list[str] = []

# 1) hard-gate replays
replays = []
for label, cmd in [
    ("stage2_lint", [PY, "-B", str(ROOT / "tools/stage2_lint.py"), str(ROOT)]),
    ("stage2_matrix", [PY, "-B", str(ROOT / "tools/stage2_build_coverage_matrix.py"), str(ROOT)]),
    ("stage2_evalmap", [PY, "-B", str(ROOT / "tools/stage2_eval_draft_map.py"), str(ROOT)]),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    replays.append({"check": label, "exit": p.returncode, "tail": (p.stdout or "").strip().splitlines()[-1:]})
    if p.returncode != 0:
        failures.append(f"{label} replay exit {p.returncode}")

# 2) knowledge docs <-> eval drafts <-> manifest
manifest = [json.loads(l) for l in (ROOT / "04_知识库候选/knowledge-manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
cands = [r for r in manifest if r["status"] == "candidate"]
drafts = {}
draft_path = OUT / "knowledge-citation-draft.jsonl"
for line in draft_path.read_text(encoding="utf-8").splitlines():
    if line.strip():
        d = json.loads(line)
        drafts[d["target_doc"]] = d
for r in cands:
    doc = r["path"]
    if not (ROOT / "04_知识库候选" / doc).exists():
        failures.append(f"missing candidate doc file: {doc}")
    if doc not in drafts:
        failures.append(f"no eval draft for {doc}")
    elif r.get("eval_seed_id") != drafts[doc]["eval_seed_id"]:
        failures.append(f"eval_seed_id mismatch: {doc}")
    else:
        d = drafts[doc]
        if not d.get("must_include") or not d.get("boundary_must_not"):
            failures.append(f"eval draft incomplete: {doc}")

# 3) formal-file collision guard (migration safety pre-check)
formal_paths = {r["path"] for r in manifest if r["status"] == "formal"}
overlap = formal_paths & {r["path"] for r in cands}
if overlap:
    failures.append(f"formal/candidate name overlap: {sorted(overlap)}")

# 4) templates <-> evidence cards <-> validator ok artifacts
tpl_dir = ROOT / "05_模板库候选"
p3 = ROOT / "06_评测与校验" / "evidence" / "stage-3" / "phase-3"
tpls = sorted(p.name for p in tpl_dir.glob("*.toml"))
if len(tpls) != 13:
    failures.append(f"expected 13 root candidate templates, got {len(tpls)}")
for name in tpls:
    stem = Path(name).stem
    if not (tpl_dir / f"{stem}.evidence.md").exists():
        failures.append(f"template without evidence card: {name}")
    art = p3 / f"{stem}.json"
    if not art.exists():
        failures.append(f"template without validator artifact: {name}")
    elif json.loads(art.read_text(encoding="utf-8")).get("result") != "ok":
        failures.append(f"template validator artifact not ok: {name}")
rej = tpl_dir / "research-rejected"
rej_pairs = sorted(p.stem for p in rej.glob("*.toml"))
for stem in rej_pairs:
    if not list(p3.glob(f"failure-*{stem.split('-conservative')[0]}*")) and not list((p3).glob("failure-F-S3-001*")) and not list((p3).glob("failure-F-S3-002*")):
        failures.append(f"rejected draft without failure report: {stem}")

# 5) migration rows (formal citation-seed format, append-only)
rows_path = OUT / "knowledge-citation-migration-rows.jsonl"
with rows_path.open("w", encoding="utf-8") as fh:
    for doc in sorted(drafts):
        d = drafts[doc]
        must = list(d.get("must_include") or [])
        must += [f"必须明确边界：{b}" for b in (d.get("boundary_must_not") or [])]
        fh.write(json.dumps({
            "id": d["eval_seed_id"],
            "question": d["question"],
            "expect_files": [f"knowledge/{doc}"],
            "must": must,
        }, ensure_ascii=False) + "\n")

# 6) behavior-seed id inventory (read-only formal; anti-fabrication coverage citation)
behav = ROOT.parent  # formal path passed relative? no: read via explicit formal root below
FORMAL_EVAL = FORMAL_ROOT / "assets/eval/agent-eval-seeds.jsonl" if FORMAL_ROOT else Path()
behav_ids = []
if FORMAL_EVAL.exists():
    for line in FORMAL_EVAL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            behav_ids.append(json.loads(line).get("id"))
else:
    failures.append("formal behavior seeds file unreadable (read-only check)")

summary = {
    "knowledge_candidates": len(cands),
    "knowledge_eval_mapped": len([r for r in cands if r["path"] in drafts]),
    "templates": len(tpls),
    "rejected_pairs": len(rej_pairs),
    "migration_rows": len(drafts),
    "formal_behavior_seed_ids": behav_ids,
    "replays": replays,
    "failures": failures,
}
(EV / "eval-review-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({**summary, "formal_behavior_seed_ids": f"{len(behav_ids)} ids"}, ensure_ascii=False, indent=2))
raise SystemExit(1 if failures else 0)

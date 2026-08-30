"""Stage 4 Phase 2: migration preview manifest (describe-only; NEVER executes copies).

Run: python -B tools/stage4_migration_manifest.py <staging_root>
Outputs 07_迁移包/migration-manifest.json (+ counts draft). Fails on any target collision.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
FORMAL = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
if FORMAL is None:
    raise SystemExit("usage: stage4_migration_manifest.py <AgentAssetsRoot> <formal-agent-assets-root>")
OUT_DIR = ROOT / "07_迁移包"
OUT_DIR.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

WHITELIST = ("assets/knowledge/", "assets/templates/", "assets/eval/", "compat.json")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    operations, problems = [], []

    for src in sorted((ROOT / "04_知识库候选").rglob("*.md")):
        rel = src.relative_to(ROOT / "04_知识库候选").as_posix()
        if rel == "README.md":
            continue
        target = f"assets/knowledge/{rel}"
        if (FORMAL / target).exists():
            problems.append(f"collision knowledge -> {target}")
        operations.append({"op": "create", "source": f"04_知识库候选/{rel}", "target": target,
                           "sha256": sha256(src), "size": src.stat().st_size,
                           "kind": "knowledge"})

    for src in sorted((ROOT / "05_模板库候选").glob("*.toml")):
        target = f"assets/templates/{src.name}"
        if (FORMAL / target).exists():
            problems.append(f"collision template -> {target}")
        operations.append({"op": "create", "source": f"05_模板库候选/{src.name}", "target": target,
                           "sha256": sha256(src), "size": src.stat().st_size, "kind": "template"})

    for src in sorted((ROOT / "05_模板库候选").glob("*.evidence.md")):
        target = f"assets/templates/{src.name}"
        if (FORMAL / target).exists():
            problems.append(f"collision evidence card -> {target}")
        operations.append({"op": "create", "source": f"05_模板库候选/{src.name}", "target": target,
                           "sha256": sha256(src), "size": src.stat().st_size, "kind": "template-evidence"})

    rows_path = ROOT / "06_评测与校验" / "eval-candidates" / "knowledge-citation-migration-rows.jsonl"
    rows = [json.loads(l) for l in rows_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    formal_ids = set()
    fseed = FORMAL / "assets" / "eval" / "knowledge-citation-seeds.jsonl"
    for line in fseed.read_text(encoding="utf-8").splitlines():
        if line.strip():
            formal_ids.add(json.loads(line)["id"])
    dup = [r["id"] for r in rows if r["id"] in formal_ids]
    if dup:
        problems.append(f"eval id collision: {dup}")
    operations.append({"op": "append", "source": "06_评测与校验/eval-candidates/knowledge-citation-migration-rows.jsonl",
                       "target": "assets/eval/knowledge-citation-seeds.jsonl", "rows": len(rows),
                       "row_ids": [r["id"] for r in rows], "kind": "eval-append"})

    compat_src = json.loads((FORMAL / "compat.json").read_text(encoding="utf-8"))
    n_know = sum(1 for o in operations if o["kind"] == "knowledge")
    n_tpl = sum(1 for o in operations if o["kind"] == "template")
    compat_draft = {
        **{k: v for k, v in compat_src.items() if k not in ("knowledgeDocs", "templates", "evalSeeds", "assetsVersion")},
        "assetsVersion_draft": "2026.08.30-5",
        "assetsVersion_current": compat_src["assetsVersion"],
        "knowledgeDocs": compat_src["knowledgeDocs"] + n_know,
        "templates": compat_src["templates"] + n_tpl,
        "evalSeeds": {**compat_src["evalSeeds"], "knowledgeCitation": compat_src["evalSeeds"]["knowledgeCitation"] + len(rows)},
        "note": "DRAFT ONLY: compat.json is not modified by this task; counts show post-approval state if the manifest were applied as-is.",
    }

    manifest = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sourceRoot": str(ROOT),
        "targetRepo": str(FORMAL),
        "execution": "NONE — describe-only preview; no copy/sync/commit/push/build/release performed or implied",
        "whitelist": list(WHITELIST),
        "seedingPolicy": "seed-if-missing + user-file sovereignty; this manifest contains ONLY create/append ops, zero overwrite/delete; every target pre-checked not to exist",
        "operations": operations,
        "compatCountsDraft": compat_draft,
        "problems": problems,
    }
    (OUT_DIR / "migration-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ops": len(operations), "knowledge": n_know, "templates": n_tpl,
                      "evidence_cards": len(rows), "eval_rows": len(rows), "problems": problems}, ensure_ascii=False))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

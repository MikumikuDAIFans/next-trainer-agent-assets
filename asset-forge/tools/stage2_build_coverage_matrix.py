"""Rebuild Stage 2 coverage matrix and knowledge manifest.

Reads the frozen G1 support matrix and projects every operational mode and
every training direction/topic onto candidate or formal knowledge documents.
Writes:

- 04_知识库候选/knowledge-coverage-matrix.csv
- 04_知识库候选/knowledge-manifest.jsonl

Deterministic and dependency-free so the artifacts can be reconstructed from
an empty state (Zero-Short).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

TOPICS = [
    "t-data-prep", "t-caption-tag-trigger", "t-regularization", "t-resolution-bucket",
    "t-exposure-budget", "t-learning-rate", "t-optimizer-scheduler", "t-rank-alpha",
    "t-cache-precision", "t-preview-evaluation", "t-checkpoint-selection",
    "t-troubleshooting", "t-repro-publishing", "t-evidence-rules",
    "t-external-model-reading", "t-update-channel",
]

DIRECTIONS = [
    "d-character", "d-style", "d-subject-concept", "d-object-product", "d-clothing",
    "d-visual-feature", "d-expression", "d-pose-composition", "d-lighting-color",
    "d-scene-domain", "d-utility-correction", "d-multi-concept", "d-slider",
    "d-erasure", "d-controlnet", "d-textual-inversion",
]

BOUNDARY_DIRECTIONS = {"d-slider", "d-erasure"}
UNSUPPORTED_DIRECTIONS = {"d-controlnet", "d-textual-inversion"}

# status: formal (exists in agent-assets baseline) | candidate (to be written)
DOCUMENTS = [
    # ---- formal baseline (14) ----
    {"path": "captions/wd14-tagging-guide.md", "status": "formal",
     "topics": ["t-caption-tag-trigger"]},
    {"path": "engines/anima-fast-vs-standard.md", "status": "formal",
     "modes": ["anima-fast-lora"]},
    {"path": "errors/common-errors.md", "status": "formal", "topics": ["t-troubleshooting"]},
    {"path": "errors/managed-channel-updates.md", "status": "formal", "topics": ["t-update-channel"]},
    {"path": "model-families/anima-character-case-v1.md", "status": "formal",
     "modes": ["anima-standard-lora"], "directions": ["d-character"]},
    {"path": "model-families/anima-lora-parameter-baseline.md", "status": "formal",
     "modes": ["anima-standard-lora"], "topics": ["t-rank-alpha", "t-learning-rate", "t-exposure-budget"]},
    {"path": "model-families/sd15-lora-parameter-baseline.md", "status": "formal",
     "modes": ["sd15-lora"], "topics": ["t-rank-alpha", "t-learning-rate", "t-exposure-budget"]},
    {"path": "model-families/sdxl-lora-parameter-baseline.md", "status": "formal",
     "modes": ["sdxl-lora"], "topics": ["t-rank-alpha", "t-learning-rate", "t-exposure-budget"]},
    {"path": "parameters/batch-vram.md", "status": "formal",
     "topics": ["t-exposure-budget", "t-cache-precision"]},
    {"path": "parameters/dim-alpha.md", "status": "formal", "topics": ["t-rank-alpha"]},
    {"path": "parameters/learning-rate.md", "status": "formal",
     "topics": ["t-learning-rate", "t-optimizer-scheduler"]},
    {"path": "parameters/parameter-evidence-rules.md", "status": "formal", "topics": ["t-evidence-rules"]},
    {"path": "training/curve-reading-guide.md", "status": "formal",
     "topics": ["t-preview-evaluation", "t-checkpoint-selection"]},
    {"path": "workflows/civitai-model-to-lora.md", "status": "formal", "topics": ["t-external-model-reading"]},

    # ---- candidates: batch 1 model families + engines (14) ----
    {"path": "model-families/anima-lora-workflow-guide.md", "status": "candidate", "batch": 1,
     "modes": ["anima-standard-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/anima-full-finetune-guide.md", "status": "candidate", "batch": 1,
     "modes": ["anima-full-finetune"], "topics": ["t-data-prep"]},
    {"path": "engines/anima-fast-workflow-guide.md", "status": "candidate", "batch": 1,
     "modes": ["anima-fast-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/sd15-lora-workflow-guide.md", "status": "candidate", "batch": 1,
     "modes": ["sd15-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/sd2-lora-conditions.md", "status": "candidate", "batch": 1,
     "modes": ["sd2-lora"]},
    {"path": "model-families/sdxl-lora-workflow-guide.md", "status": "candidate", "batch": 1,
     "modes": ["sdxl-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/sdxl-derived-cohorts.md", "status": "candidate", "batch": 1,
     "modes": ["sdxl-lora"]},
    {"path": "model-families/sd-dreambooth-finetune-guide.md", "status": "candidate", "batch": 1,
     "modes": ["sd15-dreambooth"], "topics": ["t-data-prep", "t-regularization"]},
    {"path": "model-families/sdxl-full-finetune-guide.md", "status": "candidate", "batch": 1,
     "modes": ["sdxl-finetune"], "topics": ["t-data-prep"]},
    {"path": "model-families/flux-lora-workflow-guide.md", "status": "candidate", "batch": 1,
     "modes": ["flux-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/chroma-flux-page-variant.md", "status": "candidate", "batch": 1,
     "modes": ["chroma-lora"]},
    {"path": "model-families/krea2-lora-musubi-guide.md", "status": "candidate", "batch": 1,
     "modes": ["krea2-lora"], "topics": ["t-data-prep"]},
    {"path": "model-families/lumina2-known-breakage.md", "status": "candidate", "batch": 1,
     "modes": ["lumina2-lora-currently-broken"]},
    {"path": "model-families/hidden-and-unsupported-boundaries.md", "status": "candidate", "batch": 1,
     "modes": ["flux-finetune-backend-hidden", "sd-lora-basic-legacy", "stability-sd3-not-exposed",
               "textual-inversion-not-exposed", "controlnet-not-exposed"],
     "directions": ["d-controlnet", "d-textual-inversion"]},

    # ---- candidates: batch 2 network algorithms (6) + directions (9) ----
    {"path": "network-algos/lokr-guide.md", "status": "candidate", "batch": 2,
     "modes": ["anima-standard-lora", "sd15-lora", "sdxl-lora", "flux-lora"]},
    {"path": "network-algos/tlora-anima-guide.md", "status": "candidate", "batch": 2,
     "modes": ["anima-standard-lora"]},
    {"path": "network-algos/dylora-guide.md", "status": "candidate", "batch": 2,
     "modes": ["sd15-lora", "sd2-lora", "sdxl-lora"]},
    {"path": "network-algos/oft-guide.md", "status": "candidate", "batch": 2,
     "modes": ["sdxl-lora", "flux-lora"]},
    {"path": "network-algos/lycoris-family-guide.md", "status": "candidate", "batch": 2,
     "modes": ["sd15-lora", "sd2-lora", "sdxl-lora", "flux-lora"]},
    {"path": "network-algos/anima-schema-only-adapters.md", "status": "candidate", "batch": 2,
     "modes": ["anima-standard-lora"]},
    {"path": "directions/character-identity.md", "status": "candidate", "batch": 2,
     "directions": ["d-character", "d-subject-concept"]},
    {"path": "directions/style-training.md", "status": "candidate", "batch": 2,
     "directions": ["d-style", "d-lighting-color"]},
    {"path": "directions/object-product-concept.md", "status": "candidate", "batch": 2,
     "directions": ["d-object-product"]},
    {"path": "directions/clothing-accessory.md", "status": "candidate", "batch": 2,
     "directions": ["d-clothing"]},
    {"path": "directions/pose-expression-features.md", "status": "candidate", "batch": 2,
     "directions": ["d-pose-composition", "d-expression", "d-visual-feature"]},
    {"path": "directions/scene-domain-migration.md", "status": "candidate", "batch": 2,
     "directions": ["d-scene-domain"]},
    {"path": "directions/utility-correction-lora.md", "status": "candidate", "batch": 2,
     "directions": ["d-utility-correction"]},
    {"path": "directions/multi-concept-training.md", "status": "candidate", "batch": 2,
     "directions": ["d-multi-concept"]},
    {"path": "directions/slider-erasure-boundaries.md", "status": "candidate", "batch": 2,
     "directions": ["d-slider", "d-erasure"]},

    # ---- candidates: batch 3 cross-domain (11) ----
    {"path": "datasets/preparation-checklist.md", "status": "candidate", "batch": 3,
     "topics": ["t-data-prep"]},
    {"path": "datasets/caption-tag-trigger-strategy.md", "status": "candidate", "batch": 3,
     "topics": ["t-caption-tag-trigger"]},
    {"path": "datasets/regularization-images.md", "status": "candidate", "batch": 3,
     "topics": ["t-regularization"]},
    {"path": "parameters/resolution-bucket.md", "status": "candidate", "batch": 3,
     "topics": ["t-resolution-bucket"]},
    {"path": "parameters/exposure-budget-steps.md", "status": "candidate", "batch": 3,
     "topics": ["t-exposure-budget"]},
    {"path": "parameters/optimizer-scheduler-guide.md", "status": "candidate", "batch": 3,
     "topics": ["t-optimizer-scheduler"]},
    {"path": "parameters/cache-precision-guide.md", "status": "candidate", "batch": 3,
     "topics": ["t-cache-precision"]},
    {"path": "training/preview-sampling-evaluation.md", "status": "candidate", "batch": 3,
     "topics": ["t-preview-evaluation"]},
    {"path": "training/checkpoint-selection.md", "status": "candidate", "batch": 3,
     "topics": ["t-checkpoint-selection"]},
    {"path": "training/repro-publishing-workflow.md", "status": "candidate", "batch": 3,
     "topics": ["t-repro-publishing"]},
    {"path": "errors/oom-performance-playbook.md", "status": "candidate", "batch": 3,
     "topics": ["t-troubleshooting"]},

    # ---- supplemental external-channel evidence: batch 4 ----
    {"path": "external-channels/sd-scripts-config-reading.md", "status": "candidate", "batch": 4,
     "topics": ["t-rank-alpha", "t-optimizer-scheduler", "t-evidence-rules"]},
    {"path": "external-channels/musubi-tuner-krea2-contract.md", "status": "candidate", "batch": 4,
     "modes": ["krea2-lora"], "topics": ["t-data-prep", "t-cache-precision"]},
    {"path": "external-channels/diffusers-lora-translation.md", "status": "candidate", "batch": 4,
     "topics": ["t-rank-alpha", "t-repro-publishing"]},
    {"path": "external-channels/diffusers-dreambooth-prior-preservation.md", "status": "candidate", "batch": 4,
     "modes": ["sd15-dreambooth"], "topics": ["t-data-prep", "t-regularization"]},
    {"path": "external-channels/lycoris-upstream-boundaries.md", "status": "candidate", "batch": 4,
     "modes": ["sd15-lora", "sd2-lora", "sdxl-lora", "flux-lora"], "topics": ["t-rank-alpha"]},
    {"path": "external-channels/alternative-tooling-evidence.md", "status": "candidate", "batch": 4,
     "topics": ["t-preview-evaluation", "t-repro-publishing"]},
    {"path": "external-channels/onetrainer-comparison.md", "status": "candidate", "batch": 5,
     "topics": ["t-data-prep", "t-preview-evaluation"]},
    {"path": "external-channels/joycaption-caption-review.md", "status": "candidate", "batch": 5,
     "topics": ["t-caption-tag-trigger", "t-data-prep"]},
    {"path": "external-channels/concept-sliders-research-channel.md", "status": "candidate", "batch": 5,
     "directions": ["d-slider", "d-erasure"], "topics": ["t-evidence-rules", "t-preview-evaluation"]},
    {"path": "external-channels/peft-adapter-taxonomy.md", "status": "candidate", "batch": 6,
     "topics": ["t-rank-alpha", "t-evidence-rules"]},
    {"path": "external-channels/safetensors-checkpoint-metadata.md", "status": "candidate", "batch": 6,
     "topics": ["t-external-model-reading", "t-repro-publishing"]},
    {"path": "external-channels/bitsandbytes-optimizer-context.md", "status": "candidate", "batch": 6,
     "topics": ["t-optimizer-scheduler", "t-cache-precision"]},
    {"path": "external-channels/attention-memory-runtime.md", "status": "candidate", "batch": 6,
     "topics": ["t-cache-precision", "t-troubleshooting"]},
    {"path": "external-channels/kohya-gui-comparison.md", "status": "candidate", "batch": 6,
     "topics": ["t-data-prep", "t-repro-publishing"]},
    {"path": "external-channels/hf-model-card-provenance.md", "status": "candidate", "batch": 7,
     "topics": ["t-external-model-reading", "t-evidence-rules"]},
    {"path": "external-channels/hf-metadata-missingness.md", "status": "candidate", "batch": 7,
     "topics": ["t-external-model-reading", "t-evidence-rules", "t-update-channel"]},
    {"path": "external-channels/examples-config-translation.md", "status": "candidate", "batch": 7,
     "topics": ["t-evidence-rules", "t-repro-publishing"]},
    {"path": "external-channels/captioning-blip-lavis-review.md", "status": "candidate", "batch": 7,
     "topics": ["t-caption-tag-trigger", "t-data-prep"]},
    {"path": "external-channels/dataset-ingestion-provenance.md", "status": "candidate", "batch": 7,
     "topics": ["t-data-prep", "t-repro-publishing"]},
    {"path": "external-channels/dataset-visual-qa-fiftyone.md", "status": "candidate", "batch": 7,
     "topics": ["t-data-prep", "t-resolution-bucket", "t-troubleshooting"]},
    {"path": "external-channels/clip-evaluation-boundaries.md", "status": "candidate", "batch": 7,
     "topics": ["t-preview-evaluation", "t-checkpoint-selection", "t-evidence-rules"]},
    {"path": "external-channels/pytorch-runtime-reproducibility.md", "status": "candidate", "batch": 7,
     "topics": ["t-cache-precision", "t-troubleshooting", "t-repro-publishing"]},
    {"path": "external-channels/dataset-curation-datacomp.md", "status": "candidate", "batch": 7,
     "topics": ["t-data-prep", "t-evidence-rules"]},
    {"path": "external-channels/instruction-editing-objective-boundary.md", "status": "candidate", "batch": 7,
     "directions": ["d-utility-correction", "d-multi-concept"], "topics": ["t-data-prep", "t-evidence-rules"]},
]

GLOBAL_TOPIC_OWNERS = {
    "t-evidence-rules": "parameters/parameter-evidence-rules.md",
    "t-external-model-reading": "workflows/civitai-model-to-lora.md",
    "t-update-channel": "errors/managed-channel-updates.md",
}

OPERATIONAL_LEVELS = {"first-class", "conditional"}


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    matrix_path = root / "01_训练器能力盘点" / "support-matrix.json"
    out_dir = root / "04_知识库候选"
    out_dir.mkdir(parents=True, exist_ok=True)
    support = json.loads(matrix_path.read_text(encoding="utf-8"))
    modes = [(e["id"], e["supportLevel"]) for e in support["entries"]]
    mode_ids = {m for m, _ in modes}

    doc_by_path = {d["path"]: d for d in DOCUMENTS}
    errors: list[str] = []
    for d in DOCUMENTS:
        for key in ("modes", "directions", "topics"):
            for item in d.get(key, []):
                pool = {"modes": mode_ids, "directions": set(DIRECTIONS), "topics": set(TOPICS)}[key]
                if item not in pool:
                    errors.append(f"doc {d['path']} references unknown {key[:-1]}: {item}")

    def topic_owner(mode: str, topic: str) -> tuple[str, str]:
        """Return (owner_doc, status) for a mode x topic cell."""
        if topic in GLOBAL_TOPIC_OWNERS:
            return GLOBAL_TOPIC_OWNERS[topic], "covered-by-formal"
        mode_doc = next((d["path"] for d in DOCUMENTS if mode in d.get("modes", []) and topic in d.get("topics", [])), None)
        if mode_doc:
            return mode_doc, "covered-by-mode-doc"
        topic_docs = [d["path"] for d in DOCUMENTS if topic in d.get("topics", []) and not d.get("modes")]
        if topic_docs:
            primary = next((p for p in topic_docs if doc_by_path[p]["status"] == "candidate"), topic_docs[0])
            extra = [p for p in topic_docs if p != primary]
            status = ("covered-by-candidate" if doc_by_path[primary]["status"] == "candidate" else "covered-by-formal")
            return ";".join([primary] + extra), status
        return "", "MISSING"

    def direction_owner(mode: str, direction: str) -> tuple[str, str]:
        if direction in UNSUPPORTED_DIRECTIONS:
            return "model-families/hidden-and-unsupported-boundaries.md", "boundary-unsupported"
        if direction in BOUNDARY_DIRECTIONS:
            return "directions/slider-erasure-boundaries.md", "boundary-not-first-class"
        owner = next((d["path"] for d in DOCUMENTS if direction in d.get("directions", [])), None)
        if not owner:
            return "", "MISSING"
        return owner, "covered-by-candidate"

    rows = []
    for mode, level in modes:
        operational = level in OPERATIONAL_LEVELS
        for topic in TOPICS:
            if operational:
                owner, status = topic_owner(mode, topic)
            else:
                owner, status = "", "n/a-mode-not-operational"
            if status == "MISSING":
                errors.append(f"cell mode={mode} topic={topic} has no owner")
            rows.append({"dim": "topic", "mode_id": mode, "support_level": level,
                         "dim_id": topic, "owner_docs": owner, "coverage_status": status})
        for direction in DIRECTIONS:
            if operational:
                owner, status = direction_owner(mode, direction)
            else:
                owner, status = "", "n/a-mode-not-operational"
            if status == "MISSING":
                errors.append(f"cell mode={mode} direction={direction} has no owner")
            rows.append({"dim": "direction", "mode_id": mode, "support_level": level,
                         "dim_id": direction, "owner_docs": owner, "coverage_status": status})

    # every formal-baseline doc and candidate doc gets a manifest record
    # eval_seed_id is attached from the citation-draft jsonl when present (Phase 3)
    eval_map: dict[str, str] = {}
    draft_path = root / "06_评测与校验" / "eval-candidates" / "knowledge-citation-draft.jsonl"
    if draft_path.exists():
        for line in draft_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                eval_map[rec["target_doc"]] = rec["eval_seed_id"]
    manifest = []
    for d in sorted(DOCUMENTS, key=lambda x: x["path"]):
        manifest.append({
            "doc_id": d["path"], "path": d["path"], "status": d["status"],
            "batch": d.get("batch"), "modes": d.get("modes", []),
            "topics": d.get("topics", []), "directions": d.get("directions", []),
            "eval_seed_id": eval_map.get(d["path"]),
        })

    csv_path = out_dir / "knowledge-coverage-matrix.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["dim", "mode_id", "support_level", "dim_id", "owner_docs", "coverage_status"])
        writer.writeheader()
        writer.writerows(rows)
    jsonl_path = out_dir / "knowledge-manifest.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for rec in manifest:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    summary = {
        "modes": len(modes),
        "operationalModes": sum(1 for _, lvl in modes if lvl in OPERATIONAL_LEVELS),
        "cells": len(rows),
        "cellsMissing": sum(1 for r in rows if r["coverage_status"] == "MISSING"),
        "docsFormal": sum(1 for d in DOCUMENTS if d["status"] == "formal"),
        "docsCandidate": sum(1 for d in DOCUMENTS if d["status"] == "candidate"),
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

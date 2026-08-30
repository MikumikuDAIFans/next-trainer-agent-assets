# External Collection Playbook（可复用信息收集流程）

- Version: `2026-08-30`
- Scope: catalog-driven, bounded public-source collection for Next Trainer knowledge and template evidence.
- Evidence status: process contract; each run must attach round logs and source revisions.
- Aliases / 检索关键词: 信息收集流程, external harvest, source pipeline, round, revision pinning, 去重, evidence tier

## Pipeline

`catalog → preflight → bounded fetch → status/hash/revision log → short extraction → source registry → candidate doc/template → validator/eval → dedup → manifest/Zero-Short`

## Channel classes

| Class | Examples | Safe extraction |
|---|---|---|
| Product contract | Next Trainer source, schema, preset, validator | support and field facts (L1) |
| Official trainer/model repo | sd-scripts, Musubi-Tuner, Diffusers, LyCORIS, FLUX | terminology, script semantics, revisions (L1) |
| Official docs/papers | HF docs, LoRA/DyLoRA/OFT/slider papers | method context and boundaries (L1) |
| Data/caption/eval tools | WD14, JoyCaption, Datasets, OneTrainer | review questions and comparison practices (L1/L3) |
| Public metadata | Civitai API/model pages, HF model cards | observed distributions and missingness (L2) |

## Round protocol

1. Select a contiguous catalog slice and record `start`, `limit`, timestamp, proxy, and tool version.
2. Enforce public anonymous requests, 20-second timeout, response cap, ≥0.5-second spacing, and no body retention.
3. For GitHub repos, query the public latest-commit API separately; record revision or 404.
4. Normalize source records by canonical URL/repository ID; do not count a repo page and its commit API as two independent sources.
5. Extract only short facts needed by a candidate question. Preserve unknowns and record the extraction rule/confidence.
6. Before creating a template, map every key to current page/schema/preset/validator evidence; otherwise create knowledge-only material.
7. After each round, write a summary and failure report before starting the next round.

## Deduplication and confidence

- Source dedup key: canonical host + repository/path + observed revision.
- Claim dedup key: normalized statement + scope + evidence level.
- Template dedup key: target page + model_train_type + algorithm + materially distinct fields.
- Confidence: `high` for direct current-contract facts, `medium` for pinned official external facts, `low` for public examples/free-text extraction.

## Limits and cleanup

- Default per round: ≤20 requests, ≤128 KiB retained response sample metadata, ≤20 seconds/request, ≥0.5 seconds spacing.
- No images, model weights, credentials, private data, or long text.
- Retain logs, summaries, failures, source IDs, revisions, candidate/eval/manifest outputs; discard response bodies and temporary caches.

## Failure handling

404/410: mark source unverified and do not cite precise claims. 429/5xx/timeouts: keep failure, retry only within the round budget. Incomplete response: do not infer content. Validator negative-control leak: reject template and preserve regression evidence.

## Reproducibility commands

```text
python -B tools/external_channel_harvest.py <AgentAssetsRoot> --start <N> --limit <M>
python -B tools/stage2_build_coverage_matrix.py <AgentAssetsRoot>
python -B tools/stage2_eval_draft_map.py <AgentAssetsRoot>
python -B tools/stage2_lint.py <AgentAssetsRoot>
<project>/.venv-dev/Scripts/python.exe -B tools/stage3_validate_templates.py <AgentAssetsRoot> <project>
python -B tools/stage4_eval_review.py <AgentAssetsRoot>
python -B tools/stage4_migration_manifest.py <AgentAssetsRoot>
python -B tools/stage4_zero_short.py <AgentAssetsRoot> <project>
```

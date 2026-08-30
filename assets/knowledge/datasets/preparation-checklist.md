# Dataset preparation checklist (contract-level structure gates)

- Version: `2026-08-30`
- Scope: the structural rules a dataset folder must satisfy before submit — repeat-prefixed subdirs, image/caption pairing, resolution/bucket fields — including the one destructive convenience behavior (`_zkz` auto-move) that users must know before validating or submitting.
- Evidence status: L1 project contract (`mikazuki/utils/train_utils.py` validate_data_dir, `shared.ts` DATASET_SETTINGS/CAPTION_SETTINGS); conflict register C-012.
- Aliases / 检索关键词: 数据集, dataset, train_data_dir, repeats, 子目录, zkz, 目录结构, 提交前检查, caption 配对

## Hard structural gate (L1)

`validate_data_dir` accepts a `train_data_dir` when it contains **at least one subdirectory matching `^\d+_.+`** (repeat-count prefix):

```text
X:/train/my-model/
  10_my-concept/      <- <repeats>_<name>; images + same-stem .txt captions inside
    img001.png
    img001.txt
  3_variants/         <- multiple subdirs = multiple dataset entries, repeats per dir
```

- Caption pairing: `caption_extension` default `.txt`, one file per image stem (CAPTION_SETTINGS).
- Flat directory (no subdir): validation warns, then **auto-creates `<suggested_repeat>_zkz` and MOVES all loose images and captions into it** (conflict C-012, P1 knowledge-safety item). Suggested repeats start at 7 for ≤10 images.
- **Required advice before submit:** always pre-create numbered subdirectories yourself; treat "validation passed" as having possibly relocated your loose files. Back up flat folders before running validation/training. The move is idempotent-ish but surprises people mid-pipeline.
- Empty dir or no images at all → hard error path (log + false).

## Resolution & bucket fields to state explicitly (L1 defaults)

| Field | Default | Note |
|---|---|---|
| `resolution` | `"512,512"` | string W,H, each a multiple of 64, non-square allowed |
| `enable_bucket` | true | arb buckets for mixed aspect ratios |
| `min_bucket_reso` / `max_bucket_reso` | 256 / 1024 | clamp range |
| `bucket_reso_steps` | 64 | SDXL may use 32; **below 32 fails on SDXL** (schema note) |
| `bucket_no_upscale` | true | small images go to smaller buckets; nothing gets upscaled |

Per-family starting resolutions (1024 for Anima/SDXL/Krea 2, 768 for Flux, 512-class for SD 1.x) are recorded in the page guides with their evidence tags — never inherited silently.

## Pre-submit checklist (contract-derived)

1. [ ] At least one `^\d+_` subdir inside `train_data_dir`; loose files intentionally zero (avoid `_zkz` surprise).
2. [ ] Every image has a same-stem caption file (extension matches `caption_extension`); empty captions allowed only when intentional.
3. [ ] `resolution` string fits the base family and is a 64-multiple; bucket range covers the actual aspect distribution.
4. [ ] Caption convention (trigger/caption-out choices) already decided — see `caption-tag-trigger-strategy.md`.
5. [ ] For DreamBooth-type runs: regularization decision made (`regularization-images.md`).
6. [ ] Dataset-level dedup: near-duplicate frames inflate effective repeats silently (exposure math in `../parameters/exposure-budget-steps.md`).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/utils/train_utils.py` (validate_data_dir / suggest_num_repeat), `mikazuki/schema/shared.ts` (DATASET_SETTINGS, CAPTION_SETTINGS).
- Staging artifacts: `01_训练器能力盘点/support-conflicts.md` C-012 (destructive auto-move), C-011 (model-family validation laxness — dataset dir pass ≠ model match).
- Formal knowledge: `captions/wd14-tagging-guide.md` (tagging pipeline; not repeated here).

## Boundaries

- This checklist is structural, not quality: image counts/quality per direction live in the `directions/` docs; no universal minimum image count is claimed (none exists in the audited contract).
- No scraping or dataset-sourcing guidance; rights are user-side.
- The `_zkz` behavior is pinned to the audited commit — a product fix could remove it; re-check wording after upgrades.

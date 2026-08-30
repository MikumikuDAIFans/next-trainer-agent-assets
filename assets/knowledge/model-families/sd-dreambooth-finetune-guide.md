# SD 1.x/2.x DreamBooth finetune guide (page `dreambooth` → `sd-dreambooth`)

- Version: `2026-08-30`
- Scope: workflow for the DreamBooth/model-finetune page on SD 1.x/2.x bases (`model_train_type = sd-dreambooth`, kohya `train_db.py`). Covers instance/regularization dataset contract, the SD2 flag discipline, schema defaults, and full-model risk profile.
- Evidence status: L1 project contract (schema `dreambooth.ts`, support matrix entry `sd15-dreambooth`). No shipped DreamBooth preset/template and no measured local DreamBooth run exist in the audited evidence set.
- Aliases / 检索关键词: dreambooth, sd-dreambooth, train_db, 微调, model finetune, 正则化图, prior loss, instance dataset

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `dreambooth` page, `model_train_type = sd-dreambooth` | `mikazuki/schema/dreambooth.ts:4-24`, `mikazuki/app/api.py:156` |
| Backend | `./scripts/stable/train_db.py` (DreamBooth/model fine-tuning) | support-matrix `sd15-dreambooth` |
| Output | a full model checkpoint — not a LoRA ("LoRA output" is an explicit unsupported objective) | support-matrix |
| SD 2.x bases | same `v2` flag requirement as the LoRA page, with the `v_parameterization`/`scale_v_pred_loss_like_noise_pred` union block under `v2=true` | `dreambooth.ts:10-26` |
| Recorded specialization | subject/identity personalization is the named direction interface | support-matrix `specializedDirections` |

## Dataset contract (L1 fields)

- `train_data_dir`: instance images (the subject). `reg_data_dir`: regularization images, default off ("默认留空，不使用正则化图像"); `prior_loss_weight` scales the prior loss when regularization is used. See `../datasets/regularization-images.md` (batch 3) for when regularization is worth its cost.
- `resolution` default `"512,512"`, buckets default on (256–1024, step 64).
- Caption/tag block matches the LoRA pages (`caption_extension`, shuffle, keep_tokens, dropout family).

## Defaults that matter (L1 schema)

- `learning_rate` default `1e-6`, `learning_rate_te` default `5e-7` — three orders of magnitude below LoRA LRs because full weights are updated. Do not port LoRA-class LRs here.
- `stop_text_encoder_training` (sd-dreambooth only): stop TE training at step N, `-1` disables TE training entirely.
- `save_state` + `resume` support for interrupted runs; `save_every_n_epochs` default 2.
- Optimizer union defaults to `AdamW8bit`; noise utilities (`noise_offset` ~0.1 or multires noise — mutually exclusive per schema) exist as on other families.
- Preview prompts use the classic SD prompt syntax block (`--n/--w/--h/--l/--s/--d`).

## Workflow checklist

1. Decide LoRA-vs-DreamBooth first: if an adapter would do, use the LoRA page; DreamBooth writes a whole checkpoint (disk, VRAM, forgetting risk).
2. Instance set + trigger/class-token design per `../directions/character-identity.md`; add regularization images only after reading the regularization doc — the product default is off.
3. SD 2.x base: apply the v2/v-pred discipline exactly as in `sd2-lora-conditions.md`.
4. Start at the schema-default LRs (1e-6 / 5e-7); they are product contract defaults, not measured optima — sweep from below and record.
5. Evaluate against the untouched base on fixed prompts; also spot-check a few general prompts outside the subject for forgetting symptoms (style drift, anatomy breakage on unrelated prompts).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/dreambooth.ts`, `mikazuki/app/api.py`.
- Frozen support matrix entry `sd15-dreambooth` (staging artifact `01_训练器能力盘点/support-matrix.json`).
- Formal knowledge baseline: `parameters/parameter-evidence-rules.md` (how to attach evidence to any number you record).

## Boundaries

- No shipped DreamBooth template/preset and no measured local run: everything numeric above is a schema default; never present defaults as validated best values.
- SDXL full finetune is a different train type (`sdxl-finetune`) with its own TE1/TE2 fields — see `sdxl-full-finetune-guide.md`.
- DreamBooth ≠ LoRA: adapter export, low-VRAM claims and "just load on base" workflows do not apply.
- Regularization images with downloaded third-party pictures can carry license/personality concerns; use class-matched licensed material (see `../datasets/regularization-images.md`).

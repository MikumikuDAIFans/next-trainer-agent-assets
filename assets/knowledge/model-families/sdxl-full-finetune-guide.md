# SDXL full finetune guide (page `dreambooth` → `sdxl-finetune`)

- Version: `2026-08-30`
- Scope: the first-class SDXL full-model finetune (`model_train_type = sdxl-finetune`, kohya `sdxl_train.py`), how it differs from SD1.x DreamBooth on the same page, TE1/TE2 learning-rate handling, and the SDXL-only precision switches.
- Evidence status: L1 project contract (schema `dreambooth.ts` sdxl branch, support matrix entry `sdxl-finetune`). No shipped preset/template and no measured local SDXL finetune run exist in the audited evidence set.
- Aliases / 检索关键词: sdxl finetune, sdxl-finetune, 全量微调 sdxl, sdxl_train, learning_rate_te1, learning_rate_te2, full_bf16

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `dreambooth` page, `model_train_type = sdxl-finetune` (also the schema page default) | `mikazuki/schema/dreambooth.ts:4-5`, `dreambooth.ts:71-78`, `mikazuki/app/api.py:157` |
| Backend | `./scripts/stable/sdxl_train.py` full finetune path (not `train_db.py`) | support-matrix `sdxl-finetune` |
| Output | full SDXL checkpoint; "LoRA output" is an explicit unsupported objective | support-matrix |
| TE handling | separate `learning_rate_te1` (ViT-L) and `learning_rate_te2` (BiG-G) string fields, default `5e-7` each | `dreambooth.ts:71-78` |
| Precision | `full_bf16` switch is documented as SDXL-only in the shared speed block | `dreambooth.ts` speed-options block |

## Differences from SD1.x DreamBooth (same page, different contract)

1. Backend script differs (`sdxl_train.py` vs `train_db.py`): this is a full-model trainer, not the DreamBooth prior-loss flow — the regularization/prior-loss fields belong to the `sd-dreambooth` branch semantics.
2. Two text encoders get their own LR fields; freezing or lowering both is the conservative default pattern (defaults are already far below LoRA LRs).
3. SDXL-family bases include the compatible derivatives recognized by the SDXL page rules; apply the same base-mismatch discipline as `sdxl-derived-cohorts.md`.

## Defaults that matter (L1 schema)

- `learning_rate` default `1e-6`, TE1/TE2 `5e-7`; `optimizer_type` union default `AdamW8bit`; scheduler block defaults `cosine_with_restarts`.
- `save_state`/`resume`, `save_every_n_epochs` default 2, `save_model_as` default safetensors — full checkpoints per save; size the disk budget accordingly.
- `resolution` default `"512,512"` on this shared schema, but SDXL-class training normally runs 1024; the field is user-set, so state it explicitly in every plan instead of inheriting silently.

## Workflow checklist

1. Confirm the goal needs full-weight updates; default alternative is `sdxl-lora` (`sdxl-lora-workflow-guide.md`).
2. Dataset/metadata discipline identical to the LoRA family (see `../datasets/preparation-checklist.md`, batch 3) — full finetune does not relax caption/trigger requirements.
3. Decide TE policy explicitly (both TE LRs are separate fields); for narrow domain shifts consider TE-freezing arguments — mark such choices as L3 experiments unless validated.
4. Fixed-prompt evaluation against the untouched base, including prompts outside the training domain to catch catastrophic forgetting; keep multiple checkpoints.
5. If using `full_bf16` (SDXL-only per schema), record it — it changes memory profile and numerics vs the default mixed-precision path.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/dreambooth.ts`, `mikazuki/app/api.py:157`.
- Frozen support matrix entry `sdxl-finetune` (staging artifact `01_训练器能力盘点/support-matrix.json`).

## Boundaries

- No shipped preset and no measured SDXL-finetune run in the audited set: every concrete number here is a schema default; do not present defaults as best values, and do not import community finetune LRs as if they were product facts.
- Not available for other families: Flux full finetune is UI-hidden, Krea 2/Lumina 2 have none (`hidden-and-unsupported-boundaries.md`, `lumina2-known-breakage.md`).
- "sdxl-finetune can also make LoRAs" is false by contract (LoRA output unsupported on this train type).

# SD 1.x LoRA workflow guide (page `lora-master` → `sd-lora`)

- Version: `2026-08-30`
- Scope: workflow for SD 1.x LoRA on the shared LoRA master page (`model_train_type = sd-lora`, kohya `train_network.py`). Covers contract facts, page defaults, adapter options actually available, and where measured numbers exist or do not.
- Evidence status: L1 project contract (schema `lora-master.ts`, support matrix entry `sd15-lora`); SD 1.5 measured baseline in the formal knowledge set is method-level, not a parameter guarantee.
- Aliases / 检索关键词: sd1.5, sd15, sd1x, sd-lora, lora-master, kohya, train_network, dim32, 512

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `lora-master`, `model_train_type = sd-lora` (same page also serves `sdxl-lora`) | `mikazuki/schema/lora-master.ts:4-20`, `mikazuki/app/api.py:153` |
| Backend | `./scripts/stable/train_network.py` | support-matrix `sd15-lora` |
| Network modules | `networks.lora` (default), `networks.dylora`, `lycoris.kohya` | `lora-master.ts` |
| Rejected on SD1.x | native `networks.oft` (frontend diagnostic refuses) | support-matrix `unsupportedSpecializedObjectives` |
| Support level | first-class | support-matrix |

## Page defaults that matter (L1 schema defaults)

- `network_dim = 32`, `network_alpha = 32` (schema defaults; the docs themselves warn dim is "not better when bigger" and small dim saves VRAM).
- Page train-type default is `sdxl-lora` — when training SD 1.x you must explicitly select `sd-lora`; a silently inherited default is a classic mismatch source.
- `pretrained_model_name_or_path` default file name points at an SDXL example; always set the real SD 1.x checkpoint path (placeholders like `X:/sd-models/sd15/...` in shared configs).

## Workflow checklist

1. Select `sd-lora`, set the SD 1.x checkpoint; SD 2.x bases instead follow `sd2-lora-conditions.md` (v2/v-pred flags) — do not train SD2 silently as SD1.
2. Dataset: SD 1.x native class is 512-resolution; bucket settings exist on the page. Keep `enable_bucket` on for mixed aspect ratios. See `../datasets/preparation-checklist.md` (batch 3) and `../parameters/resolution-bucket.md`.
3. Adapter: default LoRA; DyLoRA / LoKr / LoHa / LoCon / IA3 / GLoRA / Diag-OFT / BOFT arrive through `networks.dylora` or `lycoris.kohya` — algorithm specifics belong to `../network-algos/` guides (batch 2).
4. Capture/repeat/steps: SD 1.x has **no shipped preset TOML and no measured parameter table in this project's evidence**. The formal doc `model-families/sd15-lora-parameter-baseline.md` gives the recording/sweep method (log dim, alpha, repeats, resolution, batch, total steps together; compare under a fixed validation prompt set). Follow that method; treat every concrete number you see elsewhere as unvalidated until your own sweep confirms it.
5. Validation: fixed prompts + fixed seed preview per epoch-ish cadence; overfitting/underfitting calls per `../training/curve-reading` conventions (formal doc `training/curve-reading-guide.md`).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/lora-master.ts`, `mikazuki/app/api.py`.
- Formal knowledge baseline: `model-families/sd15-lora-parameter-baseline.md` (sweep discipline; local project baseline, not causal).
- Frozen support matrix entry `sd15-lora` (staging artifact).

## Boundaries

- No shipped SD1.5 preset and no measured SD1.5 parameter table exists in the audited evidence: do not fabricate LR/step/VRAM numbers for SD 1.5; say "no measured baseline in-project" instead.
- Native OFT is rejected on SD1.x (validator-level); OFT discussion lives in `../network-algos/oft-guide.md` for SDXL/Flux only.
- "Works with Pony-style SDXL recipes" is false by construction — different page train type, resolution class and text encoders.

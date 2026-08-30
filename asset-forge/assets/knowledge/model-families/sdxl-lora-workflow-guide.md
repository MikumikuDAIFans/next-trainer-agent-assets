# SDXL LoRA workflow guide (page `lora-master` → `sdxl-lora`)

- Version: `2026-08-30`
- Scope: workflow for SDXL-family LoRA on the shared LoRA master page (`model_train_type = sdxl-lora`, kohya `sdxl_train_network.py`). Covers prediction-type selection, adapter availability, the heuristic starting box already in the formal knowledge set, and derived-cohort routing.
- Evidence status: L1 project contract (schema `lora-master.ts`, support matrix entry `sdxl-lora`, imported-template mapping `config_import.py:109-113`); the conservative starting box is the formal heuristic baseline doc, not a measured guarantee.
- Aliases / 检索关键词: sdxl, sdxl-lora, lora-master, v-pred, eps, rectified flow, prediction type, pony, illustrious

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `lora-master`, `model_train_type = sdxl-lora` (page default) | `mikazuki/schema/lora-master.ts:4-20` |
| Backend | `./vendor/sd-scripts/sdxl_train_network.py` | support-matrix `sdxl-lora` |
| Network modules | `networks.lora`, `networks.dylora`, `networks.oft`, `lycoris.kohya` (LoCon/LoHa/LoKr/IA3/GLoRA/Diag-OFT/BOFT) | `lora-master.ts:93-117` |
| Prediction type | must match the checkpoint: EPS vs v-prediction vs rectified-flow derivative — this is a recorded product prerequisite for this train type | support-matrix `sdxl-lora` prerequisites (frozen) |
| Support level | first-class, including Pony/Illustrious/NoobXL-compatible derivatives routed through this page | support-matrix `baseModelVariants`; `config_import.py` SDXL path rules match `noobxl|pony|illustrious` |

## Workflow checklist

1. Set the real SDXL-family checkpoint; then verify the prediction-type configuration matches that checkpoint's own spec (see `sdxl-derived-cohorts.md` for cohort mismatch traps — this is the top SDXL failure mode).
2. Dataset: 1024-class images with buckets; mixed sources keep no-upscale behavior deliberate (see `../parameters/resolution-bucket.md`, batch 3).
3. Adapter choice: default `networks.lora`; OFT is natively available here (unlike SD1.x); DyLoRA has both a native module and a LyCORIS variant — see `../network-algos/dylora-guide.md` (batch 2) so the two entries are not confused.
4. Starting box — cite the formal heuristic doc rather than restating numbers here: dim/alpha tiers, LR magnitudes, steps, batch/accumulation and optimizer choices are recorded in `model-families/sdxl-lora-parameter-baseline.md` (formal knowledge, explicitly marked *heuristic*, community starting points, not measured in-project). The shipped `sdxl-lora-conservative.toml` template mirrors that box.
5. Two text encoders: TE1/TE2 LR fields are separate on this train type (`config_import.py` mapping). For pure identity work, freezing or lowering TE LR first is the pattern recorded in the formal baseline doc.
6. Validate on fixed prompts/seeds; over/underfit calls per the formal curve guide.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/lora-master.ts`, `mikazuki/utils/config_import.py`, `mikazuki/app/api.py:154`.
- Formal knowledge baseline: `model-families/sdxl-lora-parameter-baseline.md` (heuristic), `assets/templates/sdxl-lora-conservative.toml` (shipped template).
- Frozen support matrix entry `sdxl-lora` (staging artifact).

## Boundaries

- The heuristic box numbers are community starting points; this KB may not upgrade them to "recommended values" without a measured local run (EDD rule).
- Prediction-type per cohort (Pony/NoobXL/Illustrious variants) is not hardcoded in this knowledge base; take it from each checkpoint's published spec — otherwise keep it unknown.
- SDXL DreamBooth/full finetune is a different page (`sdxl-finetune`), see `sdxl-full-finetune-guide.md`.

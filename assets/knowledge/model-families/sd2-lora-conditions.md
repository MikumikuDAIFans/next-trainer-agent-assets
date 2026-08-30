# SD 2.x LoRA conditions (conditional mode on the SD page)

- Version: `2026-08-30`
- Scope: how SD 2.0/2.1 LoRA training is actually reached today (shared `sd-lora` page plus explicit v2/v-prediction flags), what must be set, and what remains unavailable.
- Evidence status: L1 project contract (support matrix entry `sd2-lora`, `lora-master.ts:12-23`, `train_utils.py:309-315`).
- Aliases / 检索关键词: sd2, sd2.1, sd20, v2, v-pred, v_parameterization, sd-lora, 条件支持

## Contract facts (L1)

- There is **no dedicated SD 2.x workbench selection** (explicitly listed as unsupported in the support matrix). SD 2.x LoRA is conditional support layered on the SD page:
  1. select the SD 1.5-style LoRA form on the workbench (page train type `sd-lora`);
  2. set `v2 = true` (schema note: bases from SD 2.0 onward need this);
  3. when the specific model needs v-prediction, also set `v_parameterization` (and `scale_v_pred_loss_like_noise_pred` where the pair applies — the schema exposes both under the v2 branch).
- Backend: same kohya `train_network.py` path as SD 1.x; the difference is purely these prediction/normalization flags plus the checkpoint itself. Evidence: support-matrix `sd2-lora` prerequisites, `mikazuki/schema/lora-master.ts:12-23`, `mikazuki/utils/train_utils.py:309-315`.

## Decision guide

| Model | v2 | v_parameterization |
|---|---|---|
| SD 1.4 / 1.5 | false | false |
| SD 2.0 / 2.1 base | true | per model card (768-v variants use v-prediction) |

If the base model's own release metadata does not state the prediction type, this remains **unknown**: start without v-pred, evaluate, or choose a base whose spec is explicit. Do not guess from the file name alone.

## Failure modes (contract-derived)

- Training an SD 2.1 v-pred checkpoint without `v_parameterization` (or the reverse) produces a visibly broken/mushy adapter — the flags are part of the base-model contract, not preferences.
- Leaving `v2 = false` for any SD 2.x base is the single most common misconfiguration for this family.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/lora-master.ts`, `mikazuki/utils/train_utils.py`.
- Frozen support matrix entry `sd2-lora` (staging artifact `01_训练器能力盘点/support-matrix.json`).
- Workflow base steps: see `sd15-lora-workflow-guide.md` (same page/backend).

## Boundaries

- SD 2.x remains "conditional": there is no first-class UI model selection; every answer must include the v2/v-pred caveat explicitly.
- No shipped preset and no measured SD 2.x parameter table exists in the audited evidence set — concrete LR/step numbers for SD 2.x are unknown here.
- DreamBooth on SD 2.x follows the same flag discipline (`sd-dreambooth-finetune-guide.md`).

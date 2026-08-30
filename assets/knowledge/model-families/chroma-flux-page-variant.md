# Chroma on the Flux page (model variant, not a separate page)

- Version: `2026-08-30`
- Scope: training Chroma LoRA through the existing `flux-lora` page by selecting `model_type = chroma`, including the shipped Chroma preset's exact field set and what must not be claimed about this variant.
- Evidence status: L1 project contract (schema union value + shipped preset + support matrix entry `chroma-lora`). No measured Chroma run exists in the audited evidence set.
- Aliases / 检索关键词: chroma, model_type, flux-lora 变体, t5 attn mask, guidance 0, raw prediction

## Contract facts (L1)

- Chroma is a **model variant inside the Flux page**, not its own workbench module: `model_type: union(["flux", "chroma"])` on `flux-lora.ts`; the backend stays `flux_train_network.py`.
- Support level recorded as first-class variant with prerequisite `set model_type=chroma` plus matching Chroma assets (support-matrix `chroma-lora`; evidence `flux-lora.ts:3-5`, `config/presets/chroma.toml`).
- A dedicated Chroma page does not exist and would be a false claim (`unsupportedSpecializedObjectives`).

## Shipped preset field set (L1 — `config/presets/chroma.toml`)

Beyond the four Flux asset paths (the preset is a minimal diff template), the shipped Chroma preset sets exactly:

```toml
[data]
model_type = "chroma"
apply_t5_attn_mask = true
timestep_sampling = "sigmoid"
model_prediction_type = "raw"
guidance_scale = 0.0
```

Reading: Chroma's documented contract shape here is raw prediction with guidance off and T5 attention masking on. Keep these as a unit when starting from this preset — cherry-picking only some of them breaks the variant contract the preset encodes.

## Workflow

1. Open the Flux LoRA page; import/pick the Chroma preset; then confirm `model_type = chroma` actually stayed set (variant selection is the single point of failure when reusing saved configs).
2. Replace asset paths with the real Chroma files (placeholders like `X:/sd-models/chroma/...` in shared documents).
3. Everything else follows the Flux workflow guide (`flux-lora-workflow-guide.md`): FP8 defaults, caching semantics, small-dim network defaults, preview discipline.
4. There is **no measured Chroma parameter table** in this project's audited evidence — LR/steps/VRAM claims are unknown-here; sweep and record.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/flux-lora.ts`, `config/presets/chroma.toml`.
- Frozen support matrix entry `chroma-lora` (staging artifact `01_训练器能力盘点/support-matrix.json`).

## Boundaries

- Do not describe Chroma as "just another Flux checkpoint": its preset encodes different prediction/guidance values; treating it as flux-default silently is the top Chroma misconfiguration.
- Do not hardcode per-checkpoint differences beyond what the shipped preset shows; any deeper Chroma-internal claims are unknown-here.
- Template surface: any future Chroma template must live on the `flux-lora` validator with `model_type=chroma` inside, never on a fake `chroma-lora` train type.

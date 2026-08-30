# Slider LoRA & concept erasure — boundary doc (not first-class; do not fabricate workflows)

- Version: `2026-08-30`
- Scope: calibrated attribute sliders (Concept-Sliders-style) and concept erasure/suppression: what these methods require, what this product actually provides (nothing specialized), the `enable_base_weight` misconception, and how to answer these requests honestly.
- Evidence status: L1 project contract (support matrix `unsupportedSpecializedObjectives` across operational entries; taxonomy rows "not first-class") + registered method paper (Concept Sliders arXiv:2311.12092, title-verified via arXiv API in Stage 1; exact paper URL recorded in source registry as research lead only).
- Aliases / 检索关键词: slider, 滑块, concept slider, 概念擦除, erasure, suppression, negate, base weight, 差异炼丹误区, 强度控制

## What the methods require (public method context — L1 official)

- **Concept Sliders** (arXiv:2311.12092): trains a small adapter from **paired synthetic datasets** contrasting a concept axis (e.g., elderly↔younger rendered pairs), yielding an approximately linear control direction with sign/value semantics at inference.
- **Concept erasure/suppression** families: define explicit erasure objectives (loss terms over target concepts / regularization against activations), i.e., a *negative training signal* the trainer must implement.

## What this product provides (L1, and only this)

- LoRA/adapter training toward data distributions on each page — standard positive supervision.
- **No paired-positive/negative dataset contract, no slider loss, no erasure loss, no calibration workflow** anywhere in the audited workbench/API surface (support matrix records these as unsupported specialized objectives; taxonomy: `not first-class`).
- `enable_base_weight`/`base_weights` (NETWORK_OPTION_BASEWEIGHT) rebases training on existing adapter weights ("差异炼丹"). It adds no concept axis, no contrast pairs, no calibration — treating it as a slider trainer is a category error the taxonomy explicitly calls out.

## Two specific misconceptions to refuse politely

1. "Ordinary LoRA + weight knob = slider." Inference strength knobs scale an amorphous bundle; there is no guarantee the delta axis is the named attribute, monotonic, or independent of identity — which is exactly what a calibrated slider claims.
2. "Negative captions during training = concept erasure." Caption steering changes the sampling distribution of a *trained-to-data* adapter; erasure methods modify the training objective itself. Reporting the former as the latter misleads safety-sensitive users.

## Honest answer template

- "No supported slider/erasure workflow exists today." Name what *is* possible: data-distributed tendency LoRAs (with `pose-expression-features.md`-style honesty) or utility LoRAs (`utility-correction-lora.md`).
- Research lead for users who want the real method: the Concept Sliders paper above (they'd need external tooling; out of product scope — never invent in-product steps).
- Any future product change here is a support-matrix-level event; until then this stays boundary doc.

## Sources

- Registered paper lead: https://arxiv.org/abs/2311.12092 (source registry entry `concept-sliders-paper`, status verified-title-via-arxiv-api, Stage 1 note: research lead only, not product support).
- Staging artifacts: `01_训练器能力盘点/training-direction-taxonomy.md` (slider + erasure rows + base-weight note), `support-matrix.json` (`unsupportedSpecializedObjectives` fields).
- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` NETWORK_OPTION_BASEWEIGHT block (what the field actually does).

## Boundaries

- Never write a "slider tutorial" for this product even if users insist on interpreting `base_weights` that way — document the feature per contract.
- Safety/erasure requests (e.g., removing a person's likeness) deserve the honest boundary + platform-level tooling pointer, not a mock-workflow.
- If Stage 3 template work ever surfaces a base-weight-driven TOML, it must be described as rebasing experiment config, never as a slider artifact.

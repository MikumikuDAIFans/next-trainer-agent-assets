# Utility / correction / quality LoRAs (generic objective, no dedicated machinery)

- Version: `2026-08-30`
- Scope: "detail boost", "hands fix", "lighting corrector", "line-art cleaner" and similar correction/enhancement LoRAs — what the product actually provides (ordinary LoRA + data design, plus base-weight options that are NOT correction-specific) and how to keep claims honest.
- Evidence status: L1 project contract (taxonomy row "generic utility LoRA"; `enable_base_weight`/`base_weights` semantics from schema block NETWORK_OPTION_BASEWEIGHT); effectiveness expectations are domain observation; no GPU-measured claims.
- Aliases / 检索关键词: 修正, 增强, 细节, 质量, utility, detail, quality, hands fix, 修手, base weight, 差异炼丹

## Support framing (L1)

- Taxonomy: 修正/增强/细节/质量 LoRA = trainable with standard LoRA data design, **no dedicated loss or page** (`training-direction-taxonomy.md`). Determinants: 对照数据、过拟合、可解释评测.
- Related schema surface: `enable_base_weight` + `base_weights` (network option block) use existing adapter weights as a training baseline ("差异炼丹"/diffusion-style rebasing). This is a weight-baseline feature, not a correction objective — it does not add paired losses or quality scoring (same reasoning the taxonomy applies to sliders).

## Data design for a "fix" LoRA (observation-level)

1. A correction LoRA implicitly defines a contrast: "broken" vs "fixed" regions/renders. The contrast must exist in the training distribution — curated positive-only "good hands" images teach *a hand style*, not *repair*.
2. Narrow trigger + conservative application: utility LoRAs mostly mask/weight at inference; document the intended strength band on *your* checkpoints (measured by you), because no numeric calibration exists in this KB.
3. Overfit watch: small curated sets converge fast into stylization; the formal curve guide's over/underfit reads apply verbatim (`training/curve-reading-guide.md`).
4. Pair with the base's existing competence: if base anatomy is weak, report "tendency improved", not "hands fixed".

## Evaluation protocol

- Fixed prompt battery including the historical failure prompts (the ones that motivated the fix) plus neutral controls; compare base vs base+LoRA at several strengths; keep the artifact only if failure-rate improvement is visible on *unseen* prompts.

## Sources

- Staging artifacts: `training-direction-taxonomy.md` (utility row; slider note re base-weight semantics), `support-matrix.json` SDXL/SD-LoRA entries (feature surface).
- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` NETWORK_OPTION_BASEWEIGHT block (semantics reference).

## Boundaries

- No product feature computes "quality"; anything claiming automatic correction is out of scope.
- `enable_base_weight` ≠ slider/erasure/correction mechanism (taxonomy note; see `slider-erasure-boundaries.md` for the same misuse pattern).
- Effect claims are per-user-run observations; this KB stores method, not results you didn't measure.

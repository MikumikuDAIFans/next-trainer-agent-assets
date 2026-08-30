# Clothing / outfit / accessory direction (data objective)

- Version: `2026-08-30`
- Scope: garments, outfits and accessories as a data/supervision objective; identity↔garment disentangling, category-caption token design, occlusion/viewpoint coverage, and the "outfit on my character" combination question.
- Evidence status: L1 project contract for availability (Anima character preset text names 服装; DreamBooth subject interface covers personalization); disentangling practice is domain observation; no GPU-measured claims.
- Aliases / 检索关键词: 服装, 套装, 配饰, clothing, outfit, dress, uniform, 换装, 服饰

## Support framing (L1)

- Standard dataset objective on all LoRA pages; explicitly within the shipped Anima character preset scope ("单角色、服装、道具"), and the taxonomy class row: 服装/套装/配饰 — determinants 身份与服装解耦、caption token、遮挡和视角 (`training-direction-taxonomy.md`). No clothing-specific page/adapter exists: "outfit LoRA" is ordinary LoRA training shaped by dataset design.

## Disentangling identity and garment (the core decision)

Decide first what the LoRA should learn:

1. **Garment-only** (want it on any character): dataset must vary the *wearer* (different subjects/poses/backgrounds) while the garment stays constant; caption wearer attributes out. Training one person in one dress learns "person+dress+scene" as one concept — the dominant clothing-LoRA failure.
2. **Outfit-on-my-character**: train as part of the character's dataset with outfit captions, or combine two LoRAs at inference with honest expectations (`multi-concept-training.md` — combination is not a trained guarantee).
3. **Category generalization** ("this style of jacket"): broaden by garment examples, and pick caption granularity consciously — `black leather jacket` vs separate `jacket` token changes what composes later.

## Coverage rules (observation-level)

- Viewpoints incl. back/side/detail shots; flat-lay images teach shape but bake "on hanger" context — mix worn/flat only with caption awareness.
- Occlusion states (arms covering garment, seated drapes) prevent "must be fully visible" behavior.
- Material-lighting variation per `object-product-concept.md` rules for shiny/sheer fabrics.
- Pair with pose coverage only if pose independence is claimed; otherwise caption poses out.

## Evaluation protocol

- Garment-only checks: unseen wearer prompt (identity tokens from the base or another LoRA), unseen pose, unseen background; watch garment-detail smearing (coverage gap) and identity leakage (varied-wearer gap).
- Trigger/caption conventions follow `../datasets/caption-tag-trigger-strategy.md` (batch 3) once frozen; interim, apply the formal Civitai doc's verbatim-trigger rule (`workflows/civitai-model-to-lora.md`).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `config/presets/anima-lora-character-automagic.toml` (scope text), `mikazuki/schema/lora-master.ts` (ordinary adapter surface).
- Staging artifacts: `training-direction-taxonomy.md` clothing row; support-matrix availability entries.

## Boundaries

- No measured clothing-specific parameters exist in staging evidence; page presets + sweep discipline apply.
- Physically-correct drape/occlusion quality claims depend on base model capability; do not promise cloth simulation behavior from small LoRA sets.
- Brand designs/costume IP follow the same user-side rights responsibility as product work.

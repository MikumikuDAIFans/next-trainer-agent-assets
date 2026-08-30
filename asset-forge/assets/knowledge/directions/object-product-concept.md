# Object / product / prop direction (data objective)

- Version: `2026-08-30`
- Scope: single objects, props, products and small ensembles as a data/supervision objective; viewpoint/scale/background coverage rules, material and brand/IP boundaries, and routing when the object is really a "character with eyes".
- Evidence status: L1 project contract for availability (Anima character preset text explicitly includes props/道具); coverage rules are domain practice marked as observation; no GPU-measured claims.
- Aliases / 检索关键词: 物体, 道具, 产品, object, product, prop, 视角, 材质, 品牌

## Support framing (L1)

- Standard dataset objective on all LoRA pages; the Anima character preset's own description ("适合单角色、服装、道具等常规角色 LoRA") places props inside the character-shaped workflow, and the taxonomy records 单物体/道具/产品 with determinants: 视角、尺度、背景、材质、品牌/版权边界 (`training-direction-taxonomy.md`).
- For high-fidelity identity-style objects (a specific product SKU), DreamBooth (`sd-dreambooth-finetune-guide.md`) is the recorded product surface for subject personalization on SD 1.x/2.x — the same data logic applies there.

## Coverage rules that decide product LoRAs (observation-level)

1. **Viewpoint hemisphere, not a hero shot**: front/¾/side/top/bottom and open/closed states; a product LoRA trained on one angle is a sticker, not an object model.
2. **Scale context variation**: isolated on neutral ground *and* in-hand *and* in-scene, or the LoRA learns "object = floating on white".
3. **Material/lighting interaction**: glossy/transparent materials need lighting variation; bake-in speculars get pasted everywhere otherwise.
4. **Background/caption hygiene**: caption the background unless background is part of the product identity; keep the trigger token reserved (same convention logic as `character-identity.md`).
5. **Text/logos**: legible text/logo reproduction is unreliable from small sets; treat exact-logo fidelity as out of scope for LoRA and plan compositing instead — say this early rather than after training.

## Routing decisions

- Object with character semantics (plush mascot, robot character)? Use `character-identity.md` discipline plus the viewpoint rules here.
- Clothing on a person? `clothing-accessory.md`.
- Whole scene/environment? `scene-domain-migration.md`.

## Evaluation protocol

- Unseen angle prompt + unseen background prompt + "object next to other object" prompt; failures map to coverage gaps in the data, not adapter capacity (raise coverage before dim — same evidence-first ordering as the formal SDXL heuristic doc).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `config/presets/anima-lora-character-automagic.toml` (props coverage wording), `mikazuki/schema/dreambooth.ts`.
- Staging artifacts: `training-direction-taxonomy.md` object row; support-matrix entries for availability.

## Boundaries

- Brand/IP/likeness rights on product imagery are the user's responsibility; no scraping guidance here.
- Exact text/logo reproduction: declare unreliable; do not tune LoRAs endlessly chasing typography.
- No object-specific measured parameter table exists in this evidence set; use page presets + sweep discipline.

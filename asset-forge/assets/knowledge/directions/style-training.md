# Style / visual-look direction (data objective, all LoRA pages)

- Version: `2026-08-30`
- Scope: art-style, lighting/coloring/texture ("画风/光影/质感") as a data/supervision objective across all LoRA pages; the style-vs-content decoupling decision, the lighting sub-family, and evaluation without image-quality proof.
- Evidence status: L1 project contract for availability/preset wording (Anima style preset names lighting/coloring/composition explicitly); decoupling practice is domain-level observation; no GPU-measured effect claims.
- Aliases / 检索关键词: 画风, 风格, style, 光影, 上色, 质感, lighting, coloring, 领域风格

## Support framing (L1)

- Style training is a standard dataset objective on every end-to-end LoRA page. Anima ships a style preset; its documented scope covers "art style, coloring, lighting, composition, and texture" (`config/presets/anima-lora-style-automagic.toml`, `docs/anima-lora-presets.md`) — this is the product naming the lighting/color sub-family as in-scope for style work.
- Other pages carry no style-specific mode; treat their style capability as the same standard objective under each page's support level.

## The one hard design decision: what counts as "the style"

Style LoRAs leak into whatever co-varies with the target look. Consciously decide, per caption token:

1. **Keep in style**: the rendering signature you want (line weight, palette, lighting character, texture brushwork).
2. **Caption out (controllable)**: subjects, outfits, compositions you want the LoRA to accept any of — uncaptioned they get baked into "the style".
3. **Diversity floor**: many subjects × few looks beats one subject × many images, or the LoRA learns that subject, not the style (taxonomy determinant: 风格多样性 & 内容与风格解耦).
4. **Base-model bias**: a strong base aesthetic blends into the result; SDXL-cohort expectations do not transfer (`../model-families/sdxl-derived-cohorts.md`).

## Lighting/coloring/texture as a sub-family

The Anima style preset's own description authorizes treating 光影/上色/质感 as style work on any page (mechanics identical; only the preset text names them). Practical notes: exposure/color-graded datasets need consistent color-space handling — validate previews on fixed prompts; do not chase "HDR feel" beyond what data supports.

## Evaluation protocol (non-causal)

- Fixed-prompt pairs: style prompt vs neutral prompt on base and LoRA side by side; identity-bleed check by prompting a well-known subject — if subject features shift with your style weight, style entangles content.
- Curve/preview discipline follows formal baseline docs (`training/curve-reading-guide.md`); style convergence has no universal step signature in this evidence set.

## Parameter claims

Values live in page guides (shipped preset values) and each page's parameter-baseline doc with its own evidence tag; Anima style-specific real-run numbers do not exist in staging evidence — the two real-run baselines are character runs. Never transplant them as "style numbers".

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `config/presets/anima-lora-style-automagic.toml`, `docs/anima-lora-presets.md`.
- Staging artifacts: `training-direction-taxonomy.md` (style + lighting rows), support-matrix `specializedDirections`.
- Formal knowledge: `model-families/sdxl-lora-parameter-baseline.md` (heuristic box, cited with its heuristic tag when used).

## Boundaries

- Style LoRA ≠ control mechanism: composition locking is pose/composition work (`pose-expression-features.md`), not style.
- Living artists' distinctive style raises authorship/copyright sensitivities; the KB discusses technique and dataset construction only, and never frames imitation requests as endorsed.
- No measured style-strength calibration exists; do not attach numeric weight promises.

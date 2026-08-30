# Resolution & bucket strategy (arb-bucket contract per family)

- Version: `2026-08-30`
- Scope: the resolution/bucket field contract (shared + family-specific), arithmetic behavior of arb buckets, and per-family starting resolutions with their exact evidence tags.
- Evidence status: L1 project contract (`shared.ts` DATASET_SETTINGS; `flux-lora.ts` family block; shipped presets/templates for starting values).
- Aliases / 检索关键词: 分辨率, resolution, bucket, arb bucket, bucket_reso_steps, aspect, 长宽比, 分桶, 1024, 768, 512

## Field contract (L1)

| Field | Default | Contract notes |
|---|---|---|
| `resolution` | `"512,512"` (shared) | string `W,H`; multiples of 64; non-square allowed |
| `enable_bucket` | true | arb buckets across aspect ratios |
| `min_bucket_reso` / `max_bucket_reso` | 256 / 1024 | bucket clamp range |
| `bucket_reso_steps` | 64 | SDXL may use 32; <32 fails on SDXL (schema note) |
| `bucket_no_upscale` | true | images never upscaled into larger buckets |

The shared default string `"512,512"` is *the field default*, not a family recommendation — a known silent-inheritance trap when reusing configs across pages.

## Family starting resolutions (evidence-tagged, do not silently port)

| Family | Value used in audited artifacts | Tag |
|---|---|---|
| SD 1.x | 512-class (shared default matches the family's native class) | schema default |
| SDXL | `"1024,1024"` | shipped `sdxl-lora-conservative.toml` + SDXL path rules recognize family |
| Anima | 1024-class | shipped Anima presets/preview contract (`docs/anima-training.md` preview at 1024) |
| Flux | `"768,768"` | `flux-lora.ts` schema default; bucket step kept 64 |
| Krea 2 | `"1024,1024"` | shipped `krea2-lora.toml` preset |

## Arithmetic that matters (contract behavior)

- Buckets are aspect-preserving cells on the step grid within [min,max]; resolution sets the *area class* — prompts/inference still run their own size.
- `bucket_no_upscale=true`: a 300×300 photo trains in a ~256-class bucket; it does **not** become 1024 detail. Upscale sources upstream if detail is the goal — but that's data preparation, outside the product.
- Mixed collections: bucket distribution skew (most images one aspect) silently reduces effective diversity — check the bucket report the engine prints (engine log surface; read it, it lists per-bucket counts).
- SDXL step-32 is allowed by the schema note but stays 64 in the shipped heuristic template — treat 32 as an experiment to record, not default advice.

## Practical failure modes (contract-derived)

1. Reusing an SD1.5 config (512) on SDXL → identity learns soft; fix is explicit 1024-class, not more steps.
2. Portrait-heavy dataset with square defaults → wasted buckets; resolution doesn't need to be square.
3. Tiny images into high max_bucket_reso → nothing bad, they simply don't populate big buckets.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts`, `mikazuki/schema/flux-lora.ts`, `config/presets/krea2-lora.toml`, `agent-assets templates` (`sdxl-lora-conservative.toml` in the formal asset set).
- Formal knowledge: `parameters/batch-vram.md` (heuristic VRAM/resolution interaction; cited with its heuristic tag).

## Boundaries

- No measured resolution-vs-quality tables exist in staging evidence; family starting values are shipped-contract values only.
- Supersampling/latent-space math is engine-internal; this KB stays at field-contract level.
- Preview resolution follows each family's preview contract (see `../training/preview-sampling-evaluation.md`), not silently the training resolution number.

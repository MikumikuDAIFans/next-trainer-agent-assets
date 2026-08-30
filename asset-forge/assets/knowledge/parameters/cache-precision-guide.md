# Cache & precision guide (defaults, hard conflicts, VRAM levers)

- Version: `2026-08-30`
- Scope: the precision/caching switchboard as shipped — defaults per family, the exact frontend-validated conflicts, invalidation discipline, and which switches are memory levers rather than quality knobs.
- Evidence status: L1 project contract (`shared.ts` PRECISION_CACHE_BATCH + defaults, `flux-lora.ts`, shipped presets, `params.ts` conflict diagnostics).
- Aliases / 检索关键词: cache, 缓存, fp8, bf16, fp16, mixed_precision, cache_latents, cache_text_encoder, lowram, save_precision, 显存

## Precision surface (L1)

| Field | Default | Notes |
|---|---|---|
| `mixed_precision` | `bf16` | union `no|fp16|bf16`; schema note: RTX30+ may use bf16 |
| `full_fp16` / `full_bf16` | off | full-precision-mode switches; `full_bf16` documented SDXL-only in the finetune block |
| `no_half_vae` | off | VAE stays half by default |
| `fp8_base` | `true` on Flux page | Flux memory path default-on (do not "clean up" blindly); page-family specific |
| `fp8_scaled` | used by shipped Krea 2 preset | paired with bf16 mixed precision there |
| `save_precision` | `fp16` | `fp16|float|bf16`; Krea 2 preset ships `bf16` |
| `lowram` | false | loads U-Net/TE/VAE directly into VRAM — an *inverse* lever: it commits VRAM upfront |

## Cache surface (L1)

| Field | Default | Contract note |
|---|---|---|
| `cache_latents` | true | VAE outputs cached in-session |
| `cache_latents_to_disk` | true | persisted across runs |
| `cache_text_encoder_outputs` | unset | schema note: **requires shuffle_caption off** |
| `cache_text_encoder_outputs_to_disk` | unset | persisted variant; Flux page ships TE-cache default-on |

## Hard conflicts enforced by the frontend (L1 — `params.ts`)

These produce hard errors (not warnings) — knowledge answers should treat them as contract:

1. `cache_text_encoder_outputs` × `shuffle_caption`
2. `cache_latents` × `color_aug`
3. `cache_latents` × `random_crop`
4. `noise_offset` × `multires_noise_iterations`

Consequence for advice: enabling augmentation-style options on a cached pipeline is a *blocked* combination; users hitting it should switch strategy (drop cache or drop augmentation), not hunt for flags to force through.

## Invalidation discipline (operational practice)

Cached latents/TE outputs freeze the dataset's encoded form: after editing images, captions-that-change-tokenization-impact, or resolution/bucket settings, cached encodings are stale. Practical rule (mark operational common sense, engine-version-dependent): re-run with caches disabled once after dataset edits, or clear on-disk cache artifacts before trusting comparisons. State it as hygiene; the engine's cache-key behavior is engine-internal, unverified here.

## Memory-lever ordering (pointer)

For OOM laddering see `../errors/oom-performance-playbook.md` (caches → precision → batch/accum → optimizer variants → dim). This doc covers *what the switches mean*; the playbook covers *order of operations*.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (PRECISION_CACHE_BATCH, LOG/caches), `mikazuki/schema/flux-lora.ts` (fp8_base/TE-cache defaults), `config/presets/krea2-lora.toml`, `frontend/src/training/params.ts` (conflict diagnostics).
- Staging artifact: page guides for Flux/Krea (`../model-families/*`).

## Boundaries

- No quality-equivalence claims between fp8/bf16/fp16 paths exist in staging evidence — precision switches are memory contracts here, nothing more.
- `save_precision` affects artifact size/compatibility, not training dynamics; don't bundle it with precision-mode advice.
- Cache-file locations/format are engine internals; the KB documents behavior, not file surgery.

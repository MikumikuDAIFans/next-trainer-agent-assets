# FLUX LoRA workflow guide (page `flux-lora`)

- Version: `2026-08-30`
- Scope: workflow for FLUX LoRA on the dedicated Flux page (`model_train_type = flux-lora`, kohya `flux_train_network.py`). Covers the four-asset requirement, schema defaults that differ from SD pages, FP8/caching behavior, and available adapters.
- Evidence status: L1 project contract (schema `flux-lora.ts`, support matrix entry `flux-lora`). No shipped Flux preset TOML and no measured local Flux run exist in the audited evidence set.
- Aliases / 检索关键词: flux, flux1-dev, flux-lora, ae, clip_l, t5xxl, fp8, sigmoid, timestep sampling, chroma sibling

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `flux-lora` (train type fixed/disabled field) | `mikazuki/schema/flux-lora.ts` |
| Backend | `./scripts/dev/flux_train_network.py` | support-matrix `flux-lora` |
| Network modules | `networks.lora_flux` (default), `networks.oft_flux`, `lycoris.kohya` | `flux-lora.ts:52` |
| Adapters | Flux-native LoRA and OFT via dedicated flux modules; LoCon/LoHa/LoKr/IA3/GLoRA/Diag-OFT/BOFT via LyCORIS | `flux-lora.ts:52`; support-matrix `adapterAlgorithms` |
| Full finetune | backend exists but not exposed in workbench → do not treat as available | support-matrix `flux-finetune-backend-hidden`; see `hidden-and-unsupported-boundaries.md` |

## Four required assets (L1 schema defaults show the expected file set)

| Field | Role |
|---|---|
| `pretrained_model_name_or_path` | Flux DiT (default example `flux1-dev-fp8.safetensors`) |
| `ae` | auto-encoder |
| `clip_l` | CLIP-L text encoder |
| `t5xxl` | T5-XXL text encoder (default example fp8 quantized) |

All four must point at real files; "works with one model path like SD" is false for this page.

## Defaults that differ from SD pages (L1)

- Resolution default `"768,768"`, `bucket_reso_steps = 64` with the schema note that FLUX needs >64 steps semantics — keep bucket enabled.
- Diffusion-objective knobs exposed directly: `timestep_sampling = sigmoid`, `sigmoid_scale = 1.0`, `discrete_flow_shift = 1.0`, `guidance_scale = 1.0`.
- FP8 memory path is default-on: `fp8_base = true` (+ optional `fp8_base_unet`). Turning FP8 off raises VRAM sharply — do not "clean up" this flag blindly.
- `cache_text_encoder_outputs = true` and cached to disk by default; the schema notes caching requires disabling `shuffle_caption`.
- Network defaults are unusual on purpose: `network_dim = 2`, `network_alpha = 16` — Flux community practice commonly runs small dim with large alpha; the shipped schema defaults reflect that shape. Do not "fix" them to SD-style 32/32 without your own evidence.
- `network_dropout` is incompatible with LyCORIS (use the LyCORIS-internal dropout) — schema comment.

## Workflow checklist

1. Verify all four asset paths; confirm whether your DiT is already FP8-quantized before changing `fp8_base`.
2. Dataset around 768-class with buckets; caption discipline per `../datasets/` guidance; Flux token length settings exist (`t5xxl_max_token_length` optional).
3. Start from the shipped schema defaults (small dim / alpha 16); there is **no shipped Flux preset TOML and no measured Flux parameter table in this project's audited evidence** — LR/step recommendations are unknown-here; sweep and record per the formal sweep discipline.
4. Preview/eval: same fixed-prompt discipline as other families; Flux-specific sample prompts are not pinned by schema defaults.
5. Chroma bases share this page via `model_type = chroma` — see `chroma-flux-page-variant.md`.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/flux-lora.ts`, `mikazuki/app/api.py:162`.
- Frozen support matrix entry `flux-lora` (staging artifact `01_训练器能力盘点/support-matrix.json`).
- Upstream method references: LoRA paper https://arxiv.org/abs/2106.09685 ; FLUX official model family https://github.com/black-forest-labs/flux (architecture context only, not parameter evidence).

## Boundaries

- No measured Flux LR/step/VRAM numbers exist in the audited set: answer "unknown in-project, sweep with recorded config" instead of importing third-party numbers as facts.
- Flux full finetune, calibrated sliders, concept erasure: not product capability (see `hidden-and-unsupported-boundaries.md`, `../directions/slider-erasure-boundaries.md`).
- FP8 quantized DiT + `fp8_base` interactions are contract defaults; do not claim quality equivalence either way — no measurement here.

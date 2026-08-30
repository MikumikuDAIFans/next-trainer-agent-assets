# Krea 2 LoRA guide (Musubi engine, page `krea2-lora`)

- Version: `2026-08-30`
- Scope: workflow for Krea 2 LoRA training on the Musubi-backend page (`model_train_type = krea2-lora`), including conditional-support gates, required assets, shipped official-recommendation preset values, and engine limits.
- Evidence status: L1 project contract (schema `krea2-lora.ts`, musubi adapter `adapter.py:12`, route branch `api.py:774-838`, shipped preset `krea2-lora.toml`, docs `musubi-tuner-engine-plan.md`, `krea2-linux-multigpu.md`). No measured local Krea run exists in the audited evidence set.
- Aliases / 检索关键词: krea, krea2, krea 2, musubi, musubi-tuner, qwen3-vl, fp8 scaled, 官方推荐, 条件支持

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Page / train type | `krea2-lora` | `mikazuki/schema/krea2-lora.ts:3-7` |
| Engine | Musubi backend `mikazuki.musubi_backend` (separate runtime, not kohya) | `mikazuki/musubi_backend/adapter.py:12`, `mikazuki/app/api.py:774-838` |
| Support level | conditional: Musubi feature enabled + optional runtime installed/ready + preflight passes | support-matrix `krea2-lora` prerequisites |
| Adapters | LoRA only; non-LoRA adapters and any full-finetune page are rejected | support-matrix `unsupportedSpecializedObjectives` |
| Assets | DiT + VAE + Qwen3-VL text encoder | support-matrix prerequisites; `config_import.py` Musubi path rules match `qwen3-vl` |

## Contract fields pinned by the Krea 2 page schema (L1 — `krea2-lora.ts`, read 2026-08-30)

- Asset fields are family-specific: `dit` (RAW base) + `vae` (Qwen-Image VAE) + `text_encoder` (Qwen3-VL-4B); optional `turbo_dit` preview accelerator (mutually exclusive with `blocks_to_swap`; training itself stays on RAW).
- **fp8 pair is pinned**: `fp8_base` and `fp8_scaled` must both stay on — the schema warns "only one enabled will not train" (训不起来). Never advise toggling one alone.
- `mixed_precision` union is **bf16 only** on this page.
- Optimizer union is restricted here: `AdamW | AdamW8bit | Adafactor` (default AdamW8bit) — no Prodigy/DAdapt surface on the Krea page.
- Dataset block diverges from the shared defaults: `resolution` default `"1024,1024"` with a **multiple-of-16** note, and `bucket_no_upscale` default **false** here (shared block defaults it true) — do not port shared-block assumptions onto this page.
- Preview defaults ship family-shaped: 1024×1024, CFG 4.5, 28 steps, seed 42, `sample_at_first` for config verification (turbo_dit auto-clamps to CFG1/8 steps at sampling).

## Shipped preset values (L1 — `config/presets/krea2-lora.toml`)

> Wording discipline (conflict register C-013): the preset's own text self-labels as "official recommendation", but no external Krea/Musubi official source has been verified in Stage 1. Until that verification lands, cite it as **project shipped preset**, never as an official fact.

- `network_dim = 32`, `network_alpha = 32`
- `resolution = "1024,1024"`, buckets on, batch 1, gradient checkpointing on
- `optimizer_type = AdamW8bit`, `learning_rate = 1e-4`, scheduler `constant`
- `mixed_precision = bf16` with `fp8_base = true`, `fp8_scaled = true`
- `max_train_epochs = 16`, `save_every_n_epochs = 2`, `save_precision = bf16`
- Flow-matching objective: `timestep_sampling = sigmoid`, `sigmoid_scale = 1.0`, `discrete_flow_shift = 1.0`
- The preset's own description records the rationale ("official recommended LoRA configuration; requires the independent musubi-tuner plugin environment") — cite it as shipped starting values, not measured guarantees.

## Workflow checklist

1. Gate first: confirm the Musubi feature flag is on and the optional runtime is installed; the page runs a preflight before submit. Preflight failure with the runtime absent is expected behavior for conditional support, not a training bug.
2. Asset set differs from every other family: Krea 2 DiT + VAE + **Qwen3-VL** text encoder (not Qwen3 of the Anima page; the import rules key on `qwen3-vl`). Placeholders in shared docs: `X:/sd-models/krea2/...`.
3. Start from the shipped preset; record any change. Epoch-based saving (every 2 epochs over 16) is the shipped cadence — keep several candidates for comparison.
4. Dataset/caption discipline is the same as other families (1024-class, trigger conventions per direction docs).
5. Validation: fixed prompts/seed previews decide; there is no measured Krea step/loss signature in this evidence set, so do not quote one.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/krea2-lora.ts`, `mikazuki/musubi_backend/adapter.py`, `mikazuki/app/api.py`, `config/presets/krea2-lora.toml`, `docs/musubi-tuner-engine-plan.md`, `docs/krea2-linux-multigpu.md`, `mikazuki/musubi_backend/settings.py`.
- Upstream engine: https://github.com/kohya-ss/musubi-tuner (official runtime documentation; pinned commit is a recorded P2 follow-up in the source registry).
- Frozen support matrix entry `krea2-lora` (staging artifact).

## Boundaries

- Conditional support wording is mandatory: no runtime → no training. Never describe Krea 2 as available on a plain install.
- LoRA-only: LoKr/OFT/LyCORIS requests for Krea 2 are contract-rejected; full finetune does not exist on this page.
- The Stage 1 Civitai batch found Krea-2-stratum public listings but no structured training parameters (`trainingDetails` null project-wide), so no community distribution backs the preset; its authority is "shipped product preset", nothing stronger.
- Multi-GPU/Linux specifics: point to `docs/krea2-linux-multigpu.md` rather than improvising — the knowledge base does not restate deployment topology claims.

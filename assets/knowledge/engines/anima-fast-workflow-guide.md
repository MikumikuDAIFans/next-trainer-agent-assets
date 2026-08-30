# Anima Fast workflow guide (page `anima-lora-fast`)

- Version: `2026-08-30`
- Scope: workflow for the Anima Fast plugin engine (`model_train_type = anima-lora-fast`), including what differs from the standard page at the contract level, shipped preset values, and the engine's hard limitations. Engine mechanics comparison lives in the formal doc `anima-fast-vs-standard.md`.
- Evidence status: L1 project contract (schema `anima-lora-fast.ts`, backend branch `api.py:741-767`, shipped presets, `docs/anima-fast.md`). Speed claims from project docs are project-claimed observations, not independently verified here.
- Aliases / 检索关键词: anima fast, 快速, anima-lora-fast, torch_compile, flash attention, adamw8bit, 插件引擎, skip_cache_check

## Contract facts (L1)

| Item | Value | Evidence |
|---|---|---|
| Train type | `anima-lora-fast` | `mikazuki/schema/anima-lora-fast.ts` |
| Engine | separate plugin runtime `mikazuki.anima_fast_backend` (own venv under `extensions/anima_lora/.venv`) | `mikazuki/app/api.py:741-767`, `docs/anima-training.md` |
| Support level | conditional: feature flag + optional runtime installed/ready + preflight pass | support-matrix `anima-fast-lora` |
| Adapter algorithms | LoRA only | support-matrix; LoKr/T-LoRA/others rejected |

## Shipped preset values (L1, importable starting points)

`config/presets/anima-fast-lora-character.toml` (and `-style`):

- `method = lora`, `network_module = networks.lora_anima`, `network_dim = 16`, `network_alpha = 16`
- `resolution = "1024,1024"`, buckets on, batch 1, gradient checkpointing on
- `optimizer_type = AdamW8bit`, `learning_rate = 1e-4` — the preset itself records why: **the Fast runtime does not support Automagic**, so the standard-page Automagic default cannot be copied here
- `mixed_precision = bf16`; all four cache switches off plus `skip_cache_check = true`
- Compile block: `torch_compile = true`, `static_token_count = 4096`, `compile_mode = blocks`, `dynamo_backend = inductor`, `attn_mode = flash`

## Workflow checklist

1. Enable the feature flag and install the Anima Fast runtime; the page preflight must pass before submit (conditional support: failure here is expected when the plugin is absent — it is not a product bug).
2. Dataset preparation is identical to the standard page (1024-class, same caption discipline).
3. Start from the shipped Fast preset; do not paste standard-page presets into the Fast page (cache/Automagic fields differ; the two engines deliberately do not share config entries — `docs/anima-training.md`).
4. Preview/step-budget expectations follow the same "validate images decide" discipline as the standard guide; the Fast engine claims speed gains at equal parameters (project-documented, e.g. the ~2.5× figure in `docs/anima-training.md` for RTX 4090) — treat as a vendor-claimed observation, not a measured guarantee in this knowledge base.
5. Pure CLI route exists (`train_anima_fast_by_toml.sh` with its own install script) — separate entry from the standard TOML runner; never mix.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/anima-lora-fast.ts`, `mikazuki/app/api.py`, `config/presets/anima-fast-lora-character.toml`, `config/presets/anima-fast-lora-style.toml`, `docs/anima-fast.md`, `docs/anima-training.md`.
- Formal knowledge baseline: `engines/anima-fast-vs-standard.md` (field ownership between engines).
- Frozen support matrix entry `anima-fast-lora` (staging artifact).

## Boundaries

- LoKr / T-LoRA / LoHa / VeRA / LoRA-FA on the Fast page are unsupported by contract — reject any request that mixes them.
- Automagic/CAME defaults from the standard page must not be ported here (runtime lacks Automagic).
- Speed numbers are vendor/project claims; do not restate them as benchmarks.
- No independent measured Fast run exists in the staging evidence set (Stage 1 collected no Fast-specific observation).

# Anima LoRA workflow guide (standard Kohya path, page `anima-lora`)

- Version: `2026-08-30`
- Scope: end-to-end workflow for the standard Anima LoRA page (`model_train_type = anima-lora`, engine = bundled kohya). Covers required assets, algorithm choices, shipped starting presets, preview settings, and step-count experience. Direction-specific dataset design lives in `../directions/`.
- Evidence status: L1 project contract (schema `sd3-lora.ts`, shipped presets, project doc `docs/anima-training.md`); experience values are project-documented observations, not causal claims.
- Aliases / 检索关键词: anima, anima-lora, 标准, kohya, automagic, qwen3, vae, t-lora, lokr, 工作流, 新手默认

## Contract facts (L1)

| Item | Value | Evidence (repository-relative) |
|---|---|---|
| Page / train type | `anima-lora` (URL slot legacy `sd3-lora`) | `mikazuki/schema/sd3-lora.ts`, `mikazuki/app/api.py:159-161` |
| Backend | `./scripts/dev/anima_train_network.py` wrapper → vendored kohya | `docs/anima-training.md` |
| Verified adapter algorithms | LoRA, LoKr (`lycoris.kohya` + `algo=lokr`), T-LoRA | support-matrix `anima-standard-lora`; see `../network-algos/lokr-guide.md`, `../network-algos/tlora-anima-guide.md` |
| Not verified (do not recommend) | LoRA-FA / VeRA / LoHa / PiSSA entries | see `../network-algos/anima-schema-only-adapters.md` |

## Required assets (L1)

Three weights plus optional T5 field per the training form:

| Field | Meaning |
|---|---|
| `pretrained_model_name_or_path` | Anima DiT (`anima-base-v1.0.safetensors`) |
| `vae` | Qwen-Image VAE (required) |
| `qwen3` | Qwen3 text model (file or directory) |
| `t5` | T5 text-encoder weights (documented form field) |

Project doc: official download helper pulls `circlestone-labs/Anima` from ModelScope into `sd-models/anima/` (docs/anima-training.md). Use placeholder paths like `X:/sd-models/anima/...` in shared configs.

## Shipped starting presets (L1 — importable, not guarantees)

`config/presets/anima-lora-character-automagic.toml` (character/outfit/prop default) and `anima-lora-style-automagic.toml` (style default):

- `network_module = networks.lora_anima`, `network_dim = 16`, `network_alpha = 16`, UNet-only
- `resolution = "1024,1024"`, buckets enabled (256–1024, step 64)
- `optimizer_type = Automagic`, `learning_rate/unet_lr = 1e-4`, `text_encoder_lr = 0`, scheduler `constant`
- `mixed_precision = bf16`, latents + text-encoder outputs cached to disk
- Rationale recorded in the preset itself: Automagic chosen so beginners do not tune LR/scheduler.

The shipped empirical template `anima-lora-conservative.toml` (dim 16 / alpha 12, CAME, lr 1e-5, cosine_with_restarts, warmup 50, preview every 2 epochs) is the conservative low-LR alternative; evidence behind it is the project's own real-run baselines (see `anima-lora-parameter-baseline.md`, `anima-character-case-v1.md` in the formal knowledge set).

## Workflow checklist

1. Place the three Anima weights; verify paths on the page.
2. Dataset at 1024-class resolution, captions per `../datasets/caption-tag-trigger-strategy.md` conventions; trigger-word design per direction doc (e.g. `../directions/character-identity.md`).
3. Pick adapter: default LoRA; LoKr or T-LoRA only after reading their guides (batch 2).
4. Start from a shipped preset; record every changed field.
5. Turn on preview (`enable_preview`): Anima sampling switches to project-documented recommended preview settings 1024×1024, CFG 4.5, 40 steps, seed 42.
6. Steps expectation (project-documented experience, L1 doc, non-causal): roughly **1000–3000 optimizer steps** often yields a usable character look at the same dataset/resolution; validate images decide, not the number.
7. Loss goes NaN with Automagic/CAME: check PyTorch ≥ 2.5, do not enable `full_bf16`/`full_fp16`, do not switch bf16→fp16 (documented backend behavior auto-reverts full half-precision for these optimizers).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/sd3-lora.ts`, `mikazuki/app/api.py`, `config/presets/anima-lora-character-automagic.toml`, `config/presets/anima-lora-style-automagic.toml`, `docs/anima-training.md`, `docs/anima-lora-presets.md`.
- Formal knowledge baseline: `model-families/anima-lora-parameter-baseline.md`, `model-families/anima-character-case-v1.md` (real local runs, migrated; referenced by filename because both live under `knowledge/model-families/` after migration).
- Frozen support matrix entry `anima-standard-lora` (staging artifact `01_训练器能力盘点/support-matrix.json`).

## Boundaries

- Preset values are shipped starting points; do not present them as optimal. Before recommending to a new dataset class the project docs themselves say to test on 100–300 representative images (`docs/anima-lora-presets.md`).
- No LoKr/T-LoRA/full-finetune presets are shipped (explicit project decision) — do not invent them here.
- The 1000–3000 step guidance is documented experience at fixed resolution with the project's own datasets; report as observation, never as a guarantee.
- Civitai is L2 observation only (see `../model-families` sibling docs + Stage 1 missingness report); no Civitai number backs any value above.

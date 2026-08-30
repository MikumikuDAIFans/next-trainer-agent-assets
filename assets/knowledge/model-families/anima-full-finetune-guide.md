# Anima full DiT finetune guide (page `anima-finetune`)

- Version: `2026-08-30`
- Scope: the first-class full-model finetune for Anima (`model_train_type = anima-finetune`, updates main DiT weights — not an adapter). Covers what the mode is, prerequisites, workflow differences from LoRA, and where knowledge is deliberately absent.
- Evidence status: L1 project contract (schema `anima-finetune.ts`, route `api.py:161`, support matrix entry `anima-full-finetune`). No shipped preset or template exists for this mode; no measured baseline exists in this project.
- Aliases / 检索关键词: anima finetune, 全量微调, anima-finetune, dit, 全参数, finetune, 组件学习率

## What this mode changes (L1)

- Backend entry: `./scripts/dev/anima_train.py` (kohya path), distinct from the LoRA wrapper `anima_train_network.py`. Evidence: support-matrix `anima-full-finetune`, `frontend/src/training/modules.ts:36`, `mikazuki/schema/anima-finetune.ts`, `mikazuki/app/api.py:161`.
- Granularity: full DiT weights are updated (per-component learning rates exposed in schema `anima-finetune.ts:50-58`). Output is a full model checkpoint, not a LoRA file.
- Consequences: adapter export does not apply; loading means replacing/merging the base model itself.

## Prerequisites (L1)

- Same three Anima assets as the LoRA page (DiT + Qwen-Image VAE + Qwen3).
- "Substantially higher VRAM/disk than LoRA" is the recorded product prerequisite — budget for a full checkpoint per save, and expect far lower batch sizes than the LoRA page.

## Workflow differences vs Anima LoRA

1. Every save writes a full checkpoint: disk usage grows as `#saves × checkpoint size`; set the save cadence deliberately (`save_every_n_epochs`-class controls exist on the page).
2. Learning rates: component-level LR fields apply to the DiT blocks themselves. This schema does not have "network_dim/alpha" — capacity knobs are irrelevant here.
3. Dataset/caption/trigger design is the same discipline as LoRA (see `../datasets/` candidates and `../directions/`), but the risk profile shifts: wider domain shifts and distribution changes are achievable, with real catastrophic-forgetting risk.
4. Validation: compare the finetuned model against the untouched base on a fixed prompt set (see `../training/preview-sampling-evaluation.md` conventions). LoRA-style "just load the adapter on the base" comparison does not apply.

## What this guide deliberately does NOT give you

- No parameter table: the project ships no finetune preset (`docs/anima-lora-presets.md` explicitly excludes full finetune presets) and no measured local finetune run exists in the evidence set. Any concrete LR/step number would be fabrication — this is an **unknown**, keep it unknown.
- No VRAM number: none is measured or documented in this project's evidence.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/anima-finetune.ts`, `mikazuki/app/api.py`, `frontend/src/training/modules.ts`, `docs/anima-lora-presets.md` (preset exclusion note).
- Frozen support matrix entry `anima-full-finetune` (staging artifact `01_训练器能力盘点/support-matrix.json`).

## Boundaries

- Do not reuse LoRA conservative numbers (dim/alpha/1e-4/1e-5 class) as finetune recommendations; granularity mismatch.
- If a future local finetune run produces real values, record them as an L2 observation doc first; only then may this guide cite concrete numbers.
- Full finetune is first-class for Anima only: never generalize this page's existence to Flux/Krea/Lumina (see `hidden-and-unsupported-boundaries.md` and the Krea 2 guide).

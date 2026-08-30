# Exposure budget: repeats × epochs × batch → steps (documented anchors only)

- Version: `2026-08-30`
- Scope: the exposure arithmetic the product actually computes from, the auto-repeat suggestion tiers, and the documented step/epoch anchors per family — kept strictly separated from "optimal exposure" claims that no audited evidence supports.
- Evidence status: L1 project contract (subdir repeat prefix, `suggest_num_repeat`, `max_train_epochs`/batch/accumulation fields; shipped preset/template values); step ranges from `docs/anima-training.md` are documented experience; everything else is your sweep's job.
- Aliases / 检索关键词: 曝光预算, steps, epochs, repeats, num repeat, max_train_epochs, 训练轮数, 步数, 提交前预算

## The arithmetic surface (L1)

- **Per-dataset repeats**: encoded in the subdir name (`10_name` ⇒ 10 repeats; see `../datasets/preparation-checklist.md`).
- **Auto-suggestion when a flat dir is rescued into `_zkz`** (`suggest_num_repeat`): ≤10 imgs → 7, 11–50 → 5, 51–100 → 3, >100 → 1. These are the *product's* suggestion tiers — useful as its own baseline, not as quality advice.
- **Run horizon**: `max_train_epochs` (LoRA/DreamBooth pages default **10**); `train_batch_size` default 1; `gradient_accumulation_steps` optional. Steps ≈ ceil(Σ(images×repeats) / (batch×accum)) × epochs — the engine prints its computed total; trust the log, not hand math.
- **Saving cadence**: `save_every_n_epochs` default 2 or `save_every_n_steps` (either suffices) — budget saving frequency *with* the horizon so intermediate checkpoints exist.

## Documented anchors by family (each with its tag — do not cross-port)

| Family | Anchor | Tag |
|---|---|---|
| Anima LoRA | ~1000–3000 steps for character-scale sets; more is usually overfit territory | documented experience, `docs/anima-training.md` |
| SDXL LoRA | shipped `sdxl-lora-conservative.toml` pins an 1800-step-scale budget | shipped template (heuristic family) |
| SDXL heuristic table | 1500–3000 steps band appears in the formal heuristic baseline doc | formal doc, marked heuristic |
| Krea 2 | epoch-mode budget: 16 epochs, save every 2 | shipped preset (`max_train_epochs=16`) |
| SD 1.5 | — no shipped table; unknown-here | — |
| Flux | — no shipped step value beyond schema default epochs; unknown-here | — |

## Budgeting discipline (KB policy, not math trivia)

1. Fix repeats + epochs + cadence **before** submit and record them in the run log; changing repeats mid-comparison silently invalidates step-wise comparisons (same step count ≠ same exposure).
2. Near-duplicate images inflate Σ(images×repeats) — dedup first (dataset checklist).
3. Compare checkpoints at equal *exposure* (steps), not equal wall-clock.
4. Reading results: `../training/checkpoint-selection.md` + formal `training/curve-reading-guide.md` (formal doc owns curve semantics; not restated).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/utils/train_utils.py` (suggest_num_repeat), `mikazuki/schema/lora-master.ts:82-85`, `mikazuki/schema/dreambooth.ts:50-54`, `mikazuki/schema/shared.ts:99-106` (save cadence), `config/presets/krea2-lora.toml`, `docs/anima-training.md`.
- Formal knowledge: `model-families/sdxl-lora-parameter-baseline.md` (heuristic), `parameters/parameter-evidence-rules.md` (evidence tagging rules).

## Boundaries

- No universal "good step count" exists in this KB — the anchors above are family/artifact specific with their tags; a number without a tag may not enter any answer.
- LR×steps interaction, scheduler horizon effects: unmeasured here; sweep-and-record per EDD.
- Repeat-tier values describe the auto-rescue path only; setting repeats manually is a separate (unconstrained) surface.

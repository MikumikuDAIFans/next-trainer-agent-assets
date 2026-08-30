# Checkpoint selection (choosing the artifact to ship)

- Version: `2026-08-30`
- Scope: using the product's save/state surface to produce comparable checkpoints, the selection protocol across them, and resume mechanics where the contract supports them.
- Evidence status: L1 project contract (save/state fields, shared save cadence block, `save_model_as`/`save_precision`); the selection protocol is project-consistent practice; curve semantics delegated to the formal guide.
- Aliases / 检索关键词: 选点, checkpoint, save_every, save_state, resume, 出图对比, 交付 artifact, 保留哪个 epoch

## Save surface (L1)

- Cadence: `save_every_n_epochs` (default 2) or `save_every_n_steps` — plan one of them *with* the exposure budget (`../parameters/exposure-budget-steps.md`) so intermediate candidates exist; saving only the endpoint forfeits the selection problem entirely.
- Format/precision: `save_model_as` default safetensors; `save_precision` default fp16 (Krea 2 preset ships bf16) — record both; downstream compatibility depends on them.
- State: `save_state` (+ matching `resume`) exists on the DreamBooth/finetune surface for continuing full runs (state ≠ model file: state carries optimizer/step context; the pairing flag is required by contract). LoRA-page interruption strategy: rerun with a longer horizon rather than assuming state-resume parity — parity is not established in project evidence (unknown-here).
- Network continuation (`network_weights` = continue-training-from-LoRA) is *progressive training*, not resume — different claim, keep words distinct.

## Selection protocol (project practice)

1. Pre-register the prompt battery + settings (from `preview-sampling-evaluation.md`) **before** training; the battery must include prompts the dataset never contained.
2. Sample the same battery, same seed, across every retained checkpoint (previews give the cheap pass; external fixed-seed runs the confirmation pass).
3. Score per direction question (identity vs controllability vs leakage), not "best-looking image": the classic trade is mid-run vs late-run — document which question each pick answers.
4. Decide on unseen-prompt performance; endpoint sentiment ("more steps = better") is the known anti-pattern the formal curve guide documents (`training/curve-reading-guide.md` — owns over/underfit signatures).
5. Record the selection matrix with the artifact (which checkpoint, why, on which prompts) — this becomes the artifact's honest metadata (`repro-publishing-workflow.md`).

## Misleading signals checklist (practice)

- Preview sampler drift (changing cfg/steps mid-run) — you're comparing settings, not checkpoints.
- One lucky sample picking the worst checkpoint — require the whole battery.
- Loss-only culling — loss bands across noise-sampling luck (formal curve guide).
- Epoch labels vs exposure: with changed repeats, "epoch 5" of run B ≠ epoch 5 of run A (`exposure-budget-steps.md` rule).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (save cadence/save_state block), `mikazuki/schema/dreambooth.ts` (resume pairing), `mikazuki/schema/lora-master.ts` (`network_weights`).
- Formal knowledge: `training/curve-reading-guide.md`.
- Product skills reference (compat surface): artifact-selection skill listed in the formal asset `compat.json`.

## Boundaries

- No numeric "pick the epoch closest to N steps" rule exists in this KB — selection is protocol + evidence, not a constant.
- Resume/state file locations and formats are engine internals; document behavior only.
- Selection conclusions from one model family do not transfer to another (base-mismatch discipline).

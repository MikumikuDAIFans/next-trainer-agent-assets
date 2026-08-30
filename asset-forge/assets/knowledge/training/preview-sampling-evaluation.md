# Preview sampling as evaluation (in-training observation instrument)

- Version: `2026-08-30`
- Scope: the preview-image contract as the product's built-in evaluation channel — fixed-prompt discipline, sampler/seed/cfg fields, prompt-file mode, the Anima documented preview contract, and what previews can/cannot prove.
- Evidence status: L1 project contract (`shared.ts` PREVIEW_IMAGE block, family presets); Anima preview values from `docs/anima-training.md`; evaluation interpretation is practice, tagged.
- Aliases / 检索关键词: 预览图, preview, sample, sample_prompts, 采样, seed, cfg, 训练中评测, prompt file

## Field contract (L1)

- Master switch `enable_preview` default **false** — the product does not evaluate for you unless enabled; enabling is the first habit of a reviewable run.
- With preview on: `randomly_choice_prompt` (default false), `prompt_file` (path; when set it **overrides** the inline options below), inline `positive_prompts` / `negative_prompts` (schema ships generic defaults: "masterpiece, best quality, 1girl, solo" vs the long bad-anatomy negative — neither is task-appropriate as-is), `sample_width/height` (512/512), `sample_cfg` (7, range 1–30), `sample_steps` (24, ≤300), `sample_seed` (2333), `sample_sampler` (15-way union, default `euler_a`), `sample_every_n_epochs` (2).
- Finetune pages keep the classic SD preview prompt syntax block (`--n/--w/--h/--l/--s/--d` per line) — different surface from the structured union above; don't mix syntaxes across pages.
- Family exception (documented): Anima ships previews at **1024×1024, CFG 4.5, 40 steps, seed 42** in the product docs' preview contract (`docs/anima-training.md`; shipped templates mirror it) — the shared 512/CFG7 defaults would silently mis-preview Anima if inherited unedited.

## Previews as an evaluation instrument (practice rules)

1. **Fixed battery, fixed seed.** The point of `sample_seed` is cross-checkpoint comparability: one prompt per question (identity / style / unseen-composition / negative-control), held constant across the whole run.
2. Random prompt cycling (`randomly_choice_prompt`) is variety, not evaluation — turn it off for review runs.
3. Prompt-file mode is the reproducible path for long batteries (file in version control alongside the run config); inline prompts drift.
4. Previews at training resolution ≠ inference behavior at other sizes/aspects — treat off-contract sampling as a separate test.
5. Never derive "converged" from loss alone; the formal `training/curve-reading-guide.md` pairs curve reading with sample review (it owns that method; not restated).

## What previews cannot prove

- No statistical claim: N samples with one seed are anecdotes with fixed noise; a selection decision needs the multi-checkpoint comparison protocol (`../training/checkpoint-selection.md`).
- Preview sampler/cfg/scheduler are *observation settings*; reporting them as inference recommendations is a category error — copy them into test scripts explicitly.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (PREVIEW_IMAGE block), `mikazuki/schema/dreambooth.ts` (classic syntax block), `docs/anima-training.md`, shipped templates (`anima-lora-conservative.toml` preview block in the formal asset set).
- Formal knowledge: `training/curve-reading-guide.md`.

## Boundaries

- Preview image files are runtime artifacts — this KB stores contracts, never images (evidence-governance rule).
- Sampler quality claims between the 15 options: unmeasured here; default `euler_a` is a contract default only.
- Anima's 1024/4.5/40/42 is *documented product guidance*, not a universal preview recipe for other families.

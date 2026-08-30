# Diffusers DreamBooth and prior-preservation concepts

- Version: `2026-08-30`
- Scope: use the public Diffusers DreamBooth guide to clarify prior-preservation terminology and compare it with the current Next Trainer DreamBooth contract.
- Evidence status: L1 Hugging Face documentation retrieved HTTP 200 on 2026-08-30 plus L1 project DreamBooth schema; no effectiveness claim.
- Aliases / 检索关键词: DreamBooth, prior preservation, prior loss, 类图, regularization, Diffusers

## What transfers safely

The upstream guide can explain why instance images and optional class/prior images are separate data roles, and why prior-loss weighting is a dataset/objective decision rather than a universal LoRA knob. This reinforces the current knowledge rule: `reg_data_dir` and `prior_loss_weight` must be interpreted through the DreamBooth page contract.

## What does not transfer automatically

- Diffusers argument names are not Next Trainer schema keys.
- An upstream recommended step count or learning rate is not a project default.
- A Diffusers checkpoint workflow does not prove the current page can emit a compatible artifact.

Use the current project schema and validator for `sd-dreambooth`; retain paths as import-time user values and never embed a machine path in a candidate template.

## Sources

- Hugging Face Diffusers DreamBooth guide: https://huggingface.co/docs/diffusers/en/training/dreambooth
- Current DreamBooth candidate: `../model-families/sd-dreambooth-finetune-guide.md`
- Regularization boundary: `../datasets/regularization-images.md`

## Boundaries

- This is conceptual cross-tool evidence only; it does not expand support to SDXL finetune or other pages.
- No claim is made that prior preservation improves every objective or adapter type.
- Unknown project values remain unknown.

## Eval

- Question: “Diffusers 的 prior-preservation 参数能否直接填入 LoRA 模板？”
- Expected answer: no; the current project only gives those fields meaning in the DreamBooth/full-model contract unless new evidence is added.

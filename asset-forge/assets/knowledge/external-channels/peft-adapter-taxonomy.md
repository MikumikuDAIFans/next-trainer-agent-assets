# PEFT adapter taxonomy as a cross-tool reference

- Version: `2026-08-30`
- Scope: use Hugging Face PEFT terminology to distinguish adapter families from training objectives and Next Trainer page contracts.
- Evidence status: L1 public PEFT documentation/repository channel; no direct product compatibility claim.
- Aliases / 检索关键词: PEFT, adapter taxonomy, LoRA, adapter family, 网络算法, 训练目标

## Reusable distinction

PEFT names describe how trainable parameters are inserted or constrained. They do not describe whether the dataset objective is character, style, clothing, pose, or concept. Keep the axes separate in knowledge and template reviews.

## Product mapping rule

Map a PEFT algorithm to a Next Trainer template only when the target page schema, trainer mapping, and validator accept the exact module and fields. A PEFT library example is knowledge context, not an importable TOML.

## Sources

- Hugging Face PEFT docs: https://huggingface.co/docs/peft/en/index
- PEFT repository: https://github.com/huggingface/peft
- Current algorithm matrix: `../../01_训练器能力盘点/support-matrix.json`

## Boundaries

- No cross-library checkpoint compatibility claim.
- No recommendation that one adapter family is universally better.

## Eval

- Question: “PEFT 支持某 adapter 是否代表 Next Trainer 页面支持它？”
- Expected answer: no; current product contract and validator are required.

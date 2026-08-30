# Concept Sliders research channel and product boundary

- Version: `2026-08-30`
- Scope: record the Concept Sliders paper as a research source for slider/erasure objectives without presenting it as a current Next Trainer workflow.
- Evidence status: L1 arXiv title/abstract retrieval HTTP 200 (`arXiv:2311.12092`); research evidence only.
- Aliases / 检索关键词: Concept Sliders, slider LoRA, concept control, erasure, 概念滑块, 概念擦除

## What the paper can support

The paper supports a research-level explanation that a slider adapter is trained around a controlled concept direction and evaluated for controllability. This is useful for framing questions about positive/negative prompts, paired data, and suppression objectives.

## What it cannot support here

The current Next Trainer support matrix does not expose a calibrated slider or concept-erasure loss. A standard LoRA page and a paper-level slider method are not interchangeable. Keep slider/erasure as a boundary document until route, schema, trainer, validator, and evaluation evidence exist.

## Sources

- Concept Sliders, arXiv:2311.12092: https://arxiv.org/abs/2311.12092
- Current boundary guide: `../directions/slider-erasure-boundaries.md`
- Frozen support matrix: `../../01_训练器能力盘点/support-matrix.json`

## Boundaries

- No slider template is added.
- No claim is made that ordinary LoRA training reproduces slider controllability.
- Research papers provide method context, not product import proof.

## Eval

- Question: “Concept Sliders 论文是否证明当前 Next Trainer 支持 slider？”
- Expected answer: no; current product support remains unsupported/boundary until a complete implementation contract exists.

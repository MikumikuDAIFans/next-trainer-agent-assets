# Alternative training tools as observational evidence

- Version: `2026-08-30`
- Scope: compare AI-Toolkit and SimpleTuner as discovery channels for dataset, evaluation, and reproducibility practices without claiming Next Trainer compatibility.
- Evidence status: L1 public repository retrieval (`ai-toolkit` head `be995185f598c83abb990a088e9f634c4d36eb46`; `SimpleTuner` head `b1463e977fde4b88c7c7f1c54bd591b67ec4dcba`); practices remain cross-tool observations.
- Aliases / 检索关键词: AI-Toolkit, SimpleTuner, alternative trainer, 复现, 评测, 数据集实践, 工具比较

## Why keep these channels

Alternative tools can reveal useful vocabulary for dataset manifests, caption review, checkpoint selection, and evaluation prompts. They help identify questions that the Next Trainer knowledge base should answer, but they do not define the current product's routes or fields.

## Safe extraction pattern

- Extract a short practice statement, not a copied tutorial or long model card.
- Label it L1 external context or L3 experiment suggestion.
- Cross-check whether the current product has an equivalent field or workflow.
- Keep incompatible features in a comparison/boundary document instead of a template.

## Sources

- ostris AI-Toolkit, observed revision `be995185f598c83abb990a088e9f634c4d36eb46`: https://github.com/ostris/ai-toolkit
- bghira SimpleTuner, observed revision `b1463e977fde4b88c7c7f1c54bd591b67ec4dcba`: https://github.com/bghira/SimpleTuner
- Existing evaluation guide: `../training/preview-sampling-evaluation.md`

## Boundaries

- No external tool configuration is an importable Next Trainer template.
- No claim is made about relative quality, speed, or VRAM.
- Popularity and example frequency are not technical validity evidence.

## Eval

- Question: “SimpleTuner 的 dataset manifest 能否直接放进 Next Trainer？”
- Expected answer: no; reuse only the underlying review idea after mapping it to current product fields and validators.

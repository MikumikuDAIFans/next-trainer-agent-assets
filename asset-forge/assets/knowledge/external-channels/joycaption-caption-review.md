# JoyCaption and caption-review channel

- Version: `2026-08-30`
- Scope: use JoyCaption as an external source for caption generation/review questions while preserving the current dataset and caption contract.
- Evidence status: L1 public repository retrieval HTTP 200; observed commit `b3d970ee05d4c24fd5d74b76d582ea3bfb2892eb9c15bc76656a8f67ae34b6a0`.
- Aliases / 检索关键词: JoyCaption, caption, caption review, 自动标注, 标签清洗, 触发词

## Reusable information

Captioning tools can help structure a review checklist: verify subject identity terms, remove leakage from filenames or artist names, preserve intended trigger words, and inspect whether captions describe unwanted attributes. These are dataset-quality practices, not a guarantee of a particular model outcome.

## Mapping to Next Trainer

Next Trainer still requires its own image/caption pairing, caption extension, shuffle/keep-token and dropout fields. An external caption generator does not decide those fields and does not replace manual sampling review. Keep generated captions as user data, not as hidden template content.

## Sources

- fpgaminer/JoyCaption, observed revision `b3d970ee05d4c24fd5d74b76d582ea3bfb2892eb9c15bc76656a8f67ae34b6a0`: https://github.com/fpgaminer/joycaption
- Current caption contract: `../datasets/caption-tag-trigger-strategy.md`
- Formal WD14 guide: `../captions/wd14-tagging-guide.md`

## Boundaries

- No automatic caption generation is run by this task.
- No images or private datasets are collected.
- Generated captions require human review and project-contract validation.

## Eval

- Question: “使用 JoyCaption 生成 caption 后，是否可以跳过触发词和泄漏检查？”
- Expected answer: no; generated captions still require pairing, leakage, trigger, and preview review.

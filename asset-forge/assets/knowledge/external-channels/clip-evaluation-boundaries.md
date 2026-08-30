# CLIP/torchmetrics 评测指标边界

- Version: `2026-08-30`
- Scope: 记录 CLIP、open_clip、torchmetrics 与 clip-score 的指标用途、复现要素和误读风险。
- Evidence status: L1 official repositories + L1 paper metadata；全部公开渠道 HTTP 200。
- Aliases / 检索关键词: CLIP score, torchmetrics, open_clip, 评测, 指标边界, FID

## 使用建议

固定模型版本、预处理、prompt 集、随机种子和聚合方式；分别报告主体/风格/属性等方向，避免单一总分掩盖回归。指标应与人工抽样和预览曲线并列，不能单独决定 checkpoint。

## 解释边界

CLIP 相似度受 prompt、语言和模型偏差影响；高分不等于身份保持或版权合规。torchmetrics 的实现便利性不改变指标的统计假设。

## Sources

- CLIP paper: https://arxiv.org/abs/2103.00020 (L1)
- open_clip: https://github.com/mlfoundations/open_clip (L1)
- torchmetrics: https://github.com/Lightning-AI/torchmetrics (L1)
- clip-score: https://github.com/Taited/clip-score (L1)

## Boundaries

- 本文不提供任何训练学习率或步数推荐。
- 指标缺失、模型版本不明或预处理不同必须标记 unknown，不得横向硬比。

## Eval

- Question: “CLIP 分数最高的 checkpoint 是否必然是最佳发布版本？”
- Expected answer: 不必然；需结合人工抽样、方向分解和复现记录。


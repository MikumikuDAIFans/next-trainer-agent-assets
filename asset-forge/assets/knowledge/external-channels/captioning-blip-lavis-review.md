# BLIP/LAVIS 自动 caption 与人工复核

- Version: `2026-08-30`
- Scope: 将 BLIP 与 LAVIS 作为 caption 生成渠道的比较证据，定义训练前的人工抽样与触发词审查。
- Evidence status: L1 official repositories; 两个仓库页面及 commit API 均 HTTP 200；不下载模型或图片。
- Aliases / 检索关键词: BLIP, LAVIS, caption, 自动标注, 触发词, 人工复核

## 建议流程

自动 caption 只生成草稿。对角色/风格/物体方向分别抽样，检查主体、属性、关系、镜头和不应学习的背景是否被错误描述；触发词必须单独记录并避免与常见标签冲突。将原 caption、解析规则、置信度和人工修订率保留在本地证据表。

## 与现有 tag 流程的关系

caption 与 tag 是数据目标设计，不是模型族或网络算法。可与 WD14 结果做对照，但不能把任一工具输出当作 ground truth。

## Sources

- BLIP: https://github.com/salesforce/BLIP (L1 official)
- LAVIS: https://github.com/salesforce/LAVIS (L1 official)
- 现有标注契约: `../datasets/caption-tag-trigger-strategy.md` (L1/L3)

## Boundaries

- 不保留外部模型权重、图片或长版权文本。
- 自动 caption 的语言、幻觉和漏标必须通过人工抽样报告；unknown 不补写。

## Eval

- Question: “自动 caption 是否可以跳过人工抽样直接训练？”
- Expected answer: 不可以；至少要记录抽样规模、错误类型、置信度与修订率。


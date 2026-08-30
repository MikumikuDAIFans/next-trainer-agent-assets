# FiftyOne 数据集视觉 QA 与重复检查

- Version: `2026-08-30`
- Scope: 用 FiftyOne 的公开工作流定义训练前视觉抽样、近重复和异常样本复核，不引入其机器路径或运行时配置。
- Evidence status: L1 official repository; HTTP 200。
- Aliases / 检索关键词: FiftyOne, visual QA, 近重复, 异常样本, 数据审查

## QA 清单

按训练方向分层抽样，查看尺寸/纵横比、主体可见性、背景泄漏、重复帧、过度压缩和水印。将发现按严重度记录，保留样本 ID 而不是图片副本；删除或修订动作需由用户授权。

## 对 bucket/分辨率的帮助

视觉 QA 先于 bucket 统计。先固定清洗规则，再计算面积分布与 bucket 覆盖；不要因某个工具的默认分辨率反推产品模板值。

## Sources

- FiftyOne: https://github.com/voxel51/fiftyone (L1 official)
- 分辨率与 bucket 基线: `../parameters/resolution-bucket.md` (L1/L3)

## Boundaries

- 不下载或保存图片；只保留抽样计划和统计结果。
- 视觉质量检查不能证明训练效果，也不能替代 validator。

## Eval

- Question: “FiftyOne 的默认视图是否能替代按方向分层抽样？”
- Expected answer: 不能，抽样层级和异常分类必须显式记录。


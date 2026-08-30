# Civitai 字段字典（Stage 1）

本字典区分 model-level、version-level、结构化 API 字段和 description 自由文本抽取字段。未公开值保持 `null` 或空列表；不填默认值。

| 字段 | 层级 | 来源 | 允许值/类型 | 缺失解释 |
|---|---|---|---|---|
| `modelId` | model/version | API `model.id` | integer/null | 无法关联模型时为 null |
| `modelVersionId` | version | API `modelVersion.id` | integer/null | 版本响应缺失时为 null |
| `name` | model/version | API | string/null | 平台未返回 |
| `baseModel` | version | API `baseModel` | string/null | Civitai 未声明或分类不一致 |
| `trainedWords` | version | API | string[] | 未公开时为空数组，不代表没有触发词 |
| `trainingDetails` | version | API structured | object/null | 常见为 null；不能从 description 回填 |
| `descriptionParameters.*` | version | description free text | `{value, source, confidence, match?}` | 正则未命中为 value=null/confidence=unknown |
| `files[].metadata` | version | API file metadata | object/null | 只保留 API 元数据，不下载文件 |
| `url` | model/version | deterministic public URL | string/null | 只允许公开 URL |
| `retrievedAt` | record | collector clock | RFC3339 string | 采集时刻，不是发布时间 |
| `evidence.level` | record | curation | `L2` | Civitai 仅作观察证据 |
| `stats` | model | API | object | download/favorite/rating 只用于发现和偏差报告 |

## 自由文本抽取规则

当前抽取字段为 `rank`、`alpha`、`batch_size`、`steps`、`epochs`、`learning_rate`、`resolution`。仅在 description 中命中明确键名及数值时记录；`source` 固定为 `description`，`confidence` 固定为 `low`，并保存 `match` 原文片段。正则抽取不是结构化训练事实，不能单独支撑模板精确参数。

## 证据与未知规则

- `trainingDetails=null`、`trainingStatus=null` 等原始缺失值必须在 raw 和 normalized 中保留。
- model-level 去重按 `modelId`；version-level 允许同一模型多个版本并单独统计。
- 热门度指标不参与参数有效性、推荐范围或支持结论。
- Civitai 样本低于每分层 8 个独立 model-level 记录时标记 `insufficient`；本次 MVP 所有分层均为 exploratory。

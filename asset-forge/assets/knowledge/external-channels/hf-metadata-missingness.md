# Hugging Face 公共元数据缺失率记录

- Version: `2026-08-30`
- Scope: 记录公共模型 API 字段可用性、截断和 revision 漂移，供来源审计与抽样偏差说明使用。
- Evidence status: L2 observation; 4 个公开 API/搜索请求 HTTP 200，响应上限触发时只保留 `size-limit` 状态。
- Aliases / 检索关键词: metadata, missingness, 缺失率, 模型 API, revision 漂移

## 记录规则

按模型仓库 ID 去重，每个字段三态记录 `present`、`null`、`unknown`。响应被大小上限截断时不得从截断正文推断字段缺失；只记录状态、响应大小与摘要 hash。后续重放应比较观察时间和 revision，不覆盖旧记录。

## 用途

缺失率可以解释为什么某些来源无法支持精确参数建议，也能指导人工抽样。它不等于模型质量或可训练性评分。

## Sources

- Hugging Face Hub API: https://huggingface.co/docs/hub/api (L1 official)
- FLUX API observation: https://huggingface.co/api/models/black-forest-labs/FLUX.1-dev (L2)
- Anima search observation: https://huggingface.co/api/models?search=anima%20diffusion&limit=5 (L2)

## Boundaries

- 不把 API 搜索排序、下载量或点赞数当作推荐依据。
- `unknown` 永远保留为 unknown；不可用字段不回填 schema 默认。

## Eval

- Question: “API 响应被截断时，是否可以按空字段统计缺失？”
- Expected answer: 不可以，应标记 unknown/size-limit 并保留失败或截断证据。


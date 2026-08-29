# assets/eval — 评测种子

存放知识/模板/技能变更的回归评测资产：

- `agent-eval-seeds.jsonl`：问题 → 期望引用的知识文件/模板/字段（从 POC
  `development-docs/docs/reference/agent-poc/test-cases/agent-eval-seeds.jsonl`
  迁移并按新结构改写）。**P0 收集批次待办。**
- 确定性迁移案例同址维护。

每向 `assets/knowledge/`、`assets/templates/` 或 `assets/skills/` 新增一篇内容，
应在此追加对应评测条目（维护规则：补来源、适用范围、证据层级和评测）。

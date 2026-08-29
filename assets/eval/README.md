# assets/eval — 评测种子

存放知识/模板/技能变更的回归评测资产：

- `agent-eval-seeds.jsonl`：行为/安全评测种子（18 条）。前 16 条从 POC
  `development-docs/docs/reference/agent-poc/test-cases/agent-eval-seeds.jsonl`
  原样迁移（能力级、与工具名解耦，仍有效）；2026-08-29 追加 2 条知识引用行为用例
  （三层证据、防幻觉引用）。确定性迁移案例仍见 POC `deterministic-cases.md`。
- `knowledge-citation-seeds.jsonl`：知识库引用评测（14 条，2026-08-29 建）——
  典型问题 → 期望被引用的知识文件 + 必含要点。新增知识文档时必须同步追加。

维护规则：每向 `assets/knowledge/`、`assets/templates/` 或 `assets/skills/`
新增一篇内容，在此追加对应评测条目（补来源、适用范围、证据层级和评测）。
运行方式：由宿主 `agent_skills.run_skill_eval` / agent 会话人工回放（管线接入为待办）。

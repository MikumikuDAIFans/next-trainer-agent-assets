# Gate Validation Checklist

| Gate ID | Description | Required evidence | Status | Notes |
|---|---|---|---|---|
| GATE-00 | 资料来源可信 | `preflight-source-review.md` | pass | 已列出已读与待查来源 |
| GATE-01 | Canonical plan 唯一 | `plan-manifest.md` | pass | 唯一主进度为 `00_总控目标索引.md` |
| GATE-02 | 总目标可验收 | `00_总控目标索引.md` 完成口径 | pass | 使用支持、知识、模板、评测覆盖口径 |
| GATE-03 | 范围边界明确 | 总控 In/Out scope 与授权边界 | pass | 正式迁移和源码写入被禁止 |
| GATE-04 | 目标覆盖完整 | `01_目标计划书` | pass | G1..G5 覆盖总控完成口径 |
| GATE-05 | 目标可测试 | 每目标测试矩阵 | pass | 每目标含六类测试或边界 |
| GATE-06 | 阶段可执行 | `02_长程任务书` | pass | 五阶段均有 durable fields、Phase、验证与证据 |
| GATE-07 | 阶段可失败 | 每阶段 failure handling | pass | 每个 Phase 均定义失败处理和阻断条件 |
| GATE-08 | 开工清单完整 | `04_阶段开工清单` | pass | 五份清单含阶段专属边界和失败处理 |
| GATE-09 | 证据治理完整 | 本目录全部治理文件 | pass | 初版骨架已建立，Stage 4 再固化 |
| GATE-10 | 真实测试受控 | `testing-and-evidence-governance.md` | pass | 外部 API/HTTP 有时间、请求、大小、磁盘限制 |
| GATE-11 | MVP 验证处理 | `05_最小可行性验证` | pass-with-boundary | API 需本地代理；结构化训练字段可空，已设抽取边界 |
| GATE-12 | goal 一致 | `03_goal提示词` | pass | 阶段顺序、授权边界、MVP 边界和完成口径一致 |
| GATE-13 | 变更控制明确 | `change-control-governance.md` | pass | 含迁移授权和采样范围变更规则 |
| GATE-14 | 最终复盘可追溯 | `06_开工前最终复盘报告.md` | pass | 逐份复盘、机器清点和边界审查完成 |

# CR-009：广泛外部渠道与多轮采集扩充

- Date: `2026-08-30`
- Status: `approved-by-task-scope`
- Scope: 在 AgentAssets 内新增 Hugging Face 模型卡/API、官方 examples/config、数据集/标注/评测工具、PyTorch 运行时文档和论文元数据渠道；执行有界匿名采集并生成知识/模板候选与迁移预览。
- Reason: 用户审查指出现有知识与模板覆盖不足，要求尽可能整理更多外部渠道并启动多轮收集。
- In scope: 目录登记、公开 URL 可达性、短摘要 hash、revision/缺失记录、知识候选、宿主 validator 可证明的模板候选、评测、覆盖矩阵、manifest。
- Out of scope: 正式仓库写入、迁移/同步/commit/push/PR/build/package/release、完整权重/图片/数据集下载、登录态或凭据、将外部配置直接视为 Next Trainer 合同。
- New acceptance boundary: 新增来源只能提升知识覆盖或形成比较证据；模板仍须当前页面强 validator `ok`、negative control 非 `ok`、normalized diff 经过审查。
- Sampling budget: 每轮最多 20 请求、20 秒超时、响应最多 128 KiB、请求间隔至少 0.5 秒、失败最多 3 次重试（本采集器不自动重试），不保存正文。
- Rollback: 本变更仅新增 AgentAssets 制品；若门禁失败，隔离候选/失败报告，不修改既有 Stage 0..6 资产。


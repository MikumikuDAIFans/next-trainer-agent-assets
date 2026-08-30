# 预检资料复盘

- Date: `2026-08-29`
- Project: `Next Trainer 3.0.0 / feat/pi-agent-plugin`
- Plan directory: `E:\OpenSourceTeamWork\AgentAssets\00_计划体系`
- Evidence root: `E:\OpenSourceTeamWork\AgentAssets\06_评测与校验\evidence`
- Target branch: `feat/pi-agent-plugin`（只读）
- Canonical progress file: `E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_总控目标索引.md`
- Recommended scale mode: `Full`
- Decision: `ready-with-boundary`

## Source Materials

| Source | Role | Status | Notes |
|---|---|---|---|
| 用户当前请求 | 目标、工作目录、迁移闸门 | read | 明确要求完成制备并等待批准迁移 |
| `project/README-zh.md` | 高层能力声明 | read | 初始模型族和训练方式，不作为唯一裁定 |
| `project/frontend/AGENTS.md` | 训练页面与 schema 调查入口 | read | 给出新增训练模式涉及面 |
| `project` 当前 Git 状态/分支 | 源码基线 | read | 分支为 `feat/pi-agent-plugin`；调查阶段只读 |
| `agent-assets/README.md` | 资产入库契约 | read | 已确认知识头、模板校验、同步和播种规则 |
| `agent-assets/scripts/*.py` | 校验/发布计数契约 | read | 模板须顶层、宿主 validator 为权威 |
| `project` schema/routes/trainers/presets | 精确能力矩阵 | pending | Stage 0 必须完整读取 |
| 官方模型/训练器资料 | 方法事实 | pending | Stage 1 采集并版本化 |
| Civitai API/页面 | 经验分布 | pending | Stage 1 分层采样并报告缺失率 |

## Verified Facts

1. 当前项目 README 声明支持 Anima、SD 1.5、SDXL、Flux 和 Krea 2；具体页面、后端及网络类型仍须从代码确认。
2. README 明示 Anima LoRA/LoKr/T-LoRA、Anima Fast、Anima 全量微调、SD1.5/SDXL LoRA 与全量微调、Flux LoRA、Krea 2 LoRA。
3. 正式知识文件需要 `Version`、`Scope`、`Evidence status`；正式模板需要通过目标页面的 `training_config_validate`。
4. 正式插件播种只补缺失；未来修订同名文件不能自动覆盖老实例。
5. `E:\OpenSourceTeamWork\AgentAssets` 在本任务开始时为空，尚无竞争性主计划。

## Active Assumptions

1. Civitai 公共接口可在合理限额内提供模型、版本、base model、trained words、文件格式和部分训练信息；必须通过 MVP probe 验证。
2. “尽可能所有知识”按可审计覆盖面解释，而非无限抓取互联网：覆盖所有源码确认的训练模式、主流训练目标、关键参数/数据/评测/故障域及其证据边界。
3. 无需下载完整模型权重即可完成大部分模板经验采集；如需读取 safetensors 头，只允许限额 Range 请求并先记录风险。

## Locked Decisions

1. 所有新文件只写入 `E:\OpenSourceTeamWork\AgentAssets`。
2. 未经用户后续明确授权，不迁移、不同步、不改正式资产仓库或主项目快照。
3. 训练器支持能力以“页面路由 + schema + trainer mapping/命令 + validator/preset”交叉证据裁定。
4. Civitai 热度仅用于抽样，模板参数必须标注样本量、缺失率、来源和模型版本，并通过宿主校验。
5. 不采集图片、不批量下载权重、不保存认证信息；默认仅使用公开 API/页面。

## Open Questions

1. 源码最终确认的训练页面、网络算法和 feature flag 完整集合是什么？由 Stage 0 回答。
2. Civitai 对 Anima/Krea 2 等新模型族的有效样本量是否足够？由 Stage 1 回答。
3. “滑块 LoRA”等方向是训练器一等能力、标准 LoRA 的数据构造方法，还是当前不支持？必须在能力矩阵中分级，不预设结论。

## Known Risks

| Risk | Level | Mitigation |
|---|---|---|
| README 与实际 schema/trainer 漂移 | P1 | 四类源码证据交叉确认并记录冲突 |
| Civitai 参数缺失、误报或幸存者偏差 | P1 | 报告缺失率；不从热度推因果；模板需 validator |
| “所有知识”导致无边界扩张 | P1 | 以支持矩阵和主题覆盖矩阵作为完成口径 |
| 误触正式资产或 vendored 快照 | P1 | 路径白名单 + 迁移授权 gate；Stage 4 只产出清单 |
| 外部 API 限流或变更 | P2 | 限频、缓存、重试上限、保留失败报告 |
| 元数据含版权文本或敏感内容 | P2 | 只提取事实字段与短摘要，不复制长文本或图片 |

## Blockers

无。所有未知项均可通过只读源码调查或受限外部 probe 解决。

## Conflicts

1. 备份工程根 `AGENTS.md` 约束生成物留在备份区，而用户本轮明确指定独立暂存目录 `E:\OpenSourceTeamWork\AgentAssets`。处理方式：备份工程保持只读；所有新制品严格写入用户指定暂存区，不向其他位置输出。

## Recommended Plan Shape

使用 Full 模式，五个稳定阶段：能力盘点、来源与 Civitai 证据、知识候选、模板候选、评测与迁移就绪。采用 EDD 作为主方法，以 source-driven 和领域分类作为叠加方法。

## Next Action

生成并审查 `00_总控目标索引.md`。


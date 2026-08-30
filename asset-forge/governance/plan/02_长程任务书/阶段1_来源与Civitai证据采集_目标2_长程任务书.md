# 阶段1：来源与 Civitai 证据采集长程任务书（目标2）

## 计划元数据

- Plan ID: `NT-ASSET-KB-TPL-20260829-S1`
- Version: `v2`
- Last updated: `2026-08-30 00:29 +08:00`
- Canonical progress file: `E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_总控目标索引.md`
- Parent plan: `..\00_总控目标索引.md`
- Goal plan: `..\01_目标计划书\02_目标2_来源与样本证据_实施验收计划.md`
- Checklist: `..\04_阶段开工清单\阶段1_来源与Civitai证据采集_执行前清单.md`
- Current active phase: `complete (pass-with-boundary)`
- Execution readiness: `stage closed 2026-08-30；migration still awaiting explicit user approval`

## 目标

为 G1 的每个支持模式建立官方/项目来源，并构建受控、可复算、明确缺失与偏差的 Civitai LoRA 元数据样本。

## 范围与约束

- In scope: 官方文档/仓库/论文、Civitai 公共 API/页面和限额内文件头；下载模型文件仅用于静态、结构和元数据分析，不用于训练或发布。
- Out of scope: 不必要的图片、预览图、完整权重批量下载、账号/token/Cookie、长文本复制、热度因果判断、任何正式库迁移。
- Output boundary: 下载目标、缓存、临时/解压目录、日志、原始响应、归一化数据、分析结果和报告必须位于 `E:\OpenSourceTeamWork\AgentAssets`；不能控制的外部缓存必须关闭或重定向到该目录，否则停止流程。
- Network policy: 允许有界并发；每批最多 100 个请求、每请求至少 0.5 秒间隔、总 raw 软上限 500 MB。使用连接池并设置总请求预算；HTTP 429、5xx、连接失败执行指数退避，最多重试 3 次，仍失败则保留错误记录并停止相关批次。
- Credential policy: 仅使用 Civitai 官方公开 API/页面，不使用 Token、Cookie、登录态或私人接口，不绕过访问控制。
- Evidence policy: 保留公开 URL、model ID、version ID、采集时间、响应状态、请求参数和错误记录；结构化字段、自由文本抽取字段、抽取来源、置信度及未知/缺失值分开保存。不得把下载量、点赞数、收藏数或热门排序当作技术正确性证据。
- Repository policy: 只读检查源仓库；禁止 commit、push、merge、rebase、tag、PR 或其他 Git 写操作；不修改正式知识库、模板库、主项目或 vendored 快照。正式迁移必须等待用户明确批准。
- Constraints: 先通过 MVP；unknown 保持 null；任何扩大请求量、下载范围、凭据范围或迁移目标的变更必须走 change control 并重新取得授权。

## 执行阶段

### Phase 1: 官方与项目来源登记

- Purpose: 先建立 L1 事实骨架。
- Outputs: `02_来源与证据/source-registry.jsonl`、`official-source-coverage.md`。
- Completion criteria: 每个支持模型族/后端/网络算法至少一个项目契约和官方来源，缺口显式列出。
- Validation: URL、版本/日期、主题映射和证据等级 schema 检查。
- Evidence: `06_评测与校验/evidence/stage-1/phase-1/`。
- Failure handling: 无官方来源则降级结论，不用二手博客冒充官方。

### Phase 2: Civitai 分层采样

- Purpose: 获取真实发布模型的可追溯元数据分布。
- Outputs: `03_Civitai样本/raw/`、`sampling-plan.md`、`request-log.jsonl`。
- Completion criteria: 按 G1 base model/方向分层；模型级与版本级分开；分页、去重、有界并发、限流和失败重试有记录；达到目标样本或明确不足。
- Validation: 请求计数/大小/时间检查；model-level 去重；API contract 抽样。
- Evidence: `06_评测与校验/evidence/stage-1/phase-2/`。
- Failure handling: API 限流/封锁、连续连接失败或超出磁盘/请求预算立即停止批次并报告，不绕过；保留失败 URL、状态、时间和错误信息。

### Phase 3: 归一化、统计与证据裁定

- Purpose: 把 raw 元数据转成可用于知识/模板的观察证据。
- Outputs: `normalized/model-versions.jsonl`、字段字典、缺失率、参数统计、base-model mapping、bias report。
- Completion criteria: raw 可重建 normalized；每页配置可用样本被标 `sufficient/insufficient`；异常和未知保留。
- Validation: 重建哈希/计数；统计脚本单测；抽样回链公开 URL。
- Evidence: `06_评测与校验/evidence/stage-1/phase-3/`。
- Failure handling: 参数字段不足时禁止用该样本支撑模板，仅用于生态/方向观察。

## 测试矩阵

| 类型 | 本阶段要求 | 命令/方式 | 证据 |
|---|---|---|---|
| Unit | JSONL schema、去重、null、统计 | 暂存区脚本 | `evidence/stage-1/unit` |
| Contract | Civitai API/官方 URL 响应 | 受限 HTTP | `evidence/stage-1/contract` |
| Integration | raw→normalized→statistics→evidence card | 一条完整样本链 | `evidence/stage-1/integration` |
| Gray | 样本分布 vs project preset/cases | 差异报告 | `evidence/stage-1/gray` |
| Real | 公共 API 请求 | 每批≤100，≥0.5s 间隔，总 raw≤500MB | `evidence/stage-1/real` |
| Zero-Short | raw 重建 normalized/统计 | 空临时目录 | `evidence/stage-1/zero-short` |

## 决策记录

- Verified facts:
  - Civitai 只被允许作为 L2 观察来源。
  - 通过代理 `127.0.0.1:11809` 请求 model-version `882225` 返回 HTTP 200；`trainingDetails`、`trainingStatus` 为 null，description 含自由文本训练参数。
  - Stage 0 支持矩阵验证为 `pass-with-boundary`，17 条 entry、0 errors。
- Active assumptions:
  - 公共 API 可返回足够基础字段；训练参数完整度未知。
- Locked decisions:
  - model-level 与 version-level 分别统计。
  - 配置可用阈值为每页至少 8 个独立 model-level 样本，否则不能声称分布支撑。
  - 并发采用有界 worker、连接池和总预算；429/5xx/连接失败只做有限退避重试。
  - 所有阶段输出和下载中间物只写入 `AgentAssets`；最终项目状态保持 `awaiting-user-approval`。
- Open questions:
  - Anima/Krea 2 是否有足够公共样本或明确 baseModel 分类。

## 关键制品与环境

- Inputs: G1 支持矩阵。
- Output roots: `02_来源与证据`、`03_Civitai样本`、`06_评测与校验/evidence/stage-1`，均位于 `E:\OpenSourceTeamWork\AgentAssets`。
- Evidence root: `06_评测与校验/evidence/stage-1`。
- Network: 公共 HTTPS，经本机 HTTP 代理 `127.0.0.1:11809`；不使用凭据。模型下载如经批准的分析需要，必须显式指定 AgentAssets 目标目录并记录 URL、哈希、大小和用途。
- Source repositories: `project` 与 `agent-assets` 仅执行只读 Git 检查；发现用户未提交修改只记录，不回退、不清理。

## 进度台账

- Overall progress: `done (pass-with-boundary, 2026-08-30)`
- Phase 1 官方与项目来源登记: `done`（`02_来源与证据/source-registry.jsonl` 12 条、`official-source-coverage.md`；上游 commit 钉版保留为显式 P2 跟进项）
- Phase 2 Civitai 分层采样: `done (MVP 边界)`（7 层 7 请求全 200；`raw/` + `request-log.jsonl`；每层未达 8 独立 model-level 阈值，全部标记 exploratory）
- Phase 3 归一化、统计与证据裁定: `done (MVP 边界)`（`normalized/model-versions.jsonl` 21 model/28 version；`field-dictionary.md`；缺失率与偏差报告；`trainingDetails` 结构化参数 0 条，模板参数分布不成立）
- Validation status: `stage completion gate pass-with-boundary`（`06_评测与校验/evidence/stage-1/stage-completion-gate.md`）
- Residual risks: 新模型族公开样本稀疏；API 可能变化或限流；自由文本参数只能作为低置信观察，不能直接升级为模板事实。P2 跟进：钉住 kohya/musubi/anima-fast 实际运行 commit。
- 后续能力备注（2026-08-30 drift review）：受控 Range 文件头分析能力已实测可用，若 Stage 3 证据不足可走 change control 启用（单文件 Range ≤2 MB、总 ≤50 MB、显式登记）。

## 阶段结束必须生成

stage completion gate、cleanup report、source coverage、sampling/missingness/bias report 和失败响应。

## 下一步动作

执行已通过复核的 Stage 1 Phase 1 官方来源登记，并持续将所有产物写入 AgentAssets；完成后再进入有界 Civitai 分层采样。

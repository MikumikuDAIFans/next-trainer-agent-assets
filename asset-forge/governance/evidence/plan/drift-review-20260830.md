# Drift Review — Stage 0 冻结点之后源仓与环境复核（只读）

- Captured: `2026-08-30 02:39 +08:00`
- Reviewer: `Stage 2 开工执行器（goal 轮次）`
- Scope: `9cd23996..a1a5797 漂移、正式资产基线、Civitai 能力复测`
- Result: `pass-with-boundary`（支持矩阵仍有效；基线更新走 CR-003）
- Change record: `../../00_计划体系/00_预检证据/change-record-003-post-stage0-source-drift.md`

## 1. 命令与结果

| # | 命令（只读） | 结果 |
|---|---|---|
| D1 | `git -C project merge-base --is-ancestor 9cd2399 HEAD` | exit 0，冻结点为 HEAD 祖先 |
| D2 | `git -C project rev-list --count 9cd2399..HEAD` | `14` commits 领先 |
| D3 | `git -C project diff --name-only 9cd2399..HEAD` | 变更集中于 `plugin-packages/next-trainer-pi-agent/**`（后已解除跟踪）、`frontend/dist/**` 构建产物、`mikazuki/plugin_marketplace/**`、marketplace 测试与 i18n；详见 §2 |
| D4 | 按矩阵引用路径过滤 diff：`frontend/src/training`、`mikazuki/schema`、`mikazuki/app/api.py`、`mikazuki/trainers`、`config`、`frontend/src/api/training.ts` | 每个路径 `0` 个变更文件 |
| D5 | `git diff --stat -- mikazuki/app/application.py mikazuki/tasks.py` | +32/-1，grep `trainer_mapping|train_type|training` 无命中（marketplace/任务通道改动） |
| D6 | `git diff -- tests/test_stage2_training_journey.py` | 仅工具目录 18→19（新增 `assets_update`），非训练契约 |
| D7 | `git -C project ls-files plugin-packages` | tracked_count=0（`9121c47` 解除跟踪，工作树目录存在） |
| D8 | `git -C project status --short` / `git -C agent-assets status --short` | 均 0 行（此前记录的 dirty 已由用户侧提交收敛；CR-001/002 保留历史） |
| D9 | agent-assets 盘点 | knowledge=14、templates=4、eval seeds=behavior 18 + citation 15、compat assetsVersion=`2026.08.29-4`、plugin 0.3.5、hostCompatibility `>=2.9.2 <4.0.0` |
| D10 | agent-assets 近期提交 | `4bb336d` 确立权威源仓、`e097f2f` P0 知识/模板批量+eval、`8720f11` 第 13 篇文档+assetsVersion-3、后续签名轮换至 -4 |

## 2. 支持矩阵有效性结论

1. Stage 0 矩阵的全部 L1 引用路径在区间内零变更 → **17 entries 与全部支持等级判定继续有效**，不需重冻结。
2. `tests/test_stage2_training_journey.py` 的 18→19 工具目录属 Agent 工具面（`assets_update` + `content-update` 权限），不改变任何训练页面/schema/validator 结论；知识文档若引用工具面需按 19 口径书写。
3. marketplace 与 pi-web 大量改动为用户/其他任务所有（硬性约束 14），本任务未触碰、不回退。

## 3. 迁移边界事实更新

- `project/plugin-packages/next-trainer-pi-agent` 不再是 git 跟踪的 vendored 快照；agent-assets README（权威合同）确认快照由 `scripts/sync-to-project.py` 生成、禁止手改，内容权威源为 `agent-assets/assets/**`。
- 因此 Stage 4 迁移 manifest 的内容目标只映射到 `agent-assets/assets/{knowledge,templates,eval}` 与 `compat.json` 草案；插件快照播种属于同步脚本动作（另行授权），manifest 不生成对快照的直接写入条目。
- 该变化记入 CR-003，属边界澄清而非范围扩大。

## 4. Civitai / 网络能力复测（本轮实测）

| 探测 | 结果 |
|---|---|
| 直连 civitai.com | DNS 污染（`199.59.148.222` / Facebook v6 段），TLS 连接重置；不可用 |
| 代理监听 | `verge-mihomo` 持有 11807/11808/11809；有效 HTTP 代理 = `127.0.0.1:11809`（系统代理注册表指向 11807，但 11807 到 Civitai 立即失败） |
| Python urllib + 11809 | `GET /api/v1/model-versions/882225` → HTTP 200、16783 bytes、匿名 |
| 文件下载能力 | 对官方 download URL 发 `Range: bytes=0-1048575` → HTTP 206，`Content-Range: bytes 0-1048575/228451444`，Range 被遵守；1 MB 仅驻内存未落盘 |
| 头部分析 | safetensors 头解析成功：2958 个 F16 LoRA tensor；`__metadata__` 含 kohya `ss_*` 完整训练参数（unet_lr=5e-4、text_encoder_lr=5e-5、fp16、bucket 1024×1024×200 等）；若启用该路线须按任务书先登记（单文件 Range ≤2 MB、总 ≤50 MB） |
| pwsh Invoke-WebRequest | 本环境对任何 HTTPS 目标即时失败（含 baidu），网络路径不可用；采集必须继续用 Python（与现有脚本一致） |
| 磁盘 | E: 剩余 52.1 GB，远高于 500 MB raw 软上限 |

## 5. 结论

1. 支持矩阵与 Stage 0 边界决定继续有效；Stage 2 可依据冻结矩阵开工。
2. 台账与 gray 基线按 CR-003 更新至 14/4 与 assetsVersion `2026.08.29-4`。
3. Civitai 采集与受控文件头分析能力可用（Python + 11809 代理）；pwsh 网络栈不可用的事实并入 GATE-11 边界。

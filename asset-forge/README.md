# Next Trainer 知识库与模板库制备暂存区

本目录用于在不触碰正式资产仓库的前提下，调查 Next Trainer 当前训练能力、采集来源证据、整理 Civitai LoRA 元数据，并编制候选知识文档、候选 TOML 模板和评测资产。

## 最高优先级边界

1. 本目录是暂存区，不是正式知识库或模板库。
2. 未经用户再次明确批准，不得把任何候选文件迁移到：
   - `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\agent-assets\assets\knowledge`
   - `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\agent-assets\assets\templates`
   - `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project\plugin-packages\next-trainer-pi-agent`
3. 训练器源码和现有资产仓库在本任务中只读。
4. Civitai 只采集公开、可追溯的结构化元数据和必要的文本说明；默认不下载模型权重或图片。
5. Civitai 的热度、下载量和单个作者配置只能作为发现性/观察性证据，不能直接升级为通用参数结论。

## 目录规划

| 路径 | 用途 |
|---|---|
| `00_计划体系/` | 唯一施工计划、任务书、门禁与授权规则 |
| `01_训练器能力盘点/` | 模型族、页面、后端、算法、训练方向支持矩阵 |
| `02_来源与证据/` | 官方资料、项目契约、来源登记和证据分层 |
| `03_Civitai样本/` | 原始与归一化元数据、采样说明、统计结果 |
| `04_知识库候选/` | 尚未迁移的 Markdown 候选知识文档 |
| `05_模板库候选/` | 尚未迁移的 TOML 候选模板 |
| `06_评测与校验/` | 评测种子、校验记录、覆盖度和失败样本 |
| `07_迁移包/` | 只生成清单和候选映射；用户批准前不得执行迁移 |

唯一主进度文件：`00_计划体系/00_总控目标索引.md`。

## 当前整合布局（2026-08-30）

候选镜像位于 `assets/knowledge`、`assets/templates`、`assets/eval`；采集与索引数据位于 `data/`，评测和迁移证据位于 `governance/`，只描述不执行的同步预览位于 `sync/`。`research-rejected/` 保存拒绝样本，`tools/` 保存可复用校验与审计脚本。

模板事故 F-S4-002 已按方案 B 处置：26 份模板制品中 10 份字节级恢复、16 份语义重建、0 份缺失。16 份重建制品带有 `reconstructed-2026-08-30` 标记，不能视为原件；详情见 `governance/evidence/stage-4/recovery-decision-F-S4-002.md`。正式仓库仍保持只读，当前状态为 `awaiting-user-approval`。

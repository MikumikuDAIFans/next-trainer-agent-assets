# Next Trainer 知识库与模板库全量制备 Plan Manifest

- Plan ID: `NT-ASSET-KB-TPL-20260829`
- Version: `v3.1-recovery`
- Last updated: `2026-08-30 22:00 +08:00`
- Scale mode: `Full`
- Canonical progress file: `E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_总控目标索引.md`
- Project root: `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project`（只读事实源）
- Asset source root: `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\agent-assets`（只读基线与未来迁移目标）
- Plan root: `E:\OpenSourceTeamWork\AgentAssets\00_计划体系`
- Evidence root: `E:\OpenSourceTeamWork\AgentAssets\06_评测与校验\evidence`
- Target branch: `feat/pi-agent-plugin`（只读；暂存区自身不是 Git 仓库）
- Execution readiness: `awaiting-user-approval`

## Source Materials

| Source | Role | Status | Notes |
|---|---|---|---|
| 用户 2026-08-29 指令 | 最终目标与迁移授权边界 | read | 要求在 AgentAssets 完成制备，批准后才迁移 |
| `project/README-zh.md` | 公开支持能力初始声明 | read | 声明 Anima、SD1.5、SDXL、Flux、Krea 2 |
| `project` 源码、schema、preset、trainer mapping | 训练能力权威事实源 | pending | Stage 0 穷举并交叉验证 |
| `agent-assets/README.md` | 正式资产格式和同步规则 | read | 知识头、模板校验、播种只补缺失 |
| `agent-assets/assets/**` | 现有内容基线 | sampled | 后续做完整覆盖差距分析 |
| 模型/训练后端官方文档与论文 | 模型和方法的一层证据 | pending | Stage 1 采集 |
| Civitai 公共 API/模型页面 | LoRA 经验样本与元数据 | pending | 只作观察性证据，记录缺失率 |

## Required Artifacts

| Artifact | Path | Required | Status | Owner skill |
|---|---|---|---|---|
| Workspace README | `E:\OpenSourceTeamWork\AgentAssets\README.md` | yes | done | total-control |
| Plan README | `README.md` | yes | done | total-control |
| Manifest | `plan-manifest.md` | yes | in progress | total-control |
| Master goal index | `00_总控目标索引.md` | yes | done | construction-plan-system/01 |
| Evidence governance | `00_预检证据` | yes | done | construction-plan-system/06 |
| Goal plans | `01_目标计划书` | yes | done | construction-plan-system/02 |
| Task books | `02_长程任务书` | yes | done | construction-plan-system/03 + long-task-planner |
| Goal prompt | `03_goal提示词` | yes | done | construction-plan-system/04 |
| Stage checklists | `04_阶段开工清单` | yes | done | construction-plan-system/05 |
| Feasibility probe | `05_最小可行性验证` | yes | done | construction-plan-system/08 |
| Final readiness review | `06_开工前最终复盘报告.md` | yes | done | construction-plan-system/07 |
| Final readiness report | `06_评测与校验/evidence/stage-4/readiness-report.md` | yes | done | Stage 4 Phase 3 |
| Stage 6 task/checklist/goal | `02_长程任务书/阶段6_多轮外部渠道全量采集_目标7_长程任务书.md` + `04_阶段开工清单/阶段6_多轮外部渠道全量采集_执行前清单.md` + `03_goal提示词/NextTrainer多轮外部渠道全量采集_goal提示词.md` | yes | done | CR-008 / long-task-planner |
| Stage 7 task/checklist/goal | `02_长程任务书/阶段7_广泛外部渠道与知识模板扩充_目标8_长程任务书.md` + `04_阶段开工清单/阶段7_广泛外部渠道与知识模板扩充_执行前清单.md` + `03_goal提示词/NextTrainer广泛外部渠道与知识模板扩充_goal提示词.md` | yes | done | CR-009 / long-task-planner |
| F-S4-002 recovery decision | `governance/evidence/stage-4/recovery-decision-F-S4-002.md` | yes | done | incident recovery |
| F-S4-002 recovery gate | `governance/evidence/stage-4/recovery-gate-F-S4-002.md` | yes | done | incident recovery |
| Recovery hash ledger | `governance/evidence/stage-4/recovery-hash-ledger.json` | yes | pass | recovery tool |
| Integrated template validator | `governance/evidence/stage-4/integrated-template-validation.json` | yes | pass | recovery tool |
| Integration boundary audit | `governance/evidence/integration-boundary-audit.json` | yes | pass | recovery tool |
| Sync manifest preview | `sync/sync-manifest.json` | yes | pass | recovery tool |

## Goal To Stage Mapping

| Goal | Stage | Task book | Completion gate |
|---|---|---|---|
| G1 训练器能力边界 | Stage 0 | `02_长程任务书/阶段0_训练器能力盘点_目标1_长程任务书.md` | `evidence/stage-0/stage-completion-gate.md` |
| G2 来源与样本证据 | Stage 1 | `02_长程任务书/阶段1_来源与Civitai证据采集_目标2_长程任务书.md` | `evidence/stage-1/stage-completion-gate.md` |
| G3 知识库候选 | Stage 2 | `02_长程任务书/阶段2_知识库候选编制_目标3_长程任务书.md` | `evidence/stage-2/stage-completion-gate.md` |
| G4 模板库候选 | Stage 3 | `02_长程任务书/阶段3_模板库候选编制_目标4_长程任务书.md` | `evidence/stage-3/stage-completion-gate.md` |
| G5 评测与迁移就绪 | Stage 4 | `02_长程任务书/阶段4_评测审查与迁移包_目标5_长程任务书.md` | `evidence/stage-4/stage-completion-gate.md` |
| G6 外部渠道扩展与增量资产 | Stage 5 | `02_长程任务书/阶段5_外部渠道扩展与增量资产_目标6_长程任务书.md` | `evidence/stage-5/stage-completion-gate.md` |
| G7 多轮外部渠道全量采集 | Stage 6 | `02_长程任务书/阶段6_多轮外部渠道全量采集_目标7_长程任务书.md` | `evidence/stage-6/stage-completion-gate.md` |
| G8 广泛外部渠道与知识模板扩充 | Stage 7 | `02_长程任务书/阶段7_广泛外部渠道与知识模板扩充_目标8_长程任务书.md` | `evidence/stage-7/stage-completion-gate.md` |

## Gate Status

| Gate ID | Status | Evidence |
|---|---|---|
| GATE-00 | pass | `00_预检证据/preflight-source-review.md` |
| GATE-01 | pass | 本 manifest 的 canonical progress file |
| GATE-02 | pass | `00_总控目标索引.md` 总目标与完成口径 |
| GATE-03 | pass | `00_总控目标索引.md` 范围与授权边界 |
| GATE-04 | pass | `01_目标计划书/00_目标计划书索引.md` 与 G1..G5 |
| GATE-05 | pass | G1..G5 各自测试矩阵与完成门 |
| GATE-06 | pass | Stage 0..4 任务书均含 durable fields 和可执行 Phase |
| GATE-07 | pass | Stage 0..4 每 Phase 均含 failure handling |
| GATE-08 | pass | Stage 0..4 均有通用与差异化硬门槛 |
| GATE-09 | pass | `00_预检证据` 全部治理文件 |
| GATE-10 | pass | `00_预检证据/testing-and-evidence-governance.md` |
| GATE-11 | pass-with-boundary | Civitai 需本地代理且 trainingDetails 常为 null；见 probe report |
| GATE-12 | pass | goal 阶段、边界、证据和最终状态与总控一致 |
| GATE-13 | pass | `00_预检证据/change-control-governance.md` |
| GATE-14 | pass | `06_开工前最终复盘报告.md` 逐份复盘与机器检查 |

## Evidence Roots

| Stage | Evidence path | Cleanup rule |
|---|---|---|
| Plan | `06_评测与校验/evidence/plan` | 永久保留文本门禁和报告 |
| Stage 0 | `06_评测与校验/evidence/stage-0` | 保留清单、命令和汇总；临时扫描输出可删 |
| Stage 1 | `06_评测与校验/evidence/stage-1` | 保留来源登记和归一化元数据；响应缓存按清单去重 |
| Stage 2 | `06_评测与校验/evidence/stage-2` | 保留 lint、引用和覆盖结果 |
| Stage 3 | `06_评测与校验/evidence/stage-3` | 保留 TOML/宿主校验结果和失败样本 |
| Stage 4 | `06_评测与校验/evidence/stage-4` | 永久保留 readiness、迁移清单和 hash |
| Stage 5 / G6 | `06_评测与校验/evidence/stage-5` | 外部渠道扩展、增量资产、门禁和清理报告 |
| Stage 7 / G8 | `06_评测与校验/evidence/stage-7` | 广泛渠道采集、候选增量、门禁和清理报告 |

## Current Status

- Current active phase: `计划完成 — Stage 7/G8 完成；readiness awaiting-user-approval（等待用户审阅迁移包）`
- Validation status: `GATE-00..14 pass/pass-with-boundary；Stage 0/1 pass-with-boundary；Stage 2 pass；Stage 3 pass-with-boundary；Stage 4 pass；Stage 7/G8 pass-with-boundary`
- Residual risks: live-agent 会话回放未运行（待宿主管线；迁移后首批执行 kc-001..040）；C-016（P2）致 sdxl-finetune 页无候选，复活由 runner 断言红灯触发；marketplace 并发改动属用户所有；PS5.1 ANSI 编码事故已修复固化（cleanup 缺陷 #4）。
- Next action: **移交用户**——审阅 `07_迁移包/migration-preview.md` + `migration-manifest.json`（当前 91 ops）；若批准，按 cleanup §重放链刷新 hash 后逐条另行授权迁移执行（批次/assetsVersion 由用户定）。
- Recovery status: **F-S4-002 已处置**——10 exact / 16 reconstructed / 0 missing；重建不等于原件，正式迁移仍须用户单独批准。

## Revalidation (2026-08-30)

- Deterministic replays: Stage 0 matrix, Stage 2 lint/matrix/eval map, Stage 3 host validator, Stage 4 eval review/manifest/Zero-Short all exit 0.
- Stage 1 remains the recorded 7-request exploratory sample (`pass-with-boundary`); no new network scope was opened.
- Explicit readiness artifact: `06_评测与校验/evidence/stage-4/readiness-report.md`.
- Formal repositories remain read-only and migration state remains `awaiting-user-approval`.
- Current HEAD drift is tracked by `00_预检证据/change-record-005-current-head-revalidation.md`; no training contract files changed and all deterministic gates were replayed.
- Concurrent build-script edits observed after revalidation are tracked by `00_预检证据/change-record-006-concurrent-build-script-drift.md`; migration approval must include a fresh status/manifest check.
- G6 external-channel expansion is closed with `pass-with-boundary`; refreshed manifest/preview now describe 65 ops (46 knowledge, 9 templates, 9 evidence cards, 46 eval rows).
- G7 multi-round channel program is closed with `pass-with-boundary`; refreshed manifest/preview now describe 79 ops (54 knowledge, 12 templates, 12 evidence cards, 54 eval rows).
- G7 current manifest totals are 79 ops (54 knowledge, 12 templates, 12 evidence cards, 54 eval rows); Stage 6 gate and cleanup are retained under `evidence/stage-6`.
- G8 broad-channel expansion is closed with `pass-with-boundary`; 58 channels and 90 indexed requests are cataloged, 39/39 new requests succeeded, 64 knowledge candidates and 13 validator-proven templates are represented in a 91-op migration preview.

## Stage 4 Completion (2026-08-30)

- Gate: `pass`（`evidence/stage-4/stage-completion-gate.md`，13 口径全 ✓）→ **readiness `awaiting-user-approval`**（完成口径 #10 的正向终态；`not-ready` 不成立：无硬验证失败/目标冲突）。
- Phase 1：40/40 eval 三方一致、迁移行 40（正式 citation 格式）、三态清单（失败 0/未运行 live 回放/不适用 GPU）。
- Phase 2：`07_迁移包/migration-manifest.json` 51 ops（50 create+1 append）全 sha256、白名单 4 前缀、逐目标 exists=0、compat 草案 54/9/55/18 + version 草案 `2026.08.30-5`；播种策略 seed-if-missing+主权跳过；CR-004 基线再同步。
- Phase 3：Zero-Short 空目录重建 hash parity 50/50 + lint/validator 门重放全绿 + 输入纯净 + finally 清理；git baseline/final **IDENTICAL**（HEAD `e005f77`/`7608510`，porcelain 仅用户 `.pi/`）——正式仓零写入决定性证明。
- 事故固化：PS5.1 ANSI 破坏两份阶段清单→逐字重建+全树扫描仅此两份；CJK 文件处理纪律入 cleanup。

## Stage 3 Completion (2026-08-30)

- Gate: `pass-with-boundary`（`evidence/stage-3/stage-completion-gate.md`）。候选 5 TOML（flux/chroma/krea2/sd-dreambooth/sd2）强页 validator 全 ok、negative controls 全 redirect、normalized diff 全零、zero-short 复现；正式脚本第二意见 5/5 `[ok]`。
- 真实发现：C-016 sdxl-finetune+TE1/TE2 导入必 redirect（master 页则类型漂移 sdxl-lora）→ 模板入 research-rejected + failure F-S3-001 + runner 回归断言；未削弱验收。
- 只读复核：`-B` 全程、utils `__pycache__` 未触碰（时间戳 08-21）、porcelain 无本任务痕迹；今日 plugin_host pycache 属用户并发进程。

## Stage 2 Completion (2026-08-30)

- Stage 2 completion gate: `pass`（`06_评测与校验/evidence/stage-2/stage-completion-gate.md`）。
- 40 篇候选知识（model-families 10 + engines 1 + network-algos 6 + directions 9 + datasets 3 + parameters 4 + training 3 + errors 1，另 2 篇边界文档计入 model-families）；覆盖矩阵 544 cells 0 missing；lint 40/40 冻结 exit 0。
- 每篇 eval 草稿 `kc-001..040`（`eval-candidates/knowledge-citation-draft.jsonl`，draft-unrun，执行评测排入 Stage 4）。
- 来源审查：7 arXiv 标题核实、4 GitHub 可达核实、2 例坏链当场收回（CAME 等，见 `evidence/stage-2/phase-3/phase-3-report.md`）。
- lint 工具阶段内修正 1 次（S2 跨行误报收紧为行内匹配），留痕于 `evidence/stage-2/phase-2/batch-2-report.md`。

## Stage 1 Completion (2026-08-30)

- Stage 1 completion gate: `pass-with-boundary`（`06_评测与校验/evidence/stage-1/stage-completion-gate.md`）；MVP 级 Civitai 样本 7/7 HTTP 200、21 model-level/28 version-level，全部层未达 8 独立样本阈值，仅按 L2 观察使用。
- Drift review（`06_评测与校验/evidence/plan/drift-review-20260830.md`）：支持矩阵引用路径零变更；正式资产基线 12+3 → 14+4（assetsVersion `2026.08.29-4`）；Civitai 能力经 Python+代理复测可用（含受控 Range 文件头读取能力，未启用权重下载）。
- 相关变更：`CR-003`。

## Stage 1 Boundary Update (2026-08-30)

- All collection, download, cache, extraction, logs and reports are confined to `E:\OpenSourceTeamWork\AgentAssets`.
- Bounded concurrency is allowed with connection pooling, request budgets and exponential backoff for 429/5xx/connection failures (maximum 3 retries).
- Model downloads, if later needed, are analysis-only and must record public URL, hash, size and purpose; no images or unnecessary files.
- No token/Cookie/private API and no Git write operations. Formal knowledge/template/main-project writes remain prohibited until explicit user migration approval.
## Integration Executed (2026-08-30)
- 经用户明确批准，整目录落仓 `agent-assets\asset-forge`（312 文件字节级一致；git 仅 `?? asset-forge/` 未跟踪，无 commit/push；project 仓 clean）。
- sync-manifest reconstruction 标记 16/16；边界合同见 `asset-forge/README.md`。
- Next action 变更：用户 commit `asset-forge` + 设计单向同步机制（每次执行另行授权）。

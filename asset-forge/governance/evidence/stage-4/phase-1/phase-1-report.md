# Stage 4 Phase 1 报告 — 全量结构与语义评测

- Date: `2026-08-30 03:30 +08:00` · Result: `pass`

## 结构评测（确定性，`tools/stage4_eval_review.py`，exit 0）

| 检查 | 结果 |
|---|---|
| 候选知识 ↔ eval 草稿 ↔ manifest eval_seed_id 三方一致 | 40/40 |
| eval 草稿完整性（must_include + boundary_must_not 非空） | 40/40 |
| 候选 ↔ 正式 14 篇文件名重叠 | 0 |
| 候选模板 ↔ 证据卡 ↔ validator `ok` 工件成对 | 5/5 |
| research-rejected ↔ failure report 互引 | 1/1 |
| 迁移行转换（正式 citation-seed 格式，追加式） | `eval-candidates/knowledge-citation-migration-rows.jsonl` 40 行（expect_files=`knowledge/...` 目标根格式，与现役 15 条同构） |
| 硬门重放 | stage2_lint `40/0`、matrix `544/0`、evalmap `40` 全 exit 0 |
| Real validator 重放（venv `-B`） | pass（主目录+zero-short 双轮 + 阴性/拒绝断言） |

## 行为/语义评测口径（透明声明）

- 本阶段行为层证据 = **本任务过程中的真实事故语料**（非模拟）：2 例坏引用被来源审查收回（CAME/arXiv、404 repo）、sdxl-finetune redirect 不被绕过（C-016/F-S3-001）、krea2"官方推荐"措辞按 C-013 降级、unknown-here 拒不填充（Flux LR/dim、finetune 参数）、`_zkz` 破坏性行为写入知识警示。逐条出处见 stage-2/3 phase 报告。
- 现役 18 条行为种子（含 `cfg-missing-path`"不编造路径"、`cfg-secret-redaction` 等，ids 全清单见 `eval-review-summary.json`）覆盖反编造/凭据/提交门——本任务未新增行为种子（数量草案不变），如需可另行起草（追加轨道）。
- 引用真实性由 must_cite=自身文档 + expect_files 目标根格式在迁移后即可被宿主 `run_skill_eval` 回放；"代表性 Agent 回放"未执行 live 会话（无授权运行时），按清单要求作为**未运行项**显式报告，不记 pass。

## 失败/未运行/不适用清单（三态透明）

- 失败：无。
- 未运行：live-agent 会话回放（管线接入为宿主待办，eval README 同口径）。
- 不适用：GPU 实训评测（本任务边界=不训练）。

## 工具与工件

- `tools/stage4_eval_review.py`、`eval-review-summary.json`、`eval-review-console.txt`、`knowledge-citation-migration-rows.jsonl`。

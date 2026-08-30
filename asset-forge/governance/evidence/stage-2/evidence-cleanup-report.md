# Stage 2 证据清理报告（evidence cleanup）

- Date: `2026-08-30 06:10 +08:00`
- Scope: `06_评测与校验/evidence/stage-2/**`、`tools/stage2_*.py`、`04_知识库候选/**`、`06_评测与校验/eval-candidates/**`

## 清单与留存判定

| 类别 | 路径 | 大小 | 处置 |
|---|---|---|---|
| 阶段报告 | `evidence/stage-2/stage-2-preflight-report.md`、`phase-1/`、`phase-2/batch-1..3`、`phase-3/` | ~15 KB | 永久保留（治理文本） |
| 生成器/检查器 | `tools/stage2_build_coverage_matrix.py`、`tools/stage2_lint.py`、`tools/stage2_eval_draft_map.py` | <60 KB | 保留（可重放；Stage 4 复用） |
| 覆盖产物 | `04_知识库候选/knowledge-coverage-matrix.csv`、`knowledge-manifest.jsonl` | ~70 KB | 保留（确定性重生成，源输入已冻结） |
| 候选正文 | `04_知识库候选/**/*.md` 40 篇 | ~220 KB | 保留（核心制品） |
| eval 草稿 | `06_评测与校验/eval-candidates/knowledge-citation-draft.jsonl` | ~20 KB | 保留 |
| 临时脚本 | `$env:TEMP/stage2_src_review.py`（系统 temp，非工作区） | 1 KB | 已留于 temp，不属证据树；可随 temp 回收 |
| 网络响应缓存 | 无 | — | 来源审查仅取 `<title>`/头部片段，未落盘任何响应体 |

## 敏感与边界扫描

- `stage2_lint.py` S1/S2 全量通过：无机器绝对路径（`X:/` 占位符制式）、无凭据形态串。
- 证据目录内无图片、无权重、无 token/Cookie；Civitai 相关仅引用 Stage 1 已冻结报告文件名。
- 未触碰正式仓库：本轮 `git status` 快照显示 `project` 仅 `mikazuki/plugin_host/runtime.py` 与 `.pi/`（用户并发的 plugin-marketplace/host 工作所有，CR-003 记录在案，不属本任务且未动）；`agent-assets` 的 4 改 1 增全部位于 `plugin/next-trainer-pi-agent/pi-web|scripts`（marketplace 并发改动，非 `assets/**`）。**本任务对两仓库写入次数：0。**

## 可重放性

三个入口命令（相对 `E:\OpenSourceTeamWork\AgentAssets`）：

```text
python -B tools\stage2_build_coverage_matrix.py .
python -B tools\stage2_eval_draft_map.py .
python -B tools\stage2_lint.py .
```

重放均 exit 0，输出与冻结版一致（覆盖 544/0、40/40 lint、40 eval drafts）。

# Stage 3 证据清理报告（evidence cleanup）

- Date: `2026-08-30 03:10 +08:00`（本地钟）
- Scope: `05_模板库候选/**`、`tools/stage3_validate_templates.py`、`06_评测与校验/evidence/stage-3/**`

## 清单

| 类别 | 内容 | 处置 |
|---|---|---|
| 候选制品 | 5 TOML + 5 evidence 卡 + README + coverage csv | 保留（核心制品） |
| 拒绝区 | research-rejected/（1 对） | 保留（断言目标 + failure report 互引） |
| 校验工件 | phase-3/*.json（12）、runner/formal 输出 txt | 保留（可重放，工件小） |
| 报告 | phase-1-2、phase-3、failure-F-S3-001、本清理报告 | 永久保留（治理文本） |
| 临时 | `$env:TEMP/probe_finetune.py`、`stage2_src_review.py` | 系统 temp，不属证据树，可回收 |

## 只读边界复核（Stage 3 特别项：宿主 validator 执行）

- 全程 `python -B`；决定性证据：`project/mikazuki/utils/__pycache__` 保持 2026-08-21 时间戳（本任务唯一 import 链为 `mikazuki.utils.config_import`，如写 bytecode 必落此处）。
- 项目树内今日新增 pycache 位于 `mikazuki/plugin_host`、`plugin_marketplace`、`app`、`tests`（时间戳 00:40–03:04，属用户并发 marketplace 工作/开发进程，与本任务 import 链不符）。
- `project` porcelain：仅 `?? .pi/`（用户工作）；`agent-assets` porcelain：空。两仓库 `assets/**`、`config/presets/**`、schema 目录无本任务写入。
- 未产生下载、图片、权重、token；validator 为纯函数调用。

## 可重放

```text
<project>\.venv-dev\Scripts\python.exe -B tools\stage3_validate_templates.py <staging> <project>   # 期望 exit 0
<project>\.venv-dev\Scripts\python.exe -B <agent-assets>\scripts\validate-templates.py <staging>\05_模板库候选   # 期望 exit 0
```

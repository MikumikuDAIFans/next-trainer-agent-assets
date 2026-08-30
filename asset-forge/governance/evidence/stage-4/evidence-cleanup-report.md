# Stage 4 证据清理报告

- Date: `2026-08-30 04:10 +08:00`
- Scope: `06_评测与校验/{eval-candidates,evidence/stage-4}`、`07_迁移包`、`tools/stage4_*.py`

## 保留

- `eval-candidates/knowledge-citation-draft.jsonl`（草稿全保真 40）与 `knowledge-citation-migration-rows.jsonl`（正式格式迁移行 40，由草稿确定性转换，二者互引）。
- `evidence/stage-4/`：phase-1（review json/console/report）、phase-3（zero-short json/console/report）、gate、`git-baseline-20260830.txt`、`git-final-20260830.txt`。
- `07_迁移包/`：manifest + preview。
- `tools/stage4_eval_review.py`、`stage4_migration_manifest.py`、`stage4_zero_short.py`（批准时重放链）。

## 过程缺陷记录（工具侧，已修复复跑）

1. `stage4_zero_short.py` 首跑把门重跑生成的 validator 工件误判为"多余输入"→ 输入纯净断言移至门重跑之前；复跑 pass。
2. 治理伴随文件名笔误（support-→knowledge-coverage-matrix.csv）→ 修正并加"缺失即失败"断言。
3. pwsh `>` 重定向先于 python 建目录打开文件 → 预建目录后重跑（记录为环境操作纪律，非工件缺陷）。
4. **编码事故（已修复）**：PowerShell 5.1 `Get-Content -Raw` 默认 ANSI 读 UTF-8 文件导致两份阶段清单（S3/S4）乱码且一次写入把乱码固化。处置：全树乱码特征扫描（md/csv/jsonl/toml/txt/json）确认**仅这两份**受损；按本会话内保留的逐字原文用 write 工具重建（含 tick 与完整性说明头）；复扫零命中。教训固化：**CJK 文件一律用 edit/write 工具或 `-Encoding UTF8` + Python 处理，禁用 PS5.1 隐式编码读写**。

## 回收

- `zero-short-tmp`（已清理，`Test-Path=False`）；`$env:TEMP/probe_finetune.py`（系统 temp，可自回收）。
- 无下载物、无图片/权重、无 token 类文件产生。

## 重放链（批准前刷新用）

```text
python -B tools\stage4_eval_review.py <staging>
<project>\.venv-dev\Scripts\python.exe -B tools\stage3_validate_templates.py <staging> <project>
python -B tools\stage4_migration_manifest.py <staging>
<project>\.venv-dev\Scripts\python.exe -X utf8 -B tools\stage4_zero_short.py <staging> <project>
```

# Stage 2 Phase 1 报告 — 信息架构与覆盖矩阵

- Date: `2026-08-30 03:05 +08:00`
- Result: `pass`
- Inputs: 冻结支持矩阵（17 entries）、G3 验收标准、CR-003 基线（14 formal 文档）

## 产物

| Artifact | Path | 验证 |
|---|---|---|
| 信息架构与写作契约 | `04_知识库候选/README.md` | 结构覆盖 G3 全部主题域 |
| 覆盖矩阵 | `04_知识库候选/knowledge-coverage-matrix.csv` | 544 cells（17 modes × (16 topics + 16 directions)） |
| 文档 manifest | `04_知识库候选/knowledge-manifest.jsonl` | 14 formal + 40 candidate，含批次与 eval 槽位 |
| 矩阵生成器（可重放） | `tools/stage2_build_coverage_matrix.py` | 读冻结 JSON，确定性输出 |
| Lint | `tools/stage2_lint.py` | 头三件套/别名/来源卡/边界节/链接/敏感扫描/manifest 一致性 |

## 命令与结果

```text
python -B tools\stage2_build_coverage_matrix.py E:\OpenSourceTeamWork\AgentAssets
=> modes=17 operationalModes=11 cells=544 cellsMissing=0 docsFormal=14 docsCandidate=40 errors=[] exit=0

python -B tools\stage2_lint.py E:\OpenSourceTeamWork\AgentAssets
=> scanned=0 failing=0 manifestCandidates=40 notYetWritten=40 exit=0
```

## 覆盖裁定（对应 G3 验收 1/2/3/6）

1. 11 个 operational modes（8 first-class + 3 conditional）的每格 topic/direction 均有 owner 文档（candidate 或现役 formal），`cellsMissing=0`。
2. 6 个 hidden/unsupported modes（Lumina 2、Flux finetune hidden、lora-basic legacy、SD3、TI/XTI、ControlNet）标 `n/a-mode-not-operational`，仅由边界文档承载，不生成操作指南。
3. 16 个训练方向全部有归属：12 个数据目标方向由 `directions/` 候选承载；slider/erasure → `slider-erasure-boundaries.md`（not first-class）；controlnet/TI → `hidden-and-unsupported-boundaries.md`（unsupported）。
4. 现役 14 篇 formal 文档在 manifest 中登记为 gray 基线；候选不改写它们。

## 失败处理演练

矩阵生成器对未知 mode/topic/direction 引用即报 error 并 exit 1；lint 任一 FAIL 即非零退出，文档不能标 ready。Phase 2 每批写作后必须两条命令重放。

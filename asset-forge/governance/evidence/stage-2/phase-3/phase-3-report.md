# Stage 2 Phase 3 — eval 映射、来源审查、lint 冻结报告

- Date: `2026-08-30 06:05 +08:00`
- Result: `pass`

## 1. Eval 草稿映射（每篇候选 ≥1 eval）

- 工具：`tools/stage2_eval_draft_map.py`（确定性输出，路径排序 → `kc-001..kc-040`）。
- 输出：`06_评测与校验/eval-candidates/knowledge-citation-draft.jsonl`（40 行）。
- 每条含 `question / must_cite(自身文档) / must_include(关键事实) / boundary_must_not(禁止越界表述) / status=draft-unrun`。
- 明确注记：draft 未对 live agent 执行过；正式 eval 种子在插件 seeds 目录，本任务**未修改**（只读边界）。
- `tools/stage2_build_coverage_matrix.py` 升级：manifest 的 `eval_seed_id` 从 draft jsonl 关联（formal 文档保持 null，其对应正式 citation seeds 已存在于现役资产）。重放验证：40/40 candidate 行获得 eval_seed_id。

## 2. 来源审查（引用 URL 逐条在线核实，Python+代理 `11809`）

arXiv（标题匹配通过）：

| ID | 主题 | 核实标题（截断） |
|---|---|---|
| 2106.09685 | LoRA | LoRA: Low-Rank Adaptation of Large Language Models ✓ |
| 2210.07558 | DyLoRA | DyLoRA: …using Dynamic Search-Free Low-Rank Adaptation ✓ |
| 2306.07280 | OFT | Controlling Text-to-Image Diffusion by Orthogonal Finetuning ✓ |
| 2306.06101 | Prodigy | Prodigy: An Expeditiously Adaptive Parameter-Free Learner ✓ |
| 2301.07733 | D-Adapt | Learning-Rate-Free Learning by D-Adaptation ✓ |
| 2303.09556 | Min-SNR | Efficient Diffusion Training via Min-SNR Weighting Strategy ✓ |
| 2311.12092 | Sliders | Concept Sliders: LoRA Adaptors for Precise Control in Diffusion Models ✓（Stage 1 已登记） |

GitHub（可达性核实）：`KohakuBlueLeaf/LyCORIS` ✓、`kohya-ss/musubi-tuner` ✓、`black-forest-labs/flux` ✓、`kozistr/pytorch_optimizer` ✓。

**失败与处置（2 例，全部收回，无残留）**：

1. CAME arXiv `2307.03865` → 实为代谢组学论文，不匹配；候选 `2307.02089` → 实为 NV 色心成像论文，不匹配；ACL Anthology `2023.findings-acl.3` → 实为 Conformal Nucleus Sampling，不匹配。处置：`optimizer-scheduler-guide.md` 删除全部未核实 CAME 链接，改为"按标题引用 + 已核实的 `kozistr/pytorch_optimizer` 实现集合链接"。教训：优化器论文 ID 必须先 verify 再入文（lint 不防假链接，来源审查防）。
2. `jingyi0000/pytorch-optimizer-v2` 404 → 换 `kozistr/pytorch_optimizer`（可达，且为 schema 命名空间 `pytorch_optimizer.*` 的对应实现库）。

## 3. Lint 冻结运行（Phase 3 final）

```text
python -B tools\stage2_lint.py E:\OpenSourceTeamWork\AgentAssets
=> scanned=40 failing=0 manifestCandidates=40 notYetWritten=0 exit=0
python -B tools\stage2_build_coverage_matrix.py E:\OpenSourceTeamWork\AgentAssets
=> cells=544 cellsMissing=0 docsFormal=14 docsCandidate=40 errors=[] exit=0
```

- lint 阶段内工具修正 1 次（S2 跨行误报 `token:`→行内 `[ \t]`，见 batch-2 报告）；文档示例改写 1 次（权重语法）。均留痕，未放宽实质检查。

## 4. 覆盖一致性

- manifest 40 候选 ↔ 磁盘 40 文件（`manifestCandidatesNotYetWritten=0`）；14 formal 只读引用在册。
- 544 覆盖格 0 MISSING（支持模式 × 主题/方向 owner 齐）。
- 无候选文件名与 14 篇正式文件冲突（gray 基线维持 14+4 未动）。

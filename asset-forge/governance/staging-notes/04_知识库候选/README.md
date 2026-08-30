# 04_知识库候选 — 信息架构与编制契约

- Version: `2026-08-30`
- Scope: Stage 2 候选知识库的目录结构、命名、写作契约与覆盖证明方式。
- Evidence status: 结构由 G1 冻结支持矩阵 + G3 验收标准推导；覆盖由脚本可重放生成。

## 目录结构（迁移映射到 `agent-assets/assets/knowledge/**`）

| 子目录 | 内容 |
|---|---|
| `model-families/` | 每个模型族×页面×粒度的基础工作流指南、边界文档 |
| `engines/` | 引擎差异与工作流（standard vs Fast vs Musubi） |
| `network-algos/` | adapter 网络算法适用性/限制（LoKr、T-LoRA、DyLoRA、OFT、LyCORIS、schema-only 陷阱） |
| `directions/` | 训练方向（数据/监督目标设计，与模型、算法正交） |
| `datasets/` | 数据准备、caption/tag/trigger、正则化图 |
| `parameters/` | 跨模型参数主题（bucket、曝光预算、optimizer、缓存精度） |
| `training/` | 预览采样评测、checkpoint 选择、复现与发布 |
| `errors/` | 故障排查扩展（现役 common-errors 之外） |

## 写作契约（每篇必须）

1. 头部三件套：`- Version:`、`- Scope:`、`- Evidence status:`；加 `- Aliases / 检索关键词:` 行。
2. `## Sources`：URL/项目路径 + 证据层级（L1 project contract / L1 official / L2 observation / L3 inference）；无来源的精确数值禁止出现。
3. `## Boundaries`：不支持项、未知项、不可外推项；unknown 保持 unknown。
4. 内部相对链接只指向候选集内或现役正式文档同构路径（迁移后仍可解析）。
5. 机器路径一律 `X:/...` 占位符；不复制外部或项目长文本。
6. 每篇在 `06_评测与校验/eval-candidates/knowledge-citation-draft.jsonl` 有 ≥1 条评测草稿（Phase 3 冻结）。

## 覆盖证明（不以文章数量替代）

- `tools/stage2_build_coverage_matrix.py` 读取冻结的 `01_训练器能力盘点/support-matrix.json`，生成 `knowledge-coverage-matrix.csv`（17 modes × 16 topics × 16 directions 投影，544 cells）与 `knowledge-manifest.jsonl`（40 candidates + 14 formal baseline）。
- 校验口径：每个 first-class/conditional mode 的每个 topic/direction 格有 owner；slider/erasure 指向边界文档；controlnet/TI 为 unsupported 边界；hidden/unsupported modes 标 n/a，不生成操作指南。

## 校验命令

```text
python -B tools\stage2_build_coverage_matrix.py E:\OpenSourceTeamWork\AgentAssets
python -B tools\stage2_lint.py E:\OpenSourceTeamWork\AgentAssets
```

## Gray 策略

现役正式文档 14 篇（基线 `2026.08.29-4`，见 CR-003）原样保留：本候选集不改写、不重命名现役文件；同主题候选以新文件名交叉引用现役文档；文件名升级与 compat 计数在 Stage 4 迁移 manifest 中处理。

## 批次

| 批次 | 内容 | 状态 |
|---|---|---|
| 1 | model-families + engines（14 篇，含边界文档） | **done**（lint 14/14 ok，2026-08-30） |
| 2 | network-algos（6）+ directions（9） | **done**（累计 29/29 ok，含 lint 误报修正留痕） |
| 3 | datasets（3）+ parameters（4）+ training（3）+ errors（1） | **done**（40/40 lint 冻结；Stage 2 完成门 pass） |
| 4-6 | external-channels 外部仓库/论文/工具证据 | **done**（14 篇；Stage 6 pass-with-boundary） |
| 7 | Hugging Face 模型卡/API、examples/config、caption/dataset/eval、PyTorch 与论文元数据 | **done**（新增 10 篇；64/64 lint；Stage 7 pass-with-boundary） |

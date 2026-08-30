# 迁移预览包（migration preview — describe only）

- 生成：`tools/stage4_migration_manifest.py`（本包不含任何复制/同步/提交/发布动作；执行权在用户批准之后）
- Manifest：`migration-manifest.json`（91 ops，sha256 全量，生成于当前工作区并逐目标验证"不存在"）

## 批准后将发生什么（精确口径）

| 类别 | 数量 | 目标 | 操作 |
|---|---|---|---|
| 知识文档 | 64 | `assets/knowledge/{model-families,engines,network-algos,directions,datasets,parameters,training,errors,external-channels}/...` | **create**（全部新文件名；与现役 14 篇零冲突，已机器校验） |
| 候选模板 | 13 | `assets/templates/{flux,chroma,krea2,sd-dreambooth,sd2,anima,anima-fast}-*.toml` | **create**（与现役 4 模板零冲突） |
| 模板证据卡 | 13 | `assets/templates/*.evidence.md` | **create**（.md 扩展名，不与 validator 的 *.toml glob 冲突；正式脚本只扫 toml，已验证） |
| 评测种子 | 64 行 | `assets/eval/knowledge-citation-seeds.jsonl` | **append**（id 空间 `kc-001..064` 与现役 `cite-*` 零碰撞，已机器校验；正式格式同构） |
| compat.json | — | 不写入本包 | 仅计数草案：14→78 知识、4→17 模板、citation 15→79、behavior 18 不变；assetsVersion 草案 `2026.08.30-5`（发布/签名/zip 属后续 release 流程，不在本包） |

## 播种文件名策略（清单要求）

- 策略=**seed-if-missing + 用户文件主权**（正式 README 合同）：本包全部为 create/append，**零覆盖、零删除、零改名**。
- 文件名检查：manifest 生成器对 91 个目标逐一 `exists()` 断言（当前全部不存在→可安全新建）；若批准时任何目标已存在（例如用户自增同名文件），该 op 必须跳过并报告，不覆盖。
- research-rejected/、tools/、06/00/01 计划目录**不在迁移范围**（研究/治理区，永不迁移）。

## 审查清单（用户批准前建议核对）

1. 重放 `tools/stage4_migration_manifest.py` 刷新 hash/存在性（若目标仓已前进，见 CR-004/CR-007 条款）。
2. 抽样阅读任一 `.evidence.md` 与对应 TOML（值级出处）。
3. 决定批次（一次性 vs 分阶段）与 assetsVersion bump 值（草案 `2026.08.30-5` 可改）。
4. eval 行为种子是否需要追加（本包 behavior 不变，可另起追加轨道）。
5. 迁移执行本身（复制 + compat bump + 提交）需届时逐条另行授权。

## 本包未做的事

- 未写正式仓（porcelain 前后对比见 `evidence/stage-4/git-baseline-20260830.txt` 与 Phase 3 终检）。
- 未 push/build/release/sign；未改 compat.json；未生成发布 zip。

# Stage 2 Phase 2 — Batch 1 报告（model-families + engines）

- Date: `2026-08-30 03:40 +08:00`
- Result: `pass`
- Scope: 14/40 candidate 文档（批次 1：模型族 + 引擎）

## 产出清单（全部 lint `[ok]`）

| 文档 | 模式覆盖 | 关键 L1 证据 |
|---|---|---|
| `model-families/anima-lora-workflow-guide.md` | anima-standard-lora | sd3-lora schema、shipped Automagic preset、docs/anima-training.md（步数经验/预览/NaN 处理） |
| `model-families/anima-full-finetune-guide.md` | anima-full-finetune | anima-finetune schema、preset 排除声明；显式 unknown（无实测参数） |
| `engines/anima-fast-workflow-guide.md` | anima-fast-lora | fast preset（AdamW8bit/compile/flash、无 Automagic）、独立 runtime 与 preflight 门 |
| `model-families/sd15-lora-workflow-guide.md` | sd15-lora | lora-master 默认（dim/alpha 32、train type 默认 sdxl 陷阱）；显式无实测表 |
| `model-families/sd2-lora-conditions.md` | sd2-lora | v2/v_parameterization 分支、无专用 UI 选择 |
| `model-families/sdxl-lora-workflow-guide.md` | sdxl-lora | 模块联合（含原生 OFT）、TE1/TE2、heuristic 基线交叉引用 |
| `model-families/sdxl-derived-cohorts.md` | sdxl-lora（派生） | config_import SDXL path rules（noobxl/pony/illustrious）、base-mismatch 失败族 |
| `model-families/sd-dreambooth-finetune-guide.md` | sd15-dreambooth | dreambooth schema（LR 1e-6/TE 5e-7、reg/prior_loss、stop_text_encoder_training、save_state/resume） |
| `model-families/sdxl-full-finetune-guide.md` | sdxl-finetune | sdxl 分支 schema（TE1/TE2 5e-7、full_bf16 SDXL-only、sdxl_train.py 后端） |
| `model-families/sdxl-lora-workflow-guide.md` 修正 | — | 证据引用精确化（path rules vs prediction type 前置条件分离） |
| `model-families/flux-lora-workflow-guide.md` | flux-lora | 四资产、fp8_base 默认、dim2/alpha16、TE 缓存与 shuffle 冲突 |
| `model-families/chroma-flux-page-variant.md` | chroma-lora | model_type union、shipped preset 五字段整体性 |
| `model-families/krea2-lora-musubi-guide.md` | krea2-lora | musubi 后端、qwen3-vl 资产、官方推荐 preset、LoRA-only |
| `model-families/lumina2-known-breakage.md` | lumina2（边界） | 串行化/后端 mapping 断链、空 Civitai 层 L2 声明 |
| `model-families/hidden-and-unsupported-boundaries.md` | 5 个 hidden/unsupported entries | api.py/config_import/modules.test 证据表 |

> 注：批次 1 共 14 篇全部完成；下表 lint 为终态。

## Lint 运行（终态）

```text
python -B tools\stage2_lint.py E:\OpenSourceTeamWork\AgentAssets
=> scanned=14 failing=0 manifestCandidates=40 notYetWritten=26 exit=0
```

## 证据纪律抽查（Unit 层）

- 14/14 文档含三件套头 + Aliases + `## Sources` + `## Boundaries`。
- 零机器路径（X:/ 占位符）、零凭据形态字符串、零外部正文复制（preset 仅引用最小字段集）。
- 所有精确数值均有 L1 出处（shipped preset / schema default / 正式基线文档）；无法核实的具体值全部写作 unknown-here（Flux LR、Chroma 参数、finetune LR、SD2 参数、Krea 步数签名）。

## Gray 观察

- 候选与现役 14 篇零文件名冲突；与 `anima-fast-vs-standard.md`、`sdxl-lora-parameter-baseline.md`、`civitai-model-to-lora.md`、`curve-reading-guide.md` 为互补引用关系，未改写现役内容。
- 修正一处自引精度（SDXL prediction-type 的证据归因），作为 Unit 级证据纪律记录。

# Stage 2 Phase 2 — Batch 3 报告（datasets / parameters / training / errors）

- Date: `2026-08-30 05:50 +08:00`
- Result: `pass`
- Scope: 11/40 candidate 文档；Phase 2 全量 40/40 完成

## 产出清单

| 文档 | 核心 L1 锚点 |
|---|---|
| `datasets/preparation-checklist.md` | `validate_data_dir` 子目录正则 `^\d+_.+`、`<N>_zkz` 自动移文件（C-012 P1 知识安全）、suggest_num_repeat 档位 |
| `datasets/caption-tag-trigger-strategy.md` | CAPTION_SETTINGS 九字段（shuffle/keep_tokens/weighted 冲突警示/dropout 三件套/max_token_length） |
| `datasets/regularization-images.md` | reg 字段属 DreamBooth prior-loss 语义；LoRA 页行为 unproven-in-project |
| `parameters/resolution-bucket.md` | DATASET_SETTINGS 分辨率/桶默认、SDXL step<32 fails、家族起始分辨率逐项标证据 |
| `parameters/exposure-budget-steps.md` | 子目录 repeat 前缀、suggest 档位(≤10→7/11-50→5/51-100→3/其他→1)、max_train_epochs=10、家族步数锚点逐项带 tag |
| `parameters/optimizer-scheduler-guide.md` | 20 项优化器联合、Prodigy LR=1 诊断、DAdapt×constant 诊断、EmoSens schema 内嵌 1.0 提示、min_snr=5、loss_type |
| `parameters/cache-precision-guide.md` | 精度/缓存默认表、`params.ts` 四组硬冲突、lowram 反直觉语义、失效重扫纪律（标 operational） |
| `training/preview-sampling-evaluation.md` | PREVIEW_IMAGE 全块（enable_preview 默认 false、prompt_file 覆盖语义、sampler 15 联合、seed 2333）、Anima 1024/CFG4.5/40/42 文档约定、"预览不能证明什么" |
| `training/checkpoint-selection.md` | save 节奏二选一、save_state×resume 契约范围（LoRA 页等价=unknown）、network_weights≠resume |
| `training/repro-publishing-workflow.md` | seed/日志表面（tensorboard 默认、logging_dir）、verbatim base/trigger、自管 hash、托管内容通道边界区分 |
| `errors/oom-performance-playbook.md` | 六阶段故障定位、契约内梯子（cache→精度→梯度检查点→batch/accum→8bit→分辨率→dim）、反梯子警示、VRAM 数字零承诺 |

## 过程中文档修正（batch 1/2 回流）

- `flux-lora-workflow-guide.md`：模块联合修正为 `networks.lora_flux / networks.oft_flux / lycoris.kohya`（`flux-lora.ts:52` 实测，此前误写 networks.lora）。
- `krea2-lora-musubi-guide.md`：按 C-013 在 preset 数值节加措辞纪律（项目 preset ≠ 官方事实）。
- `sdxl-lora-workflow-guide.md`：证据归因精确化（path rules 与 prediction-type 前置分离）。
- `datasets/caption-tag-trigger-strategy.md`：权重语法示例改写规避 lint 误报（详见 Phase 3 lint 记录）。

## Lint

终态见 Phase 3 报告（全阶段一次冻结运行）。

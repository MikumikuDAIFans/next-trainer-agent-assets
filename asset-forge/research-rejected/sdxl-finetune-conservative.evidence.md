# sdxl-finetune-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `sdxl-finetune-conservative.toml`（DreamBooth 页 sdxl-finetune train type）· Evidence status: L1 项目契约（schema 默认 + 家族公共事实），无实测效果声明
- Aliases / 检索关键词: sdxl finetune 模板, 全量微调模板, TE1 TE2

## Field-by-field rationale

| 字段 | 值 | 来源 | 标签 |
|---|---|---|---|
| `model_train_type` | `sdxl-finetune` | `dreambooth.ts` 页面默认联合；`config_import.py` DREAMBOOTH_TRAIN_TYPES | L1 契约 |
| `learning_rate` | `1e-6` | schema default | L1 默认（非实测最优） |
| `learning_rate_te1` / `learning_rate_te2` | `5e-7` | schema 字段（ViT-L / BiG-G 独立 TE LR） | L1 默认 |
| `resolution` | `"1024,1024"` | SDXL 家族公共事实 + `sdxl-full-finetune-guide.md` 明示"勿静默继承 512" | 家族事实，导入时按底模校正 |
| `optimizer_type` | `AdamW8bit` | schema union default | L1 默认 |
| `save_state` | `true` | finetune 长跑续训契约（`save_state`/`resume` 配对） | L1 契约 |
| `save_every_n_epochs` | `2` | schema default | L1 默认 |
| `noise_offset` | `0.1` | schema note "如果启用推荐为 0.1"；本页全权重训练更易曝光/暗部漂移 | L1 note（可选开关，卡内标注可删） |

## Deliberately NOT set（unknown-here）

- `gradient_accumulation_steps`、`max_data_loader_n_workers`：环境相关，无产品级默认推荐可引。
- `stop_text_encoder_training`：sd-dreambooth 分支字段；sdxl-finetune 用 TE1/TE2 LR 表达冻结意图（设 0 等价冻结=无契约支持，不猜）。
- `prior_loss_weight`/`reg_data_dir`：prior-loss 属 sd-dreambooth 分支语义（`datasets/regularization-images.md`）。

## Validator & diff expectations

- `validate_config_import("dreambooth", cfg)` 期望 `result="ok"`；redirect/reject 均视为失败移出候选。
- 归一化 diff 审查重点：`model_train_type` 保留、无意外注入字段。

## Boundaries

- 全量权重更新：磁盘/显存/遗忘风险高于 LoRA；效果不承诺；固定提示对比未触及底模是硬要求（页面指南纪律）。
- `full_bf16` 等 SDXL-only 精度开关为实验项，故意不进保守模板。
- 无路径字段：数据集与底模路径导入时由用户填写，模板不占位。

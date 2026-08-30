# sd-dreambooth-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `sd-dreambooth-conservative.toml`（DreamBooth 页 SD1.x/2.x 分支）· Evidence status: L1 项目契约（schema 默认）；无出厂 preset、无实测记录
- Aliases / 检索关键词: dreambooth 模板, sd-dreambooth, train_db, 1e-6

## Field-by-field rationale

| 字段 | 值 | 来源 | 标签 |
|---|---|---|---|
| `model_train_type` | `sd-dreambooth` | `dreambooth.ts:4-24`；`config_import.py` DREAMBOOTH_TRAIN_TYPES | L1 契约 |
| `learning_rate` | `1e-6` | schema default（比 LoRA 低约 3 个数量级——本页核心教学点） | L1 默认 |
| `learning_rate_te` | `5e-7` | schema default | L1 默认 |
| `resolution` | `"512,512"` | schema default（SD1.x 类面积） | L1 默认 |
| `train_batch_size` | `1` | schema default | L1 默认 |
| `max_train_epochs` | `10` | schema default | L1 默认（非实测轮数） |
| `save_state` | `true` | `save_state`/`resume` 配对续训契约 | L1 契约 |
| `save_every_n_epochs` | `2` | schema default | L1 默认 |

## Deliberately NOT set（unknown-here）

- `reg_data_dir` / `prior_loss_weight`：正则化决定属于数据集设计（`datasets/regularization-images.md` 决策表），不预埋。
- `stop_text_encoder_training`、`noise_offset`/multires：可选技术项，无产品默认倾向证据；留给用例。
- `v2` / `v_parameterization`：仅 SD2.x 底模需要（`sd2-lora-conditions.md` 同一纪律）；模板不猜底模。
- `optimizer_type`：继承 union default（AdamW8bit），不显式锁死。

## Validator & diff expectations

- `validate_config_import("dreambooth", cfg)` 期望 `result="ok"`；redirect/reject 失败出局。
- 归一化 diff 审查：无注入 train type 变更；`model_train_type` 保持 `sd-dreambooth`。

## Boundaries

- 输出是整模型，非 LoRA；"能出 LoRA"为契约否定项。
- 全部数值是 schema 默认 = 契约起点，不是实测推荐；从下往上扫描并记录（EDD）。
- 真人/受版权主体训练的合规责任在使用者。

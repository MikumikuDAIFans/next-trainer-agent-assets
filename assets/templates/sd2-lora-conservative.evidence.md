# sd2-lora-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `sd2-lora-conservative.toml`（LoRA master 页 SD2.x 条件支持分支）· Evidence status: L1 项目契约（schema v2 分支字段）；无出厂 SD2 preset、无实测表
- Aliases / 检索关键词: sd2 模板, v2, v-pred, sd-lora 分支

## Field-by-field rationale

| 字段 | 值 | 来源 | 标签 |
|---|---|---|---|
| `model_train_type` | `sd-lora` | SD2.x 无独立页面；条件支持 = `sd-lora` + v2 分支（`lora-master.ts:12-23`、support-matrix `sd2-lora`） | L1 契约 |
| `v2` | `true` | schema note：SD 2.0 及以后底模需要 | L1 契约 |
| `v_parameterization` | `true` | schema v2 分支字段；适用 768-v 类底模 | L1 字段 + 底模规格校正指引（TOML 内注释） |
| `resolution` | `"768,768"` | SD 2.1-base 为 768 类模型 | 家族公共事实（按实际底模校正） |
| `enable_bucket` / `bucket_no_upscale` | `true/true` | 共享 defaults | L1 默认 |
| preview 768 块 | 见 TOML | 家族面积类，同 Flux 偏离逻辑 | 契约默认 + 记录在案的偏离 |

**为什么单独立模板（反伪多样性答辩）**：与 `sd15-lora-conservative` 的差异是字段级契约对（`v2`/`v_parameterization`）与面积类，不是改名字；这一对正是 SD2 支持判定中"conditional"的全部技术内容。

## Deliberately NOT set（unknown-here）

- LR / TE LR / dim / alpha / steps：无出厂 preset、无实测 SD2 表（`sd2-lora-conditions.md` 同一空缺纪律）。
- `scale_v_pred_loss_like_noise_pred`：v-pred 相关但仅特定底模需要；让使用者按底模规格显式添加，不预埋。

## Validator & diff expectations

- `validate_config_import("sd-lora", cfg)` 期望 `ok`；若被判 `sdxl-lora`（页面默认 train type）而 redirect，即失败——这正是显式 `model_train_type="sd-lora"` 要防的坑。
- 归一化 diff 关注：`v2`/`v_parameterization` 必须保留。

## Boundaries

- v-pred 判定来源只能是底模自身发布规格；文件名不是证据。
- 模板不声称"SD2 一等支持"——措辞保持 conditional（矩阵冻结等级）。

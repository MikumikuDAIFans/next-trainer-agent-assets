# flux-lora-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `flux-lora-conservative.toml`（Flux LoRA 页合同脚手架）· Evidence status: L1 项目契约（schema 默认值显式化）；核心训练参数故意空缺
- Aliases / 检索关键词: flux 模板, flux-lora, 合同脚手架, C-014

## Field-by-field rationale

| 字段 | 值 | 来源 | 标签 |
|---|---|---|---|
| `model_train_type` | `flux-lora` | `flux-lora.ts` fixed type；PAGE_SPECS `flux-lora` | L1 契约 |
| `timestep_sampling` | `"sigmoid"` | `flux-lora.ts` default | L1 默认 |
| `fp8_base` | `true` | `flux-lora.ts` default memory path | L1 默认（勿盲关） |
| `resolution` | `"768,768"` | `flux-lora.ts` default | L1 默认 |
| `enable_bucket` / `bucket_no_upscale` | `true/true` | 共享 DATASET_SETTINGS defaults | L1 默认 |
| `enable_preview` + 768 preview | 见 TOML | 有意偏离共享 preview 默认 512（家族面积类），preview 字段本身为共享块 defaults | 契约默认 + 记录在案的偏离 |

## Deliberately NOT set（unknown-here — 本页是 C-014 的正面执行案例）

- `learning_rate`/`unet_lr`/`text_encoder_lr`：无出厂 Flux preset、无实测表 → 模板给任何数都是捏造。
- `network_dim`/`network_alpha`：schema 携带 2/16，但冲突台账 C-014 明令"schema 默认不得直接当经验模板"；此处刻意不复制，改由使用者按 sweep 协议确立。
- `max_train_epochs`/`max_train_steps`：曝光预算依赖数据集（Flux 行在曝光文档中为 unknown）。
- 四资产路径（`pretrained_model_name_or_path`/`ae`/`clip_l`/`t5xxl`）：必填但属机器状态，导入时填写；模板零路径。

## Validator & diff expectations

- `validate_config_import("flux-lora", cfg)` 期望 `ok`；`redirect`（被判为其他家族）或 `reject` 失败出局。
- 归一化 diff 关注：路径缺失不应导致 reject（validator 无路径存在性检查）；若 normalize 注入资产默认路径（`./sd-models/...`），记录为观察项而非模板内容。

## Boundaries

- 本模板是"能安全导入的合同脚手架"，不是效果推荐；发布前必须带自己的 sweep 记录。
- FP8 量化底模×`fp8_base` 交互无质量等价测量；不做两侧质量声明。

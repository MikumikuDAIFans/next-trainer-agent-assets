# chroma-lora-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `chroma-lora-conservative.toml`（Flux 页 model_type=chroma 变体）· Evidence status: L1 项目契约（出厂 preset 五字段整体 + schema union）
- Aliases / 检索关键词: chroma 模板, model_type chroma, guidance 0, raw prediction

## Field-by-field rationale

| 字段 | 值 | 来源 | 标签 |
|---|---|---|---|
| `model_train_type` | `flux-lora` | Chroma 无独立页面；`flux-lora.ts` `model_type` union | L1 契约 |
| `model_type` | `"chroma"` | `config/presets/chroma.toml` | L1 出厂 preset |
| `apply_t5_attn_mask` | `true` | 同上 | L1 出厂 preset |
| `timestep_sampling` | `"sigmoid"` | 同上 | L1 出厂 preset |
| `model_prediction_type` | `"raw"` | 同上 | L1 出厂 preset |
| `guidance_scale` | `0.0` | 同上 | L1 出厂 preset |
| `fp8_base`/`resolution`/bucket/preview | Flux 脚手架 | `flux-lora.ts` defaults（与 flux-lora-conservative 同来源） | L1 默认 |

**整体性规则**：五字段是变体契约单元（cherry-pick 部分字段=破坏 preset 编码的变体合同），这也是本模板相对 flux-lora-conservative 的字段差异证据——不是改输出名的伪多样性。

## Deliberately NOT set（unknown-here）

- LR / dim / alpha / horizon：出厂 preset 未给出（preset 只含变体单元），无实测表 → 与 Flux 模板同一空缺纪律（C-014）。
- Chroma 资产路径：四资产字段导入时填写。

## Validator & diff expectations

- `validate_config_import("flux-lora", cfg)` 期望 `ok`（chroma 的 t5xxl/clip_l/ae 路径规则同样命中 Flux 家族，但本模板不含路径，判定应由显式 train type 驱动——正是显式 `model_train_type` 的价值点）。
- 归一化 diff 关注：`model_type=chroma` 必须原样保留（重导入丢失变体位是最大陷阱）。

## Boundaries

- 不把 Chroma 描述为"又一个 Flux checkpoint"：prediction/guidance 单元不同（`chroma-flux-page-variant.md`）。
- 不承诺逐底模差异；preset 之外的 Chroma 内部主张全部 unknown-here。

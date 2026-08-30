# krea2-lora-conservative — evidence card

- Version: `2026-08-30` · Scope: 候选模板 `krea2-lora-conservative.toml`（Musubi 引擎 Krea 2 页）· Evidence status: L1 项目契约（出厂 preset 字段整体 + 页面 schema defaults）；措辞受 C-013 约束
- Aliases / 检索关键词: krea2 模板, musubi, fp8 pair, rank 32

## Field-by-field rationale

| 字段组 | 值 | 来源 | 标签 |
|---|---|---|---|
| train type | `krea2-lora` | `krea2-lora.ts` fixed；PAGE_SPECS `krea2-lora` | L1 契约 |
| `network_dim/alpha` | 32/32 | `config/presets/krea2-lora.toml` | L1 出厂 preset |
| `resolution` | `"1024,1024"` | preset = schema default 双命中 | L1 |
| `train_batch_size`/`gradient_checkpointing` | 1/true | preset（grad ckpt 亦是页面 default true） | L1 |
| `optimizer_type` | `AdamW8bit` | preset；页面 optimizer union 仅 `AdamW|AdamW8bit|Adafactor` 三选 | L1 |
| `learning_rate` / `lr_scheduler` | `"1e-4"` / `constant` | preset（constant 也是页面默认 scheduler） | L1 出厂 preset |
| `mixed_precision` | `bf16` | 页面 union 仅 bf16 | L1 硬约束 |
| `fp8_base`+`fp8_scaled` | true/true | preset = schema defaults；schema 钉"只开一个会训不起来" | L1 硬约束（成对，勿拆） |
| `max_train_epochs`/`save_every_n_epochs`/`save_precision` | 16/2/`bf16` | preset（save_precision 页面默认也是 bf16） | L1 |
| `timestep_sampling`/`sigmoid_scale`/`discrete_flow_shift` | sigmoid/1.0/1.0 | preset = schema defaults | L1 |
| preview 块 | 1024/4.5/28/42/每 2 epoch | 页面 preview defaults（Turbo 采样时自动降 CFG1/8 步为 schema 行为） | L1 默认 |

## 措辞纪律（C-013）

- 出厂 preset 的 description 自labeling"官方推荐"；Stage 1 未检索到外部 Krea/Musubi 官方来源核实。本卡与模板一律引用为**项目出厂 preset 值**，不写"官方推荐值"。

## Deliberately NOT set（unknown-here）

- `turbo_dit` / `blocks_to_swap`：互斥对，且属部署选择。
- `min_timestep`/`max_timestep`：底模分布相关，无产品默认。
- 资产路径（dit/vae/text_encoder）：运行时/插件环境就绪后由用户填写；Musubi 运行时缺失时页面本身会 preflight 拒绝。

## Validator & diff expectations

- `validate_config_import("krea2-lora", cfg)` 期望 `ok`。
- 归一化 diff 关注：fp8 对、bf16、dim/alpha 原样；若 normalize 注入 `./sd-models/krea2/...` 默认资产路径，记为观察项。

## Boundaries

- 运行时未就绪 ≠ 模板失效：可导入性与可训练性是两个门（清单"不执行训练"）。
- LoRA-only 页面；无实测步数/损失签名可引；效果不承诺。

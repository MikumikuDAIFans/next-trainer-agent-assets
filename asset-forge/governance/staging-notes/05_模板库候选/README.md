# 候选模板库（Stage 3 制品区）

- Version: `2026-08-30`
- 状态：候选（未迁移）。正式 `agent-assets/assets/templates/`（4 份）未被改写；本目录 13 份候选模板与其文件名零冲突。

## 格式合同（对齐正式资产风格）

- 顶层 TOML、**最小差异**式经验模板：只写有证据的字段，页面默认值留给页面。
- 必含头部键：`template_version`、`scope`、`base_model`、**显式 `model_train_type`**（不依赖 scope 推断，杜绝 `[skip]`）。
- 配套证据卡 `<stem>.evidence.md`：每个值 = 选择理由 + 证据标签（shipped preset / schema default / 家族公共事实 / formal 基线及其原标签）；显式列出**故意不写的字段**及 unknown-here 原因。
- 禁止：机器绝对路径（本目录模板完全不写路径字段）、token/`wandb_api_key`、数据集真名、方向性"神参数"。
- `research-rejected/`：被否草案 + 拒绝理由；候选根目录零 reject/skip。

## 命名与覆盖

- 命名 `<family>-<purpose>-<variant>.toml`；覆盖判定见 `template-coverage-matrix.csv`。
- 最小必要原则：正式模板已覆盖 conservative 位的 4 页不重复造轮（伪多样性是清单禁止项）；候选填缺口（Flux/Chroma/Krea2/SD2-branch/DreamBooth/SDXL-finetune）。

## 决策记录（对应任务书 open question）

- 全量微调页面**进入模板库**：以"无路径最小差异"形式编码 LR/TE/save_state 等契约默认，路径由用户导入时自填——回避机器路径占位问题，同时页面归属由真实 validator 证明。
- `validate_config_import` 返回 `ok|redirect|reject`：redirect 与 skip 一律**不算 pass**（C-015 纪律）。
- 模板证明契约，不证明效果；效果声明需要实测（EDD）。

## 校验

- 工具：`tools/stage3_validate_templates.py`（用宿主 `project\.venv-dev` Python `-B` 调真实 `validate_config_import`）；命令与完整输出见 `06_评测与校验/evidence/stage-3/`。
- Stage 7 增量：`sd-dylora-conservative.toml` 由 `lora-master` schema 的 `networks.dylora` 分支证明；其余外部算法仍为知识/比较证据，未越过 validator 门。

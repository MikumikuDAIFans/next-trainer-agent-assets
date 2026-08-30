# Failure report F-S3-001 — sdxl-finetune 模板被真实 import validator 拒绝

- Date: `2026-08-30` · Severity: **P2**（不阻断：无用户流程回归；模板侧已按纪律出局）
- Disposition: 模板移入 `05_模板库候选/research-rejected/`；候选根目录零 reject/redirect；冲突登记 **C-016**

## 现象

`sdxl-finetune-conservative.toml`（含 `learning_rate_te1/te2 = 5e-7`，schema 合法默认）在其归属页 DreamBooth 上被真实 `validate_config_import` 判 `redirect`，永远无法 `ok`。

## 根因（源码级）

1. `SDXL_CONFIG_MARKERS = {sdxl_prediction_type, learning_rate_te1, learning_rate_te2}`（`mikazuki/utils/config_import.py:70-74`），每字段计 3 分，`≥2` 即采用推断家族。
2. `analyze_train_type` 以 sdxl-lora 家族名义收编这些字段；`validate_config_import` 用 `config_type = inferred or explicit`——**推断压过显式** `model_train_type="sdxl-finetune"`。
3. DreamBooth 页 accepted = `{sd-dreambooth, sdxl-finetune}`：推断值 `sdxl-lora` 不在内 → `redirect → /lora/master.html`。
4. 探测定律（`$env:TEMP/probe_finetune.py`，宿主 venv 运行）：

| 配置 | dreambooth 页 | lora-master 页 |
|---|---|---|
| 无 te1/te2 | **ok**（类型保持 sdxl-finetune） | ok（类型保持） |
| 带 te1/te2 | redirect（类型字段虽仍 sdxl-finetune，结果不可导入） | **ok 但类型漂移为 sdxl-lora**（LoRA 化，静默！） |

第 4 行的 master 路径比 redirect 更危险：静默把全量微调配置规范化成 LoRA 配置。

## 为什么不"绕过"

- 从模板删除 te1/te2 可换到 ok——但那正是本模板的全部差异化教学价值，为凑数换 pass 属于削弱验收（清单禁止项 1 的精神）。
- 改报 master 页通过 = 掩埋类型漂移。
- 处置 = 候选出局 + failure report + 冲突登记 + 回归断言（runner `REJECTED_EXPECTATIONS` 每次运行断言 redirect 事实仍成立；若产品修复，断言变红即为信号）。

## 影响面与后续

- 用户侧：在 DreamBooth UI 内直接调 te1/te2 训练不受影响（本问题只在**配置导入/模板复用**路径）；但导出→再导入闭环会踩坑。属产品 import 校验的 train-type 推断对"同族不同粒度"的盲区。
- Stage 3 出口口径：sdxl-finetune 页在覆盖矩阵标记 `rejected-import-quirk`，不记为"候选覆盖"；未来产品修复后（markers 或 config_type 优先级变化）可复活模板，由断言红灯提示复验。
- 关联知识：`04_知识库候选/model-families/sdxl-full-finetune-guide.md` 已含 TE1/TE2 字段指导；本发现暂不改写该文档（UI 契约仍真），待产品修复或官方说明后再更新。

# Stage 3 Phase 3 报告 — 宿主校验、归一化差异与冻结

- Date: `2026-08-30` · Result: `pass`（候选根目录零 reject/redirect/skip；1 例真实失败按纪律出局并登记 C-016）

## 真实宿主 validator（非仿制）

- 运行体：`project\.venv-dev\Scripts\python.exe -B tools\stage3_validate_templates.py <staging> <project>`，直接 import `mikazuki.utils.config_import.validate_config_import`。
- 强页证明：每份候选在其用户实际落地的 PAGE_SPECS 页上判 `ok`（sd2 用 `lora-master` 强页而非弱键 `sd-lora`——后者无页面规则属弱通过，已记观察）。
- 阴性对照：5/5 在错误页均 `redirect`（证明 gate 能红）；deny-draft 断言：sdxl-finetune 在 dreambooth 页恒定 `redirect`（回归红灯机制）。
- normalized diff：5/5 候选 `+0/-0/~0`（无注入、无删除、无值变、无类型漂移）；每份 JSON 工件在 `phase-3/*.json`。
- Zero-short：候选复制到空 temp 目录重跑全套（含断言）——全同结果，排除机器路径依赖。

## 双视角输出

- `runner-output.txt`：自研 gate 两轮全绿（主目录 + zero-short），exit 0。
- `formal-gate-second-opinion.txt`：正式资产自带 `validate-templates.py` 对候选目录 5/5 `[ok]` exit 0。
- 治理观察：正式脚本把 `model_train_type` 直接当 page key，`sd-lora`/`sd-dreambooth` 落到"无规则→ok"弱路径；本阶段以强页 runner 为主证明，正式脚本仅作第二意见（不改正式脚本——只读边界）。

## 失败处理（唯一）

- F-S3-001：sdxl-finetune+TE1/TE2 导入必 redirect、master 页 ok 但类型静默漂移为 sdxl-lora。模板入 `research-rejected/`，冲突登记 **C-016**（P2），runner 常驻断言。未用"删字段换 pass"的削弱路径。

## 冻结态（Stage 3 出口）

| 指标 | 值 |
|---|---|
| 候选根目录 TOML | 5（chroma/flux/krea2/sd-dreambooth/sd2） |
| validator | 5/5 ok（强页）+ 5/5 阴性对照 + deny 断言 ok |
| normalized diff | 5/5 全零变更 |
| reject/skip 于候选根目录 | 0 |
| research-rejected | 1 对（含 failure report 交叉引用） |
| 与正式 4 模板文件名冲突 | 0（runner 碰撞守卫） |

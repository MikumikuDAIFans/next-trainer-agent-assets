# Stage 3 Phase 1/2 报告 — 覆盖设计与证据卡编制

- Date: `2026-08-30` · Result: `pass（phase-3 前状态）`

## Phase 1：页面与模板覆盖设计

- 产物：`05_模板库候选/template-coverage-matrix.csv` + `README.md`（格式合同/命名规范/决策记录）。
- 输入闭环：validator `PAGE_SPECS`/accepted 集合（源码逐键核对）× Stage 0 冻结支持矩阵 17 entries × 正式 4 模板覆盖面。
- 判定：4 页 covered-formal（不重造，防伪多样性）；6 候选（flux/chroma/krea2/sd2-branch/sd-dreambooth/sdxl-finetune）；7 类 blocked（no-contract/broken/legacy/hidden/alias/unsupported×2），每行有 notes 依据。

## Phase 2：参数选择与证据卡

- 5 份候选 TOML + 5 份 `.evidence.md`（成对，非 toml 扩展名）+ 1 份最终出局的 sdxl-finetune 对（保留在 `research-rejected/`）。
- 值纪律：仅三类来源可入文——出厂 preset（chroma 五字段整体、krea2 全量）、schema default（显式化并标注"非实测最优"）、家族公共事实（768/1024 面积类，标校正指引）；unknown-here 字段在 TOML 注释与卡片双重显式（Flux LR/dim 是 C-014 的正面执行案例）。
- 零路径字段、零凭据形态、零数据集真名（runner lint 内嵌 secret/drive-path/path-bearing-field/碰撞/配对检查全绿）。
- 措辞纪律：krea2 preset"官方推荐"按 C-013 一律引用为项目出厂值。

## 过程修正

- 知识回流：`krea2-lora-musubi-guide.md` 增补页面 schema 钉死事实（fp8 对成对约束、bf16-only、optimizer 三选、16 倍数、preview 默认形、bucket_no_upscale 页内默认 false）——模板编写中发现的更强证据回写候选知识。

# Stage 2 Phase 2 — Batch 2 报告（network-algos + directions）

- Date: `2026-08-30 04:35 +08:00`
- Result: `pass`
- Scope: 15/40 candidate 文档（6 network-algos + 9 directions）；累计 29/40

## 产出清单（全部 lint `[ok]`）

network-algos（6）：
- `lokr-guide.md` — Anima 已验证路径 vs LyCORIS 路径分层；`lokr_factor=-1` 语义、train_norm 自动禁用（Anima LoKr 防采样崩溃）与 dropout 例外均引自 `shared.ts` schema 描述
- `tlora-anima-guide.md` — Anima-only；docs 表格字段/默认值/行为预期；推理兼容说明
- `dylora-guide.md` — 双入口（native `networks.dylora`+`dylora_unit` vs LyCORIS `algo=dylora`）严格区分；无 slice-export 承诺
- `oft-guide.md` — 三分法（SDXL native / Flux-native `networks.oft_flux` / LyCORIS diag-oft+boft）；SD1.x 硬拒绝为 diagnostic 事实
- `lycoris-family-guide.md` — 8 algo 联合、双容量对（linear vs conv）、字段例外钉死、逐页可用性表
- `anima-schema-only-adapters.md` — LoRA-FA/VeRA/LoHa/PiSSA 三档失效分层（静默同化 / 切模块未证 / 无实现），回答话术模板

directions（9）：
- `character-identity.md`、`style-training.md`、`object-product-concept.md`、`clothing-accessory.md`、`pose-expression-features.md`、`scene-domain-migration.md`、`utility-correction-lora.md`、`multi-concept-training.md`、`slider-erasure-boundaries.md`
- 全部继承 taxonomy 支持等级：12 个数据目标方向按 standard objective 写数据/评测设计；slider/erasure 边界文档 + ControlNet/TI 指向 hidden/unsupported 文档；零"把数据倾向写成控制能力"表述

## Lint 运行（终态）

```text
python -B tools\stage2_lint.py E:\OpenSourceTeamWork\AgentAssets
=> scanned=29 failing=0 manifestCandidates=40 notYetWritten=11 exit=0
```

## Lint 工具修正记录（本轮 1 次）

- `style-training.md` 首跑 FAIL：`S2 credential-looking string`。人工核查为**误报**：正文短语 "per caption token:" 后接换行与有序列表 "1." 被 `token\s*[:=]\s*[A-Za-z0-9]` 跨行匹配。
- 修正：S2 正则的空白类从 `\s*` 收紧为 `[ \t]*`（不跨行）。真实凭据形态均为单行赋值，检测能力不降。修正后全量重跑 29/29 pass。此为 lint 规则缺陷修复，非文档放宽。

## 证据纪律抽查

- 每篇精确数值仅出现在（a）shipped preset/schema default/共享 schema 描述（标 L1）或（b）现役基线文档按其原证据标签引用；其余全部 unknown/L3。
- `slider-erasure-boundaries.md` 引用 Concept Sliders arXiv:2311.12092 时保留 source registry 的 "research lead only / verified-title" 状态，未升级。
- 0 处将 Civitai 观察用作参数证据（Stage 1 structured=0 被反向引用为"无参数证据"）。
- Gray：与现役 14 篇零冲突；`wd14-tagging-guide`、`common-errors`、`dim-alpha`、`learning-rate`、`curve-reading` 均为引用关系。

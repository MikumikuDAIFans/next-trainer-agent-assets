# InstructPix2Pix 指令编辑目标边界

- Version: `2026-08-30`
- Scope: 说明 instruction-based image editing 与角色/风格 LoRA 的目标差异，防止把编辑数据误标为普通概念训练。
- Evidence status: L1 paper metadata (arXiv:2211.09800 HTTP 200); product support remains determined by current route/schema.
- Aliases / 检索关键词: InstructPix2Pix, instruction editing, 编辑目标, 数据目标, 方向分类

## 分类规则

编辑数据包含输入图、编辑指令和目标图，监督目标是条件变换；角色/画风 LoRA 通常学习可触发的概念或风格残差。两者在数据字段、评测问题和过拟合风险上不同，应在方向矩阵中分开。

## 与 Next Trainer 的处理

当前支持矩阵未将 InstructPix2Pix 作为独立训练页面时，只能记录为研究/边界知识，不能生成可导入模板。若未来出现新 route，必须走 change control 与 Stage 0 重新盘点。

## Sources

- InstructPix2Pix paper: https://arxiv.org/abs/2211.09800 (L1 official)
- 当前方向分类: `../../01_训练器能力盘点/training-direction-taxonomy.md` (L1 project)

## Boundaries

- 论文存在不等于产品支持；不推断 hidden route。
- 不提供未经验证的字段、默认值或训练参数。

## Eval

- Question: “编辑指令数据能否直接套用角色 LoRA 模板？”
- Expected answer: 不能，目标函数与数据合同不同，需独立页面和证据。

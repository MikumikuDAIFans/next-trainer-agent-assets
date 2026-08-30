# 训练方向分类：不要混淆模型、算法与目标

- Version: `2026-08-29`
- Scope: Next Trainer 当前模型训练方向与支持边界
- Evidence status: L1 项目契约 + 领域分类；具体方法效果将在 Stage 1 以官方资料补证

## 四条正交轴

| Axis | 问题 | 当前值示例 |
|---|---|---|
| 模型/架构 | 在什么底模上训练？ | Anima、SD1.x/2.x、SDXL、Flux/Chroma、Krea 2、Lumina 2（当前断链） |
| 训练粒度 | 更新多少权重？ | adapter/LoRA、DreamBooth/model finetune、full DiT/full model |
| Adapter 算法 | 用什么参数化网络？ | LoRA、LoKr、LoHa、DyLoRA、OFT、T-LoRA、VeRA、LoRA-FA、LyCORIS 等 |
| 数据/监督目标 | 想学会什么？ | 角色、画风、服装、物体、特征、姿态、表情、概念、修正、slider 等 |

“角色 LoRA”和“LoKr”不是并列概念：前者是目标，后者是 adapter 算法。

## 训练方向支持表

| Direction | 当前产品支持含义 | Support class | 主要决定因素 |
|---|---|---|---|
| 角色/身份 | 所有端到端可用 LoRA 页面都可用角色数据训练；Anima 有角色 preset | standard dataset objective；Anima explicit preset | 身份一致性、触发词、caption 去泄漏、姿态/服装覆盖 |
| 画风/风格 | 所有可用 LoRA 页面可训练视觉风格；Anima 有 style preset | standard dataset objective；Anima explicit preset | caption 是否保留/移除内容、风格多样性、底模偏置 |
| 人物/物体概念 | 标准 LoRA 或 full finetune 可学习一个 subject/concept | standard dataset objective | 触发词、类先验、负样本/正则化、数据多样性 |
| 单物体/道具/产品 | 标准 LoRA 数据目标；Anima 角色 preset 文案明确包含道具 | standard dataset objective | 视角、尺度、背景、材质、品牌/版权边界 |
| 服装/套装/配饰 | 标准 LoRA 数据目标；不是独立 adapter | standard dataset objective | 身份与服装解耦、caption token、遮挡和视角 |
| 发型/颜色/材质/局部视觉特征 | 标准 LoRA 数据目标 | standard dataset objective | 局部特征可见性、与身份/背景共现偏差 |
| 表情/情绪 | 标准 LoRA 数据目标 | standard dataset objective | 表情标签、强度梯度、身份保持 |
| 姿态/动作/构图 | 标准 LoRA 可学习，但不等同 ControlNet | standard dataset objective with control limits | 姿态分布、caption、构图偏差；没有条件控制图训练页 |
| 光影/上色/质感 | Anima style preset 明示；其他 LoRA 页面同样为标准风格目标 | standard dataset objective | 内容与风格解耦、颜色/曝光分布 |
| 环境/场景/领域迁移 | LoRA 或支持的 full finetune 可做；无单独页面 | standard objective / full-model option | 数据规模、范围宽度、灾难性遗忘 |
| 修正/增强/细节/质量 LoRA | 可用标准 LoRA 数据设计训练，但没有专用 loss/page | generic utility LoRA | 对照数据、过拟合、可解释评测 |
| 多概念组合 | 可在一个数据集中训练，但不是“自动可组合”保证 | generic multi-concept objective | token 冲突、样本平衡、概念泄漏 |
| Slider LoRA（连续强度/方向） | 当前没有 paired-positive/negative、slider loss 或专用数据 contract | not first-class | 不能把普通 LoRA 权重滑动或 `enable_base_weight` 当成校准 slider 训练 |
| 概念擦除/抑制 | 当前没有专用 erasure loss/workflow | not first-class | 标准负面 caption 不等于模型概念擦除 |
| ControlNet/LLLite | 仓库含底层脚本，但当前工作台/API 不暴露 | unsupported product workflow | 需要条件图数据 contract、schema、mapping 和测试 |
| Textual Inversion/XTI | 仓库含脚本，但当前工作台/API 不暴露 | unsupported product workflow | 需要 embedding 专用页面/参数/验证 |

## Slider LoRA 的特别说明

当前 schema 中的 `enable_base_weight`/`base_weights` 是把已有 adapter 权重作为训练基线/差异炼丹输入；它并没有提供“正负概念对”“连续属性坐标”“slider 专用损失”或校准评测。因此：

1. 普通 LoRA 推理时调权重，只说明强度可变化，不证明训练产物是可解释 slider。
2. 用两个端点数据训练普通 LoRA，最多可视为探索性近似，不能在知识库中称为一等 slider 支持。
3. Stage 1 应读取 Concept Sliders/相关方法的官方论文或仓库，对照当前 schema 后再写专门知识文档。

## Adapter 算法覆盖

| Algorithm family | Available pages | Notes |
|---|---|---|
| LoRA | Anima standard/Fast、SD/SDXL、Flux、Krea 2；Lumina form broken | 通用基线 |
| LoKr | Anima standard；SD/SDXL/Flux 通过 LyCORIS | Anima 有 adapter 测试和专属 preset 注入 |
| LoHa | SD/SDXL/Flux 通过 LyCORIS；Anima schema 显示但未形成后端证明 | Anima 暂不计入可验证支持 |
| T-LoRA | Anima standard only | 动态 rank schedule |
| LoRA-FA / VeRA | Anima schema 暴露，但当前都落到普通 `networks.lora_anima` 且 type 被丢弃 | 暂不计入可验证支持 |
| PiSSA init | Anima schema 暴露，固定 upstream 无实现命中 | 暂不计入可验证支持；即使实现也是初始化法，不是训练方向 |
| DyLoRA | SD/SDXL native；也有 LyCORIS algo | 不要混淆两个入口 |
| OFT | SDXL native；Flux native；Lumina form declares but broken | SD1.x native OFT 被前端诊断拒绝 |
| LoCon/IA3/GLoRA/Diag-OFT/BOFT | SD/SDXL/Flux LyCORIS | 需逐页 validator/后端兼容核对 |

## Full finetune 适用方向

全量微调更适合宽领域迁移、大规模风格/分布改变或需要更新主模型能力的场景，但数据、显存、回滚和灾难性遗忘风险显著高于 LoRA。当前 first-class full/model finetune 只包括 Anima、SD 1.x/2.x DreamBooth 和 SDXL；Flux 仅后端隐藏，Krea 2/Lumina 2 无可用工作台路径。

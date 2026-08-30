# Next Trainer 当前训练支持矩阵

- Version: `2026-08-29`
- Source commit: `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`
- Evidence status: L1 项目契约

## 结论速览

| 模型/模式 | 粒度 | Engine | Support | 主要算法/说明 |
|---|---|---|---|---|
| Anima standard | LoRA/adapter | Kohya | first-class | 已形成后端证据：LoRA、LoKr、T-LoRA；LoRA-FA/VeRA/LoHa/PiSSA 仅 schema 暴露，暂不计入可验证支持 |
| Anima Fast | LoRA/adapter | Anima Fast | conditional | LoRA only；需可选 runtime/preflight |
| Anima | full DiT finetune | Kohya | first-class | 全量 DiT，组件学习率 |
| SD 1.x | LoRA/adapter | Kohya | first-class | LoRA、DyLoRA、LyCORIS；native OFT 不允许 |
| SD 2.x | LoRA/adapter | Kohya | conditional | 共用 SD 页面，必须 `v2=true`，按模型设置 v-pred |
| SDXL 及 Pony/Illustrious/NoobXL 兼容派生 | LoRA/adapter | Kohya | first-class | LoRA、DyLoRA、OFT、LyCORIS；EPS/v-pred/RF |
| SD 1.x/2.x | DreamBooth model finetune | Kohya | first-class/conditional | SD2 仍需 v2/v-pred 条件 |
| SDXL | full finetune | Kohya | first-class | `sdxl_train.py` 路径 |
| FLUX | LoRA/adapter | Kohya | first-class | LoRA、Flux OFT、LyCORIS |
| Chroma | LoRA/adapter | Flux page | first-class variant | `model_type=chroma` |
| Krea 2 | LoRA/adapter | Musubi | conditional | fixed Krea 2 LoRA；需可选 runtime |
| Lumina 2 | LoRA form | Kohya | unsupported currently | UI/schema 存在，但 train type 串行化和后端 mapping 断裂 |
| FLUX | full finetune | backend only | backend-capable-ui-hidden | 后端脚本/mapping 有，工作台明确不暴露 |
| SD LoRA basic | simplified legacy form | Kohya | backend-capable-ui-hidden | schema/serializer 保留，当前工作台不作为独立模式 |
| Stability AI SD3 | bundled scripts only | none | unsupported | `sd3-lora` 现为 Anima legacy alias，不是 SD3 产品支持 |
| Textual Inversion/XTI | embedding | bundled scripts only | unsupported | 无工作台 module/API submit mapping |
| ControlNet/LLLite | control adapter | bundled scripts only | unsupported | 无工作台 module/API submit mapping |

## 支持等级定义

- `first-class`：工作台、schema、serialized train type、validator 和 backend 闭环。
- `conditional`：闭环存在，但依赖可选 runtime、feature flag 或隐藏模型条件。
- `backend-capable-ui-hidden`：后端或 legacy schema 能力存在，当前工作台不提供受支持入口。
- `unsupported`：端到端链断裂或仅有依赖脚本，不能当产品能力使用。
- `unknown`：源码不足以裁定；本批次没有把 unknown 升级为 supported。

## LoRA 算法不是训练方向

网络算法控制参数化方式；角色、画风、服装、物体、特征等主要由数据集、caption、触发词、采样与评测定义。同一个 `networks.lora` 可训练多种方向，同一个方向也可选择多种 adapter 算法。

## 全量微调的语义差异

- Anima：明确更新主 DiT 权重。
- SD 1.x/2.x：页面目标名为 finetune，后端是 `train_db.py` 的 DreamBooth/model fine-tuning 路径。
- SDXL：后端是 `sdxl_train.py` 全量微调路径。
- Flux：后端脚本存在，但当前工作台未暴露，不能作为正式模板目标。
- Krea 2/Lumina 2：当前没有可用全量微调工作台模式。

## 兼容子族

Pony、Illustrious、NoobXL 等在本项目中由 SDXL page/validator 的路径规则识别为 SDXL 兼容模型，不是独立 trainer。Civitai 采样时应分 cohort，但模板最终仍必须以 `sdxl-lora` validator 为准。

详细 machine-readable 记录见 `support-matrix.json`；冲突见 `support-conflicts.md`。

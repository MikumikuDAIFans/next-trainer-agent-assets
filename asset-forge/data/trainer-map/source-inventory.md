# Next Trainer 训练能力源码清单

- Source project: `E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project`
- Source commit: `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`
- Branch: `feat/pi-agent-plugin`
- Inspected on: `2026-08-29`
- Evidence status: L1 项目契约（只读源码）

## 判定方法

一个模式只有同时满足以下链路，才可标为当前产品 `first-class`：

1. 工作台 `TRAINING_MODULES` 可选；
2. schema 存在且序列化得到正确 `model_train_type`；
3. `/api/run` 能进入标准 `trainer_mapping` 或明确的特殊后端分支；
4. validator 接受对应 page/train type；
5. 没有已知阻断冲突。

可选插件运行时使模式降为 `conditional`；只有后端入口而 UI 未暴露的模式标 `backend-capable-ui-hidden`；文件存在但端到端链断裂的模式不算支持。

## 核心入口

| Surface | Source | Findings |
|---|---|---|
| Workbench domain | `frontend/src/training/modules.ts:3-43` | 6 model、3 engine、2 target、10 module |
| Route | `frontend/src/router.ts:20-57` | 统一 `/training`；旧 URL 重定向到 query selection |
| Form serialization | `frontend/src/training/params.ts:37-45` | schemaName 强制 page train type；发现 Lumina 错配 |
| Schema loader | `mikazuki/app/api.py:221-238` | `mikazuki/schema` 下所有文件均按文本载入，包括 shared/tagger/basic |
| Standard backend | `mikazuki/app/api.py:152-164` | 8 个标准 trainer mapping（含隐藏 Flux finetune） |
| Special backend | `mikazuki/app/api.py:741-838` | Anima Fast 和 Krea 2/Musubi 独立 feature/runtime/preflight 分支 |
| Unsupported guard | `mikazuki/app/api.py:845-849` | 不在特殊分支或 trainer mapping 的 train type 明确拒绝 |
| Import validator | `mikazuki/utils/config_import.py:12-211` | train type 集、alias、page specs 和 redirect targets |
| Product tests | `frontend/src/training/modules.test.ts:16-120` | 模块映射/不支持组合/legacy 规则 |
| Backend route tests | `tests/test_train_routing.py:17-38` | Anima、SD、SDXL 标准 mapping 契约 |

## 工作台模型、引擎与目标

```text
TrainingModel  = anima | sd15 | sdxl | flux | lumina | krea2
TrainingEngine = kohya | anima-fast | musubi
TrainingTarget = lora | finetune
```

`target` 只有 LoRA 与 finetune；LoKr、T-LoRA、OFT、LyCORIS 等是 LoRA 页面内部的 adapter/network algorithm，不是顶层 target。角色、画风、服装、特征、slider 等是数据/监督目标，也不是页面或 network algorithm。

## 10 个工作台组合

| Model | Engine | Target | Schema | Intended train type | Initial chain result |
|---|---|---|---|---|---|
| Anima | Kohya | LoRA | `sd3-lora` | `anima-lora` | complete |
| Anima | Anima Fast | LoRA | `anima-lora-fast` | `anima-lora-fast` | complete, optional runtime |
| Anima | Kohya | finetune | `anima-finetune` | `anima-finetune` | complete |
| SDXL | Kohya | LoRA | `lora-master` | `sdxl-lora` | complete |
| SD 1.5/2.x | Kohya | LoRA | `lora-master` | `sd-lora` | complete |
| SDXL | Kohya | finetune | `dreambooth` | `sdxl-finetune` | complete |
| SD 1.5/2.x | Kohya | finetune | `dreambooth` | `sd-dreambooth` | complete |
| Flux/Chroma | Kohya | LoRA | `flux-lora` | `flux-lora` | complete |
| Lumina 2 | Kohya | LoRA | `lumina2-lora` | intended `lumina-lora` | broken chain |
| Krea 2 | Musubi | LoRA | `krea2-lora` | `krea2-lora` | complete, optional runtime |

## Schema inventory

| Schema | Product role | Key adapter/network choices |
|---|---|---|
| `sd3-lora.ts` | Anima standard LoRA | 可验证链：LoRA、LoKr、T-LoRA；另有 LoRA-FA、VeRA、LoHa、PiSSA UI 分支但后端证明不足 |
| `anima-lora-fast.ts` | Anima Fast | LoRA only |
| `anima-finetune.ts` | Anima full DiT finetune | no adapter；component LR |
| `lora-master.ts` | SD/SDXL LoRA expert | LoRA、DyLoRA、native OFT、LyCORIS |
| `dreambooth.ts` | SD DreamBooth / SDXL finetune | full/model finetune path |
| `flux-lora.ts` | Flux/Chroma LoRA | Flux LoRA、Flux OFT、LyCORIS |
| `lumina2-lora.ts` | Lumina 2 LoRA form | Lumina LoRA、Lumina OFT、LyCORIS；submit chain broken |
| `krea2-lora.ts` | Krea 2 via Musubi | fixed Krea 2 LoRA network |
| `lora-basic.ts` | legacy simplified SD LoRA schema | no workbench module；serializer fills `sd-lora` defaults |
| `tagger.ts` | dataset tagging tool | not training |
| `shared.ts` | shared schema fragments | not a standalone page |

## Standard trainer mapping

| Train type | Trainer |
|---|---|
| `sd-lora` | `scripts/stable/train_network.py` |
| `sdxl-lora` | `vendor/sd-scripts/sdxl_train_network.py` |
| `sd-dreambooth` | `scripts/stable/train_db.py` |
| `sdxl-finetune` | `scripts/stable/sdxl_train.py` |
| `sd3-lora` | `scripts/dev/anima_train_network.py`（legacy alias，实际是 Anima） |
| `anima-lora` | `scripts/dev/anima_train_network.py` |
| `anima-finetune` | `scripts/dev/anima_train.py` |
| `flux-lora` | `scripts/dev/flux_train_network.py` |
| `flux-finetune` | `scripts/dev/flux_train.py`（后端存在，工作台不暴露） |

Anima Fast 与 Krea 2 不在该 mapping：分别在 `/api/run` 进入专用 runtime adapter。Lumina 不在 mapping，也没有特殊分支。

## Network/adapter algorithms

### SD 1.5/2.x 与 SDXL

- `networks.lora`
- `networks.dylora`
- `networks.oft`：前端诊断仅允许 `sdxl-lora`
- `lycoris.kohya`：LoCon、LoHa、LoKr、(IA)^3、DyLoRA、GLoRA、Diag-OFT、BOFT

### Anima standard

- LoRA (`networks.lora_anima`)
- LoKr (`lycoris.kohya`, algo=lokr)
- T-LoRA (`networks.tlora_anima`)

Schema 还显示 LoRA-FA、VeRA、LoHa 和 PiSSA init，但当前固定 upstream/adapter 证据不足：LoRA-FA/VeRA 都映射到普通 `networks.lora_anima`，随后 `lora_type` 被 adapter 丢弃；PiSSA 字段在固定 upstream 中无实现命中；LoHa 缺少 Anima 专属验证。因此这四项暂不计入可验证算法支持。

### Anima Fast

- 固定 `networks.lora_anima`；不支持上述多 adapter 分支。

### Flux/Chroma

- `networks.lora_flux`
- `networks.oft_flux`
- `lycoris.kohya` 的八种共享算法

### Lumina 2

- schema 声明 `networks.lora_lumina`、`networks.oft_lumina`、LyCORIS；当前端到端链路断裂，不能当作可用支持。

### Krea 2

- adapter 固定 `musubi_tuner.networks.lora_krea2`。

## Bundled but not product-exposed training code

仓库还包含 SD3、ControlNet/LLLite、Textual Inversion/XTI 等脚本，但它们没有当前工作台 module + submit mapping 闭环。它们只能标为“依赖源码内存在”，不能算当前产品支持。

尤其要注意：当前 `sd3-lora` 是 Anima 的 legacy alias，不代表当前 UI 支持 Stability AI SD3 训练。

## Phase 1 conclusion

端到端可用/条件可用链路可以从本地源码穷举。Lumina 2 和隐藏 Flux finetune 是必须在支持矩阵中单独解释的差异，后续知识和模板不得仅按 schema 文件生成。

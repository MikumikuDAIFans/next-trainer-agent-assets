# 支持矩阵验证报告

- Date: `2026-08-29`
- Source commit: `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`
- Result: `pass-with-boundary`

## 结构与源码闭环

运行：

```text
python -B tools\validate_support_matrix.py \
  --project-root E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project \
  --assets-root E:\OpenSourceTeamWork\AgentAssets
```

结果：

```json
{
  "sourceModules": 10,
  "rawModules": 10,
  "trainerMappings": 9,
  "supportEntries": 17,
  "operationalEntries": 11,
  "firstClass": 8,
  "conditional": 3,
  "hidden": 2,
  "unsupported": 4,
  "unknown": 0,
  "errors": []
}
```

校验同时检查：module tuple 完全相等、trainer mapping 文件存在、支持等级合法、ID 唯一、必填字段齐全、所有本地 evidence path 存在。

## 现有项目 contract tests

### Frontend

```text
npm test -- src/training/modules.test.ts src/training/params.test.ts src/schema/adapter.test.ts
Test Files 3 passed (3)
Tests 34 passed (34)
```

### Backend

```text
.venv-dev\Scripts\python.exe -B -m pytest -q -p no:cacheprovider \
  tests\test_train_routing.py tests\test_config_import.py tests\test_anima_backend_adapter.py
44 passed in 0.25s
```

## Page/train-type import probe

| Page | Config train type | Result | Notes |
|---|---|---|---|
| `sd3-lora` | `anima-lora` | ok | standard Anima |
| `anima-lora` | `anima-lora` | ok | alias page |
| `anima-lora-fast` | minimal `anima-lora-fast` | redirect | 缺 Fast markers；完整现有模板另测为 ok |
| `anima-finetune` | `anima-finetune` | ok | validator 可识别 |
| `lora-master` | `sd-lora` | ok | SD1/2 |
| `lora-master` | `sdxl-lora` | ok | SDXL |
| `dreambooth` | `sd-dreambooth` | ok | SD DreamBooth |
| `dreambooth` | `sdxl-finetune` | ok | SDXL finetune |
| `flux-lora` | `flux-lora` | ok | Flux/Chroma page |
| `lumina-lora` | `lumina-lora` | ok | validator 本身识别，但 run backend 仍缺 |
| `lumina2-lora` | `lumina-lora` | ok | page fallback 可识别；前端实际强制值仍错误 |
| `krea2-lora` | `krea2-lora` | ok | Musubi page |

## Anima schema-only adapter probe

对 adapter 直接输入的结果：

```text
lora    -> {"network_module":"networks.lora_anima"}
lora_fa -> {"network_module":"networks.lora_anima"}
vera    -> {"network_module":"networks.lora_anima"}
loha    -> {"network_module":"networks.loha"}
pissa   -> {"network_module":"networks.lora_anima","pissa_init":true,"pissa_method":"rsvd"}
```

结合固定 upstream 搜索：PiSSA 字段没有实现命中，LoRA-FA/VeRA 与普通 LoRA 无可观察配置差异，LoHa 无 Anima 专属回归。因此仅 LoRA/LoKr/T-LoRA 计入当前可验证算法支持。

## README/源码灰度对比

1. README 列 Anima、SD1.5、SDXL、Flux、Krea 2；源码额外注册 Lumina，但端到端断裂。
2. README 宣称 Anima LoRA/LoKr/T-LoRA，与本次可验证算法结论一致。
3. README 只宣称 Flux LoRA；源码虽有 Flux finetune backend，但工作台测试显式判 unsupported selection。

## Zero-Short

Result: `pass-with-boundary`。在新的 Python `-B` 进程中，仅给定 read-only project root、AgentAssets root 和标准库，矩阵校验可复现相同计数与零错误。支持等级和方向分类属于有证据的策展判断，不能完全由代码自动生成；其可追溯性由 evidence paths 和 conflict register 保证。

## Boundary decisions

1. Lumina、实际 SD3、Textual Inversion、ControlNet 不进入“当前可用知识/模板”操作路径。
2. Flux finetune 与 lora-basic 只记兼容/隐藏能力，不生成 first-class 模板。
3. Anima LoRA-FA/VeRA/LoHa/PiSSA 不进入可验证 adapter 模板；可在知识中作为当前 UI 陷阱说明。
4. Slider/erasure 不计专用支持。

## Source state after tests

project 与正式 agent-assets 在本轮验证结束时 `git status --short` 均无输出。本任务未修改两个只读源仓；CR-001/002 仍保留并发状态历史。


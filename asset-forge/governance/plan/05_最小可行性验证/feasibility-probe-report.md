# Feasibility Probe Report

- Date: `2026-08-29`
- Plan: `NT-ASSET-KB-TPL-20260829`
- Result: `pass-with-boundary`

## Critical Assumptions

| ID | Assumption | Existing evidence | Probe result | Decision |
|---|---|---|---|---|
| A1 | 训练能力可从源码入口穷举 | README/AGENTS 入口 | `rg` 找到 training modules、9 类 schema 文件、trainer mapping、validator、presets 和 tests；还发现 README 未列出的 Lumina 2 | pass |
| A2 | Civitai 公共 API 无 token 可访问 | 官方 API 文档 | 直连超时；经本机既有 HTTP 代理 `127.0.0.1:11809` 请求 `/api/v1/models` 与 `/model-versions/882225` 均为 HTTP 200 | pass-with-boundary |
| A3 | 训练字段缺失可被诚实检测 | 官方 model-version 响应合同 | 版本 `882225` 同时存在 `trainingDetails`/`trainingStatus` 键但值为 null；说明文本包含 rank/alpha/batch/steps/optimizer/LR/resolution 标记 | pass-with-boundary |
| A4 | 宿主 validator 可只读验证指定目录 | `validate-templates.py` 源码 | 现有 3 模板全部 `[ok]`，exit 0；未写 agent-assets | pass |

## Commands / Requests

1. 本地只读源码入口扫描：`rg --files` 与 `rg -n`，排除 cache/build 目录。
2. 官方 Civitai 文档检索：确认公共 REST API、`/models` 与 `/model-versions/{id}` 合同。
3. Civitai 实测：
   - 直连 `civitai.com` 与 `civitai.green` 均在约 8 秒连接超时；
   - 使用环境已有 HTTP 代理访问官方 `civitai.com` 成功；
   - 总真实 API 请求数未超过 probe 上限 5。
4. Validator：
   `..\project\.venv-dev\Scripts\python.exe -B scripts\validate-templates.py`

## Evidence

### P1 源码入口摘要

- `frontend/src/training/modules.ts` 注册 Anima、SD1.5、SDXL、Flux、Lumina、Krea 2 组合。
- `mikazuki/schema/` 包含 `sd3-lora.ts`、`anima-lora-fast.ts`、`anima-finetune.ts`、`lora-master.ts`、`dreambooth.ts`、`flux-lora.ts`、`lumina2-lora.ts`、`krea2-lora.ts` 等。
- `mikazuki/app/api.py` 有 `trainer_mapping` 与 Anima Fast/Musubi 特殊分支。
- 结论：支持面可以系统穷举，且 README 不是完整事实源。

### P2/P3 Civitai 字段摘要

- 官方文档确认 model version 响应含：ID、modelId、baseModel、baseModelType、trainedWords、trainingStatus、trainingDetails、files/hash、download URL 等；trainingDetails 可为 null。
- 实测版本 `882225`：HTTP 200，16,783 bytes；`trainingDetails=null`、`trainingStatus=null`；description 长度 692，并出现 rank、alpha、batch、steps、optimizer、LR、resolution 标记。
- 结论：API 可用于身份、base model、版本和可追溯性；训练参数需分为结构化字段与自由文本抽取，并记录抽取置信度。自由文本不得直接当高置信结构化事实。

### P4 Validator 摘要

```text
[ok] anima-lora-conservative.toml page=anima-lora normalized_keys=45
[ok] anima-lora-fast-conservative.toml page=anima-lora-fast normalized_keys=38
[ok] sd15-lora-conservative.toml page=sd-lora normalized_keys=10
VALIDATOR_EXIT=0
```

## Cleanup

- 未保存图片、模型权重、Cookie、token 或完整 API 响应。
- 未在 source project/agent-assets 生成缓存或候选文件。
- Probe 只将字段摘要写入本报告。

## Boundary

1. Stage 1 网络请求必须使用本机既有代理，并保持同样请求/时间/磁盘限额。
2. `trainingDetails` 为 null 是常见可预期状态；description 抽取必须保存原字段、解析规则、置信度和人工抽样审查。
3. 主项目在 probe 结束时出现与本任务无关的 plugin marketplace 工作树改动，已在 change record 记录；训练相关调查保持只读且须避开这些路径。

## Next Action

生成全程执行 goal，并对完整计划做开工前最终复盘。


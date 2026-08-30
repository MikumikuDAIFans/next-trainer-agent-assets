# Hugging Face 模型卡来源与用途核对

- Version: `2026-08-30`
- Scope: 将 Hugging Face 模型卡/API 作为模型来源与限制说明的观察证据，不把卡片字段当作 Next Trainer 模板默认值。
- Evidence status: L1 official documentation + L2 public metadata; `hf-api-flux-dev`、`hf-api-sdxl-base`、`hf-api-sd15` 于 2026-08-30 公开 API 返回 HTTP 200。
- Aliases / 检索关键词: 模型卡, Hugging Face, provenance, license, intended use, 来源核对

## 核对流程

记录模型仓库标识、观察时间、公开 revision 字段（若缺失则保持 unknown）、许可/用途/限制字段和是否为 base checkpoint。模型卡可帮助确认来源与适用范围，但不能证明某个训练器页面、网络算法或训练方向已被 Next Trainer 支持。

## 与 Next Trainer 的映射

将模型卡事实映射到 `base_model`、资产路径和数据/许可审查问题；具体字段仍以当前页面 schema、trainer mapping 和 validator 为准。API 搜索结果只用于发现候选，不提升为技术有效性证据。

## Sources

- Hugging Face Model Cards guide: https://huggingface.co/docs/hub/model-cards (L1 official)
- Public model API: https://huggingface.co/api/models/black-forest-labs/FLUX.1-dev (L2 metadata)
- Public model API: https://huggingface.co/api/models/stabilityai/stable-diffusion-xl-base-1.0 (L2 metadata)

## Boundaries

- 模型卡缺失字段不补默认值；下载量、点赞或标签不是训练效果证据。
- 不保存权重、图片或长篇许可文本；只保留 URL、时间、状态和短事实。

## Eval

- Question: “Hugging Face 模型卡能否直接决定 Next Trainer 的模板字段？”
- Expected answer: 不能；只能提供来源/用途观察，模板必须经过项目 schema 与 validator。


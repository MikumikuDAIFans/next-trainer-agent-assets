# External Channel Discovery (bounded public-source audit)

- Version: `2026-08-30`
- Scope: public channels considered for supplemental Next Trainer knowledge and template evidence; this document records discovery, not automatic adoption.
- Evidence status: L1 retrieval evidence for public repositories/docs; product compatibility remains L1 project validator evidence.
- Aliases / 检索关键词: 外部来源, source channel, sd-scripts, Musubi-Tuner, Diffusers, LyCORIS, AI-Toolkit, SimpleTuner, 模板来源

## Channels reviewed

| Channel | Public URL | Retrieval evidence | Intended use | Import status |
|---|---|---|---|---|
| kohya-ss sd-scripts | https://github.com/kohya-ss/sd-scripts | HTTP 200; observed head `37a1cbbc5725ed2a3575506e7bd2001c9908ac92` | SD/SDXL/Flux script contracts, config semantics | knowledge evidence; only project validator can admit templates |
| kohya-ss Musubi-Tuner | https://github.com/kohya-ss/musubi-tuner | HTTP 200; observed head `e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1` | Krea/DiT runtime and dataset/config conventions | knowledge evidence; product page remains authoritative |
| Hugging Face Diffusers LoRA | https://huggingface.co/docs/diffusers/en/training/lora | HTTP 200 | cross-tool LoRA concepts and reproducibility checklist | knowledge only; Diffusers configs are not Next Trainer TOML |
| Hugging Face Diffusers DreamBooth | https://huggingface.co/docs/diffusers/en/training/dreambooth | HTTP 200 | full-model fine-tune and prior-preservation concepts | knowledge only; page contract differs |
| KohakuBlueLeaf LyCORIS | https://github.com/KohakuBlueLeaf/LyCORIS | HTTP 200; observed head `b4d2f5e03c1d5f0c2337c0c98e407f9b61de4fff` | algorithm names, adapter-family boundaries | knowledge only unless page validator accepts |
| ostris AI-Toolkit | https://github.com/ostris/ai-toolkit | HTTP 200; observed head `be995185f598c83abb990a088e9f634c4d36eb46` | alternative workflow comparison and field vocabulary | knowledge only; no product support claim |
| bghira SimpleTuner | https://github.com/bghira/SimpleTuner | HTTP 200; observed head `b1463e977fde4b88c7c7f1c54bd591b67ec4dcba` | alternative dataset/eval practices | knowledge only; no product support claim |

## Retrieval policy

- Seven bounded HTTPS page requests and five bounded GitHub commit API requests were made through the existing local proxy `127.0.0.1:11809`.
- Only status, URL, observed commit ID, and short scope notes are retained; no page body cache, image, weight, credential, or long copyrighted text is stored.
- Upstream facts are version-sensitive. Each supplemental document must carry the observed date/commit and a boundary that product support is decided by the frozen support matrix and real validator.

## Round 1 execution

- The reusable harvester ran 20 public requests through `127.0.0.1:11809`: 17 HTTP 200, 3 failures.
- Request logs: `external-harvest/request-log-000-019.jsonl`; summary: `external-harvest/harvest-summary-000-019.json`.
- Failure report: `06_评测与校验/evidence/stage-5/external-harvest-round-1-failure-report.md`.

## Boundaries

- An external tool's YAML/JSON/TOML cannot be copied into a Next Trainer candidate template by analogy.
- Popularity, stars, downloads, or example frequency are discovery signals only, never correctness evidence.
- Broken or unpinned links are retained as source risks and cannot support precise claims.

## Stage 7 expansion (2026-08-30)

新增渠道族包括 Hugging Face 模型卡/API（FLUX、SDXL、SD1.5、Anima 搜索）、Diffusers 官方 examples、sd-scripts/Musubi 文档、BLIP/LAVIS caption、img2dataset/WebDataset 摄取、FiftyOne 视觉 QA、TorchMetrics/open_clip/clip-score 评测、PyTorch AMP/serialization/profiler 运行时，以及 BLIP/DataComp/CLIP/InstructPix2Pix/DreamBooth+LoRA 论文元数据。目录现为 58 个渠道、90 个可重放请求索引。

Stage 7 新增两段有界采集：`request-log-051-070.jsonl`（20/20 HTTP 200）与 `request-log-071-089.jsonl`（19/19 HTTP 200）。13 个响应达到 128 KiB 上限，保留 `size-limit` 状态，不从截断正文推断字段。

上述渠道只产生 10 篇知识候选和 1 份经 validator 证明的 SD DyLoRA 模板；其余外部配置保持比较证据，未自动进入模板库。

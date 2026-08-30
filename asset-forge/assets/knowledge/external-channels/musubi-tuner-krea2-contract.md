# Musubi-Tuner and Krea 2 evidence boundary

- Version: `2026-08-30`
- Scope: use the public Musubi-Tuner repository to understand Krea/DiT workflow vocabulary, runtime prerequisites, and evidence boundaries for the current Krea 2 page.
- Evidence status: L1 upstream repository observation (`e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1`) plus L1 Next Trainer Krea 2 schema/backend contract.
- Aliases / 检索关键词: Musubi-Tuner, Krea 2, DiT, Qwen3-VL, musubi, 运行时, Krea 配置

## Contract split

Musubi-Tuner explains the upstream engine and its model-family vocabulary. Next Trainer decides whether a field is exposed by `krea2-lora`, whether the runtime is enabled, and whether the import validator accepts the resulting config. Keep these layers separate:

| Layer | Evidence | Safe conclusion |
|---|---|---|
| Upstream engine | Musubi-Tuner repository and docs | what the engine calls a model, text encoder, VAE, or cache |
| Product page | `krea2-lora` schema and page route | which fields users can provide |
| Runtime gate | Musubi backend adapter and feature flag | whether the installed environment can execute |
| Import contract | real `validate_config_import` | whether a candidate template is admissible |

## Practical use

- Keep `qwen3-vl`, DiT, VAE, and cache prerequisites explicit when documenting Krea 2.
- Do not copy an upstream launcher command into a TOML template; Next Trainer deliberately omits machine paths and asks the user to fill them at import time.
- Treat engine version drift as a source risk. The observed revision is recorded for this audit and should be refreshed before migration approval.

## Sources

- kohya-ss/Musubi-Tuner, observed revision `e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1`: https://github.com/kohya-ss/musubi-tuner
- Current Krea 2 candidate: `../model-families/krea2-lora-musubi-guide.md`
- Krea 2 template evidence card: `../../05_模板库候选/krea2-lora-conservative.evidence.md`

## Boundaries

- The upstream repository does not upgrade Krea 2 from conditional to first-class support.
- No claim about training speed, VRAM, or output quality is made here.
- Model files, images, and private runtime caches were not downloaded.

## Eval

- Question: “Musubi-Tuner README 是否足以证明 Krea 2 模板可导入？”
- Expected answer: no; it is upstream context. Importability requires the current Krea 2 page validator and normalized diff.

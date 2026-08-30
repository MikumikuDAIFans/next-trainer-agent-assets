# 官方来源覆盖（Stage 1 Phase 1）

- Captured: `2026-08-30`
- Evidence level: L1 project contract + official repository/paper references
- Status: `pass-with-boundary`

## Coverage

| Support area | Project contract evidence | Official/source evidence | Status |
|---|---|---|---|
| Anima standard LoRA/LoKr/T-LoRA | `modules.ts`, Anima schema/adapter, `docs/anima-training.md` | kohya sd-scripts; LoRA/DyLoRA/OFT/LyCORIS references | covered; algorithm claims remain product-specific |
| Anima Fast LoRA | Fast schema, backend config and preflight | `sorryhyun/anima_lora` | covered; fixed runtime commit still pending |
| Anima full finetune | finetune schema and API route | kohya sd-scripts | covered |
| SD 1.x/2.x LoRA and DreamBooth | lora-master/dreambooth schema and route mapping | kohya sd-scripts; LoRA paper | covered; SD2 requires conditional flags |
| SDXL LoRA and finetune | SDXL schema, route, validator evidence | kohya sd-scripts; LoRA/LyCORIS/OFT references | covered |
| Flux/Chroma LoRA | flux schema, Chroma preset, route mapping | kohya sd-scripts; FLUX official repository | covered; Chroma is Flux-page variant |
| Krea 2 LoRA | Musubi schema/backend/preflight | kohya-ss/musubi-tuner | covered; optional runtime and commit pending |
| Lumina 2 | schema/route conflict evidence | official source not yet sufficient for product support | boundary: unsupported end-to-end |
| Slider/concept erasure | unsupported specialized objectives in support matrix | research lead only; exact paper URL requires verification | not product support |

## Source Handling Decisions

The registry separates project-contract evidence from upstream/official references. A source marked `needs-verification` is not used to support a precise claim. Civitai remains L2 observation evidence and cannot override route/schema/trainer/validator conclusions. Exact upstream commits and any unresolved paper identifier must be completed before Stage 1 completion gate; this Phase 1 artifact makes those gaps explicit rather than inventing versions.

# OFT guide (Orthogonal Finetuning adapters — availability by page)

- Version: `2026-08-30`
- Scope: where native OFT modules are actually accepted in this product, the frontend diagnostic that gates them, and the LyCORIS OFT variants (Diag-OFT/BOFT) that are separate things.
- Evidence status: L1 project contract (module unions + `params.ts` diagnostics + support matrix).
- Aliases / 检索关键词: oft, orthogonal finetuning, networks.oft, networks.oft_flux, diag-oft, boft, oft sdxl only

## Availability map (L1)

| Page | Native OFT module | Gate |
|---|---|---|
| SDXL (`sdxl-lora`) | `networks.oft` accepted (`lora-master.ts` module union) | frontend diagnostic allows OFT **only** when `model_train_type = sdxl-lora`: selecting `networks.oft` on `sd-lora` pushes a hard error (`params.ts` oftSdxl rule) |
| SD 1.x/2.x (`sd-lora`) | rejected by frontend diagnostic (and matrix records native OFT as unsupported objective) | same rule |
| Flux (`flux-lora`) | dedicated `networks.oft_flux` module in the Flux page union | Flux-path OFT is a different module from `networks.oft` |
| Anima / Fast / Krea / Lumina | none | adapter unions reject it |

Separately, **LyCORIS Diag-OFT and BOFT** are algorithm choices inside `lycoris.kohya` (`shared.ts` algo union includes `diag-oft`, `boft`) — orthogonal-variant families from LyCORIS, not the native OFT module. Never report "OFT" without saying which of the three: native SDXL OFT, Flux-native OFT, or LyCORIS OFT-variants.

## Method context (official paper — L1 public)

OFT rotates (orthogonal transform) feature spaces instead of low-rank updates, theoretically preserving relative distances in representation space; BOFT composes butterfly OFT blocks for sparse updates. Paper: arXiv:2306.07280 (registered source `oft-paper`). Paper claims about parameter efficiency are method-level, not per-page product measurements.

## Practical reading (contract-derived)

- The SD1.x hard rejection is a validation-level fact: do not suggest "try OFT on SD 1.5 anyway" — the product blocks it, and forcing TOML around a frontend gate is not supported usage.
- No shipped OFT preset and no measured OFT run exists in this staging evidence: capacity/quality comparisons vs LoRA remain L3 experiment territory.
- Availability carries the page's support level: SDXL first-class; Flux first-class. Support is per page + module pair.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/lora-master.ts`, `mikazuki/schema/flux-lora.ts:52`, `mikazuki/schema/shared.ts`, `frontend/src/training/params.ts` (oftSdxl diagnostic).
- OFT paper: https://arxiv.org/abs/2306.07280.
- Frozen support matrix entries `sdxl-lora`, `flux-lora`, `sd15-lora` (staging artifact).

## Boundaries

- Lumina 2's schema declares OFT forms but the whole page is end-to-end broken — never count it (`../model-families/lumina2-known-breakage.md`).
- Diag-OFT/BOFT availability comes through LyCORIS and inherits LyCORIS field semantics (`lycoris-family-guide.md`), not the native OFT knobs.
- No OFT numbers may be presented as validated; none are measured here.

# LyCORIS family guide (LoCon / LoHa / LoKr / IA3 / GLoRA / Diag-OFT / BOFT)

- Version: `2026-08-30`
- Scope: the shared LyCORIS contract surface in this product — module selection, algo union, shared fields and their pinned exceptions, per-page availability, and known field-level quirks recorded in the schema.
- Evidence status: L1 project contract (`shared.ts` LYCORIS_MAIN/LOKR blocks, `params.ts` serialization, module unions, support-matrix adapter lists).
- Aliases / 检索关键词: lycoris, locon, loha, lokr, ia3, glora, diag-oft, boft, conv_dim, conv_alpha, train_norm, network_args

## Selection contract (L1)

- Entry: `network_module = lycoris.kohya` → `lycoris_algo` union: **`locon` (default), `loha`, `lokr`, `ia3`, `dylora`, `glora`, `diag-oft`, `boft`**.
- Shared fields (serialized into `network_args` as `conv_dim=,conv_alpha=,dropout=,algo=`):
  - `conv_dim` default 4 / `conv_alpha` default 1 — conv-layer capacity pair (linear-side capacity uses the page's `network_dim/network_alpha`).
  - `dropout` default 0, schema note recommends 0–0.5 but marks **LoHa/LoKr/(IA)³ as not supporting this dropout field**.
  - `train_norm` default false; schema pins IA3 unsupported for it, and Anima LoKr auto-disables it (NormModule sampling crash avoidance).
- LoKr adds `lokr_factor` (default -1 = infinite; commonly ≥4) — full detail in `lokr-guide.md`.
- Custom escape hatch: `network_args_custom` (one per line; overrides duplicated keys — the params UI warns the preview may show duplicates while custom wins).

## Per-page availability (L1; matrix adapter lists)

| Page | LyCORIS present |
|---|---|
| SD 1.x (`sd-lora`) | yes (LoCon/LoHa/LoKr/IA3/DyLoRA/GLoRA/Diag-OFT/BOFT) |
| SD 2.x (`sd-lora` + v2 flags) | yes (via general LyCORIS availability on the page) |
| SDXL (`sdxl-lora`) | yes |
| Flux (`flux-lora`) | yes (module in Flux union) |
| Anima (standard) | LoKr only as verified adapter; other LyCORIS algos not verified (C-005/C-006 discipline) |
| Anima Fast / Krea 2 / Lumina 2 | none |

## Naming traps (L1)

1. "LoCon" vs old "LoHa-style conv pairs": in this union `locon` is the default algo — switching pages doesn't change that default silently; always record `lycoris_algo` in run logs.
2. `network_dim/network_alpha` (linear layers) and `conv_dim/conv_alpha` (conv layers) are **two independent capacity pairs**; reporting only one for a LyCORIS run under-documents it.
3. LyCORIS-native dropout replaces the generic `network.dropout` field where the schema says the generic field is unsupported; don't expect `network_dropout` to do anything for LoHa/LoKr/IA3.
4. Diag-OFT/BOFT here are LyCORIS algorithms, distinct from native `networks.oft`/`networks.oft_flux` (`oft-guide.md`).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (LYCORIS_MAIN / LYCORIS_LOKR blocks), `mikazuki/schema/lora-master.ts`, `mikazuki/schema/flux-lora.ts:52`, `frontend/src/training/params.ts` (UI_PARAMS + network_args serialization).
- LyCORIS upstream: https://github.com/KohakuBlueLeaf/LyCORIS (algorithm implementations; the pinned project-side version is a recorded P2 follow-up in the source registry).
- Frozen support matrix (staging artifact).

## Boundaries

- Page-level availability is validator/contract-level proof, not a measured product run: per-algo quality/VRAM claims are outside this KB (no measured LyCORIS run in staging evidence).
- On standard Anima only LoKr has product proof; do not extend LyCORIS-family behavior claims to Anima beyond that.
- `train_norm` exceptions are pinned behavior; treat them as contract, not preference.

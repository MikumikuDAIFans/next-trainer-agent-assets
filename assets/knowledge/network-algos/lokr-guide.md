# LoKr guide (Kronecker-product adapter)

- Version: `2026-08-30`
- Scope: where LoKr is actually supported in this product (verified Anima path + LyCORIS path on SD/SDXL/Flux), the UI fields it serializes to, project-documented starting behavior, and known runtime quirks pinned in the schema.
- Evidence status: L1 project contract (Anima adapter tests, LyCORIS shared schema block, docs). Effect guidance from `docs/anima-training.md` is project-documented experience, not causal.
- Aliases / 检索关键词: lokr, cyclical lokr, kronecker, factor, conv_dim, conv_alpha, train_norm, 高秩

## Where LoKr exists (L1)

| Path | Pages | Evidence |
|---|---|---|
| Verified Anima adapter | `anima-lora` (standard) — LoKr listed among verified algorithms (adapter tests + preset injection) | support-matrix `anima-standard-lora.adapterAlgorithms`; `mikazuki/anima_backend/adapter.py` |
| LyCORIS path | SD 1.x/2.x, SDXL, Flux pages via `network_module = lycoris.kohya`, `lycoris_algo = lokr` | `mikazuki/schema/shared.ts` LYCORIS_MAIN block |
| Not available | Anima Fast, Krea 2, Lumina 2 | respective support-matrix entries reject non-LoRA adapters |

## Field contract (L1 — shared schema block)

- `lycoris_algo` union: `locon` (default), `loha`, `lokr`, `ia3`, `dylora`, `glora`, `diag-oft`, `boft`.
- `conv_dim` default 4, `conv_alpha` default 1 (conv-side capacity), serialized into `network_args` together with `dropout` and `algo`.
- `lokr_factor` default `-1` (documented as "infinite"; commonly ≥4). Smaller factor ⇒ more parameters/capacity (approaching full-rank), per schema description and project docs.
- `dropout` note pinned in schema: LoHa/LoKr/(IA)³ do not support the generic dropout field — use algorithm-native options if needed.
- `train_norm` default false; schema pins that **Anima LoKr automatically disables `train_norm`** to avoid a LyCORIS NormModule sampling crash — do not treat unexpected train_norm-off behavior as a bug.

## Project-documented starting behavior (docs/anima-training.md, LoKr section — observation-level)

- Start `factor` relatively large (e.g. 16); lower gradually when underfitting, lowering LR together with factor.
- `full_matrix` mode uses the full Kronecker product instead of low-rank approximation (no very large dim needed).
- LoKr is documented as tolerating somewhat higher LR than plain LoRA; Anima's dense-attention architecture motivates high-rank adapters.
- LoKr and LoRA are framed as complementary; mixing/对比 is explicitly suggested by the doc.
None of the above is a guarantee; each is documented project experience to verify on your own dataset.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts`, `mikazuki/anima_backend/adapter.py`, `frontend/src/training/params.ts`, `docs/anima-training.md`.
- LyCORIS upstream: https://github.com/KohakuBlueLeaf/LyCORIS (method/implementation reference; exact version in project environment is a recorded P2 follow-up).
- Frozen support matrix (staging artifact); conflict register C-005/C-006 for what is NOT verified on Anima.

## Boundaries

- Only LoKr on standard Anima carries first-class product proof (tests + presets). On SD/SDXL/Flux it is LyCORIS-module availability — page-level validator proof, not a tested product path; say so when recommending.
- Never mix this with the schema-only adapters (VeRA/LoRA-FA/LoHa-on-Anima/PiSSA) — see `anima-schema-only-adapters.md`.
- No measured LoKr-vs-LoRA comparison exists in this staging evidence set; "LoKr is better for X" is an L3 experiment suggestion at most.

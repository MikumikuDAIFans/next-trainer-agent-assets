# T-LoRA guide (timestep-dependent rank, Anima only)

- Version: `2026-08-30`
- Scope: T-LoRA in this product — availability limited to the standard Anima LoRA page; the dynamic-rank contract fields, documented defaults, expected behavior differences from plain LoRA, and inference compatibility.
- Evidence status: L1 project contract (support matrix lists T-LoRA among verified Anima algorithms; `docs/anima-training.md` T-LoRA tutorial section is the product's own documented guidance). Numeric guidance there is documented default/observation, not causal.
- Aliases / 检索关键词: t-lora, tlora, 动态rank, timestep, min_rank, rank_schedule, orthogonal_init, anima

## Availability (L1)

- Standard `anima-lora` page: T-LoRA is one of the three verified adapter algorithms (with LoRA and LoKr). Evidence: support-matrix `anima-standard-lora.adapterAlgorithms`; selecting it switches to the dedicated network module with tuned defaults (`docs/anima-training.md`).
- Rejected elsewhere: Anima Fast (LoRA-only), Krea 2 (LoRA-only), SD/SDXL/Flux LyCORIS union does not include T-LoRA (`shared.ts` algo list). There is no product-wide T-LoRA.

## Contract fields and documented defaults (L1 docs table)

| Field | Doc default | Documented meaning |
|---|---|---|
| `network_dim` | 32 | dynamic rank compresses effective capacity ⇒ typically needs higher dim than plain LoRA |
| `network_alpha` | 32 | recommend equal to dim to avoid implicit LR scaling |
| `tlora_min_rank` | 4 | rank floor near t≈0; smaller saves parameters, lowers capacity |
| `tlora_rank_schedule` | linear | `linear` vs `cosine` (smoother) |
| `tlora_orthogonal_init` | on | orthogonal init for stability; keep on per docs |
| `unet_lr` | — | effective gradients smaller under dynamic rank ⇒ docs suggest possibly raising vs plain LoRA |

Documented behavior expectations (project docs, observation-level):

- Slower convergence than plain LoRA with visibly little preview change early — docs explicitly normalize this expectation and list levers (dim↑, min_rank↑, LR↑ modestly, more epochs).
- Overfitting pressure lower at low-noise steps (the design rationale).
- Small datasets / fine-control scenarios are the documented fit; LoKr addresses a different axis (high-rank capacity) — the docs compare them as complements, not winners.
- Output checkpoints load as ordinary LoRA at inference (full static rank; no timestep-dynamic adjustment at runtime) — documented compatibility note.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `docs/anima-training.md` (T-LoRA tutorial section), `mikazuki/schema/sd3-lora.ts`, `mikazuki/anima_backend/adapter.py`.
- Frozen support matrix entry `anima-standard-lora` (staging artifact).

## Boundaries

- Anima-only: any "T-LoRA for SDXL/Flux" request is unsupported product-wise; the underlying paper's generality is not a product capability.
- The doc defaults above are shipped/documentation values; measured T-LoRA runs exist nowhere in this staging evidence — effects remain observations.
- Do not confuse with DyLoRA (different mechanism: trained-dim-slice extraction) — see `dylora-guide.md`.

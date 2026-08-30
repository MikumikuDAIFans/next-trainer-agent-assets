# Anima schema-only adapters — UI traps (LoRA-FA / VeRA / LoHa / PiSSA)

- Version: `2026-08-30`
- Scope: the four adapter choices exposed by the standard Anima LoRA UI that currently have **no backend differentiation proof** — what actually happens when you select them, why they are excluded from supported algorithms, and how to answer users who picked one.
- Evidence status: L1 project contract (schema mapping, pinned adapter tests, backend adapter code, fixed upstream search). This is a boundary/trap doc, not a usage guide.
- Aliases / 检索关键词: lora-fa, vera, pissa, loha anima, schema-only, 假选项, UI陷阱, networks.lora_anima, discarded

## What the contract shows (L1, Stage 0 probes; conflict register C-005/C-006)

| UI choice | What the adapter layer emits | Verdict |
|---|---|---|
| LoRA-FA | `{"network_module": "networks.lora_anima"}` — identical to plain LoRA, type discarded | not verifiable as a distinct adapter |
| VeRA | `{"network_module": "networks.lora_anima"}` — identical to plain LoRA | same; and the fixed upstream has no VeRA implementation hit |
| LoHa | `{"network_module": "networks.loha"}` — module does switch, but no Anima-specific test/regression exists | unverified on Anima (upstream LyCORIS LoHa ≠ proven Anima path) |
| LoRA + PiSSA init | `{"network_module": "networks.lora_anima", "pissa_init": true, "pissa_method": "rsvd"}` — flags emitted, but **no implementation hit in the pinned `vendor/sd-scripts`** | unknown-effect flags; may be silently ignored |

Pinned evidence: `sd3-lora.ts` maps LoRA-FA/VeRA to `networks.lora_anima`; `adapter.test.ts:184-197` pins that mapping; `anima_backend/adapter.py:392-400` treats `lora_type` as UI-only and discards it.

## Consequences (frozen decisions)

1. Supported Anima adapter set remains **LoRA / LoKr / T-LoRA** only. The matrix records the other four under `schemaDeclaredUnverifiedAlgorithms`.
2. A user selecting LoRA-FA/VeRA on Anima is silently training a **plain Anima LoRA** — the produced file's behavior matches the plain LoRA contract, so their results are "wrong algorithm", not "corrupted file". Correct advice: re-run with the intended supported adapter (e.g. LoKr for high-rank goals), or wait for backend proof.
3. PiSSA flags must not be described as an available initialization method; no implementation exists in the pinned upstream. Even after implementation, PiSSA is an initialization technique — never a training direction.
4. No candidate templates may target any of these four choices (Stage 3 hard rule, same rule as support-conflicts registry header "conflicted pages get no templates").

## How to phrase user-facing answers

- "The option exists in the UI but the backend currently cannot prove a different adapter was trained" — accurate, non-accusatory.
- Never fill the gap with upstream general LoRA-FA/VeRA lore ("FA freezes A matrix..." etc.) as if it were this product's behavior; the observable product behavior here is plain-LoRA substitution.
- If the user's actual goal is capability-based (memory, high rank, initialization), route to the supported equivalent: LoKr (capacity), T-LoRA (overfit control), small dim + grad checkpointing (memory).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/sd3-lora.ts:110-125`, `mikazuki/tests` adapter tests `adapter.test.ts:184-197`, `mikazuki/anima_backend/adapter.py:392-400`.
- Stage 0 probe results and conflict register: `01_训练器能力盘点/support-matrix-validation.md`, `support-conflicts.md` C-005/C-006 (staging artifacts).

## Boundaries

- This document's claims are pinned to the audited commits; a product fix could flip any row — re-validate before reusing wording after upgrades.
- Do not infer "hidden VeRA/LoRA-FA might secretly work": absence of differentiation in emitted config is exactly the failure.
- LoHa status is "module-switches-but-unverified-on-Anima", weaker than "not even different" (LoRA-FA/VeRA) and stronger than "no implementation" (PiSSA); keep those three tiers distinct.

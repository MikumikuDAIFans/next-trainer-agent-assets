# Multi-concept / combination training (generic objective, no composability guarantee)

- Version: `2026-08-30`
- Scope: training several concepts (characters, styles, objects) in one dataset/run vs keeping separate LoRAs; token-collision rules, sample balance, and the honest limits of "combined" LoRAs.
- Evidence status: L1 project contract (taxonomy row "generic multi-concept objective"; caption/keep-tokens fields on LoRA pages); balance/leakage practice is domain observation; no GPU-measured claims.
- Aliases / 检索关键词: 多概念, 组合, multi-concept, combination, token collision, 概念泄漏, 一个LoRA多个角色

## Support framing (L1)

- Taxonomy: 多概念组合 can be trained in one dataset, but "automatic composability" is explicitly not a product guarantee; determinants are token 冲突、样本平衡、概念泄漏 (`training-direction-taxonomy.md`).
- No multi-concept mode exists: it is ordinary LoRA training with disciplined captioning, so the page contract (caption fields, keep_tokens, dropout) is the entire mechanism.

## Two strategies (both ordinary LoRA — the difference is data)

| Strategy | When | Failure profile |
|---|---|---|
| One run, several triggers | concepts share rendering context; cheap deployment | weaker per-concept identity when sets are small; leakage between concepts |
| Separate LoRAs, combined at inference | strong individual identities | combination behavior is inference-time; not trained — see `character-identity.md` combination honesty; base/other-LoRA interference possible |

## Token-collision rules (observation-level, caption-field-grounded)

1. One reserved trigger per concept; never share a trigger token across concepts.
2. Shared descriptive captions ("1girl, dress") describe the *common* space; concept differences live in the trigger + unique caption tokens — ambiguous captions blur concepts.
3. Sample balance: near-equal effective exposure per concept (images×repeats); a 3× larger concept dominates by default. (Repeat/exposure knobs per page contract.)
4. `keep_tokens` (per caption block) protects leading trigger tokens from shuffle — that is the mechanical reason triggers stabilize; it is not identity magic.

## Evaluation protocol

- Per-concept fidelity vs the single-concept baseline (same prompts); combination prompts (A + B attributes) to measure leakage explicitly; neutral prompts for cross-talk.
- If concepts degrade vs solo baselines, treat as data-balance/coverage issue first; capacity claims need your own sweep evidence.

## Sources

- Staging artifacts: `training-direction-taxonomy.md` (multi-concept row), caption/keep-tokens field surface per `mikazuki/schema/shared.ts` (https://github.com/wochenlong/lora-scripts-next).

## Boundaries

- Do not promise N-concept LoRA == N solo LoRAs; report measured fidelity.
- Cross-family combination claims (Anima LoRA + SDXL LoRA) don't apply: adapters bind to their base family's contract (`../model-families/sdxl-derived-cohorts.md` mismatch discipline).
- No numeric recipe: staging evidence has no measured multi-concept exposure tables.

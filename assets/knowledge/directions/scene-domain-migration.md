# Scene / environment / domain-migration direction

- Version: `2026-08-30`
- Scope: environments, scenes and wider domain shifts as data objectives; the LoRA-vs-full-finetune decision boundary, scale/forgetting risks, and cohort/base-bias caveats.
- Evidence status: L1 project contract (taxonomy row "standard objective / full-model option"; full-finetune first-class list is fixed); scale/forgetting guidance is domain observation; no GPU-measured claims.
- Aliases / 检索关键词: 场景, 环境, 领域迁移, scene, environment, background, domain, 风格领域

## Support framing (L1)

- Taxonomy: 环境/场景/领域迁移 = standard dataset objective (LoRA pages) **or** supported full finetune where first-class: Anima full DiT, SD 1.x/2.x DreamBooth, SDXL full finetune (`training-direction-taxonomy.md`; page guides carry the contract details). Flux finetune stays UI-hidden; Krea/Lumina have no finetune page.
- No dedicated scene page exists — choice is granularity + data design.

## Granularity decision (contract-shaped)

| Goal | Surface | Why |
|---|---|---|
| Add a recurring environment/style domain to an otherwise intact model | LoRA on the matching base page | adapter stays swappable, cheap iteration |
| Wide distribution change the base genuinely lacks | full finetune where first-class | more capacity, but risk profile: 数据、显存、回滚和灾难性遗忘 significantly higher (taxonomy wording; page guides repeat it) |

Domain breadth vs LoRA capacity is a known tension: a broad-domain LoRA saturates fast; taxonomy's determinants are 数据规模、范围宽度、灾难性遗忘 — keep claims to what the base already approaches.

## Data design (observation-level)

- Environment diversity: same "domain" across weather/time/framing; otherwise weather or framing becomes the domain.
- Caption split: scene tokens (keep steerable) vs subject tokens (caption out, or your scene LoRA learns one protagonist).
- For backgrounds used behind characters: combine expectations follow `multi-concept-training.md` — no automatic composability guarantee.

## Evaluation protocol

- Fixed prompts across {domain prompt, neutral prompt, unrelated-subject prompt}; watch base-capability drift (forgetting proxy) especially on full finetune runs; compare against the untouched base, per `../model-families/sdxl-full-finetune-guide.md` / `anima-full-finetune-guide.md` discipline.

## Sources

- Staging artifacts: `training-direction-taxonomy.md` (scene row + full-finetune scope note), support-matrix granularity fields.
- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: LoRA/finetune page contracts per cited page guides.

## Boundaries

- Do not sell LoRA domain LoRAs as capability injection beyond base-model reach; no measurement here supports "learn any domain".
- Full finetune forgetting has no numeric guardrail in this evidence set — treat as risk to monitor, not a bounded quantity.
- Real locations/brands raise the usual rights questions; dataset sourcing remains user-side.

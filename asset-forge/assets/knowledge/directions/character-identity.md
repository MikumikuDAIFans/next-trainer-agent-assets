# Character / identity direction (data objective, all LoRA pages)

- Version: `2026-08-30`
- Scope: character & identity LoRA as a **data/supervision objective** (orthogonal to model family and adapter algorithm): dataset coverage discipline, trigger/caption conventions, identity-vs-clothing/pose disentangling, evaluation protocol, and which product surfaces explicitly name character support.
- Evidence status: L1 project contract for availability/preset wording; coverage/evaluation guidance is domain practice marked as observation-level; no GPU-measured effect claims.
- Aliases / 检索关键词: 角色, 身份, character, identity, oc, 触发词, trigger, 单角色, 一致性

## Support framing (L1)

- Character training is a standard dataset objective on **every end-to-end LoRA page** (Anima std/Fast, SD1.x/2.x, SDXL incl. cohorts, Flux/Chroma, Krea 2) — no special mode is needed or exists.
- Explicit product touchpoints: Anima ships a character preset whose description covers "single character, outfits, props" (`config/presets/anima-lora-character-automagic.toml`); the DreamBooth page records "subject/identity personalization" as its named direction (`support-matrix sd15-dreambooth`).
- Frozen taxonomy class: `standard dataset objective`; the taxonomy's determinants of success are data-side: identity consistency, trigger words, caption de-leakage, pose/clothing coverage (`01_训练器能力盘点/training-direction-taxonomy.md`).

## What "character LoRA" actually learns (observation-level discipline)

A character set usually entangles identity + default outfit + default pose + background + rendering style. The model learns the whole bundle. Decisions that must be made consciously at dataset time:

1. **Trigger token**: reserve one rare token sequence as the identity handle; keep it out of generic captions (caption strategy: `../datasets/caption-tag-trigger-strategy.md`, batch 3). The formal Civitai-reading doc records the same rule when reusing external trigger conventions: take them verbatim, caption consistently (`workflows/civitai-model-to-lora.md`).
2. **What to caption vs bake in**: caption things you want controllable later (outfit, pose, expression, background) and leave the identity itself to the trigger — every uncaptioned varying factor becomes part of "the character".
3. **Coverage matrix**: vary pose angle, framing (face-close / half / full body), lighting, expression, outfit; identity claims only generalize over what varied.
4. **Clothing/identity separation** questions route to `clothing-accessory.md`; expression/feature separation to `pose-expression-features.md`.

## Evaluation protocol (project-consistent, non-causal)

- Fixed prompt set + fixed seed previews across checkpoints (pages expose preview switches; Anima preview contract documented at 1024/CFG4.5/40/seed42 in `docs/anima-training.md`).
- Identity checks: unseen pose prompt, unseen outfit prompt (should bend), background-swap prompt (should persist).
- Failure reads: only-training-view identity (fails unseen angles) = coverage problem, not dim problem; style bleed = base-model/caption leakage, cf. `../model-families/sdxl-derived-cohorts.md` mismatch family.

## Parameter claims — deliberate silence

Concrete dim/LR/step values for character work exist only as (a) shipped preset values (recorded in each page guide) and (b) project real-run baselines (`model-families/anima-lora-parameter-baseline.md`, `anima-character-case-v1.md` — explicitly marked as local observations, sister cases, not causal conclusions). Cite them with their evidence tag; never restate as guarantees. Civitai Stage 1 observation found **zero structured training parameters** across sampled versions, so community popularity numbers are not parameter evidence (`03_Civitai样本/reports/missingness-and-bias-report.json`, staging artifact).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `config/presets/anima-lora-character-automagic.toml`, `docs/anima-training.md`.
- Staging artifacts: support-matrix entries (`specializedDirections`), `training-direction-taxonomy.md`, Stage 1 missingness report.
- Formal knowledge: `model-families/anima-character-case-v1.md` (real run, sanitized), `workflows/civitai-model-to-lora.md`.

## Boundaries

- Do not promise identity transfer across base-model families or cohorts; retrain per base.
- Do not scale LoRA weight strength as "identity amount" claims — strength knobs are inference-side.
- Likeness/copyright/consent constraints for real persons are user responsibilities; the KB never sources datasets.

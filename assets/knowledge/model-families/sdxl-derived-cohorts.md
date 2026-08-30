# SDXL-derived cohorts — Pony, Illustrious, NoobXL and friends

- Version: `2026-08-30`
- Scope: how SDXL-family derivative checkpoints are treated by the product (cohort routing, not separate trainers), the base-mismatch failure family, and how Civitai cohort observations should be read.
- Evidence status: L1 project contract (support matrix `sdxl-lora` baseModelVariants; `config_import.py` SDXL path rules) + one formal heuristic doc for reading Civitai pages; cohort behavior itself is observation-level.
- Aliases / 检索关键词: pony, illustrious, noobxl, 派生, 兼容, base mismatch, 底模不匹配, sdxl family

## What the contract says (L1)

- Pony, Illustrious, NoobXL and compatible derivatives are recognized as **SDXL-compatible models on the SDXL page/validator**, not as separate trainers or pages. The template contract for all of them remains the `sdxl-lora` validator. Evidence: support-matrix `sdxl-lora` (`baseModelVariants`), `mikazuki/utils/config_import.py` SDXL path rules matching `noobxl|pony|illustrious`.
- Consequences:
  1. There is no per-cohort preset, per-cohort template, or per-cohort validation rule inside the product today.
  2. Any "Pony-specific trainer" claim would be false; anything a cohort needs beyond the SDXL page is either a field value (prediction type, LR) or out of product scope.

## The base-mismatch failure family (formal heuristic + contract)

The formal doc `workflows/civitai-model-to-lora.md` records the reading rule: a LoRA trained for Pony does not transfer cleanly to stock SDXL even though both are "SDXL family"; base model is the hard-stop field when reusing external LoRA/recipes. The concrete failure modes:

- Copying stock-SDXL parameter advice onto a Pony-style derivative (or reverse) and blaming the adapter when identity does not converge — prediction-type mismatch is the usual root; take the value from the checkpoint's own published spec.
- Mixing trigger/caption conventions across cohorts, diluting identity signal.
- Cross-loading LoRA files between cohorts during inference and reading the artifact as "the LoRA is broken".

## How to handle cohort questions

1. Route to the SDXL page workflow: `sdxl-lora-workflow-guide.md`.
2. State cohort explicitly in the plan metadata (name + source URL) but keep parameter claims at the SDXL starting-box level unless a measured run for that cohort exists — none does in the audited evidence.
3. For Civitai evidence: Stage 1 sampling kept cohorts separate at query level; per-stage rules apply — same-model versions are not independent samples, popularity is not technical evidence, `trainingDetails` was null across the sample. Cohort observations (what authors tend to publish) are fine as L2 context; cohort parameters are not L1 facts.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/utils/config_import.py` (SDXL_PATH_RULES), `mikazuki/schema/lora-master.ts`.
- Formal knowledge baseline: `workflows/civitai-model-to-lora.md` (heuristic reading order).
- Frozen support matrix entry `sdxl-lora` (staging artifact); Stage 1 observation policy: `03_Civitai样本/reports/missingness-and-bias-report.json` (staging artifact).

## Boundaries

- Do not create per-cohort product templates in Stage 3: the validator surface is `sdxl-lora`; per-cohort TOMLs would fabricate a product distinction that does not exist.
- Do not assert per-cohort prediction types from memory; the knowledge base intentionally hardcodes none.
- Cohort popularity on Civitai (downloads/faves) is discovery-only and must never appear as a parameter justification.

# Regularization images (DreamBooth prior-loss scope; not a general technique here)

- Version: `2026-08-30`
- Scope: what `reg_data_dir`/`prior_loss_weight` are, which training flow actually gives them meaning (DreamBooth prior loss), the honest status of these fields on LoRA pages, and dataset-side cautions.
- Evidence status: L1 project contract (shared DATASET_SETTINGS fields; DreamBooth schema context; product default "off"). LoRA-page effectiveness is explicitly **not established** in project evidence.
- Aliases / 检索关键词: 正则化, regularization, reg_data_dir, prior_loss_weight, prior loss, 类图, class images, 防遗忘图

## Contract (L1)

- Shared dataset block exposes `reg_data_dir` (schema description: "regularization dataset path. Default empty, regularization images not used") and `prior_loss_weight` (default 1.0).
- The mechanism these fields name — prior-loss preservation against a class prior — belongs to the DreamBooth/model-finetune flow (`train_db.py`, train type `sd-dreambooth`; see `../model-families/sd-dreambooth-finetune-guide.md` where reg pairing with instance images is part of the page contract).
- **Scope caution:** because the fields sit in a shared block, they surface on LoRA pages too, but neither product docs, presets, nor any staging verification establish regularization-image behavior for LoRA network training. KB rule: treat LoRA+reg as **unproven-in-project**; use the DreamBooth flow when preservation against a class prior is the goal.

## How DreamBooth uses them (page-contract level)

- Instance images (`train_data_dir` subdirs) teach the subject under the trigger token; regularization images (same class, not the subject) anchor the class prior so the trigger doesn't swallow the whole class; `prior_loss_weight` scales that anchor term.
- Off by default in this product — consistent with common practice that prior preservation costs time and only pays off for anthropomorphic/high-prior-conflict subjects (mark: practice observation, not measured here).

## Dataset-side cautions (practice + rights)

1. Class-matched content: regularization images should depict the *class* ("a tok_abc dog"), matching captions per the caption pipeline; unrelated pretty pictures anchor the wrong prior.
2. Quantity/time cost roughly mirrors instance set size — plan training wall-clock accordingly (no product number exists; keep L3).
3. Third-party class images carry license/personality rights issues (real people/artist works); the KB gives no sourcing channels — user responsibility.

## Decision table

| Goal | Mechanism |
|---|---|
| Subject learns without class-drift, SD 1.x/2.x DreamBooth | reg_data_dir on/off per above, prior_loss_weight default 1.0 |
| LoRA runs (any page) | don't claim reg-image benefits; control via caption distribution + checkpoints instead |
| Forgetting mitigation on SDXL full finetune | no reg pipeline contract there either — evaluate vs untouched base (see that page guide) |

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (DATASET_SETTINGS), `mikazuki/schema/dreambooth.ts`.
- Staging artifacts: page guides `sd-dreambooth-finetune-guide.md` (this staging set).

## Boundaries

- Never describe reg images as an anti-forgetting feature of LoRA pages — the audited contract doesn't support it.
- No measured instance:reg ratio guidance exists in this KB; ratios quoted in community posts stay community claims.
- SDXL DreamBooth-era prior preservation specifics beyond the fields above: unknown-here.

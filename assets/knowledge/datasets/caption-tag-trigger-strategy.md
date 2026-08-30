# Caption / tag / trigger strategy (field-grounded decisions)

- Version: `2026-08-30`
- Scope: how the caption schema fields actually constrain tag strategy — shuffle/keep-tokens mechanics, dropout knobs, weighted-caption caution, token-length ceiling — and how to design trigger tokens that survive shuffling; the WD14 tagging pipeline stays in the formal doc.
- Evidence status: L1 project contract (`shared.ts` CAPTION_SETTINGS, params.ts serialization); trigger conventions are domain practice marked as such.
- Aliases / 检索关键词: caption, tag, 触发词, trigger, keep_tokens, shuffle_caption, dropout, 权重语法, wd14

## Field mechanics (L1)

| Field | Default | Real behavior |
|---|---|---|
| `caption_extension` | `.txt` | pairing gate (`datasets/preparation-checklist.md`) |
| `shuffle_caption` | false | shuffles comma tags each step — order-robustness at the cost of position priors |
| `keep_tokens` | 0 | first N tokens exempt from shuffle (**the** trigger-protection knob when shuffle is on) |
| `keep_tokens_separator` | unset | custom separator counted for keep-tokens |
| `max_token_length` | 255 | caption token ceiling (75-blocks semantics upstream) |
| `weighted_captions` | off | per-tag weight syntax `(word:1.2)`; schema note: **not recommended together with shuffle_caption** |
| `caption_dropout_rate` | unset | probability a whole image trains caption-less (unconditional mix) |
| `caption_dropout_every_n_epochs` | unset | epoch-quantized full-caption dropout |
| `caption_tag_dropout_rate` | unset | per-tag dropout probability |

## Strategy decisions the fields force (L1-shaped, practice-tagged)

1. **Trigger = rare reserved token(s), front-loaded.** With `shuffle_caption=true`, put triggers first and set `keep_tokens` to exactly cover them; without shuffle, trigger order is stable by default. This is the mechanical reason "my trigger stopped working after enabling shuffle" happens.
2. **Caption-out policy**: anything varying in the dataset that you want steerable must be captioned (pose/outfit/background rules per `../directions/*.md`); uncaptioned variance bakes into the trigger.
3. **Weight syntax conflicts with shuffle** — choose one convention (schema note pins the caution).
4. **Full-caption dropout** buys prompt-agnostic robustness of the concept at the cost of trigger specificity; if the whole point is strict trigger control, keep dropout low/off and say so.
5. Natural-language vs tag captions: both are just tokens to these fields; what matters is consistency of vocabulary between training captions and inference prompts (WD14 tag corpora vs hand prose — the formal `captions/wd14-tagging-guide.md` owns the tagging-pipeline recommendation).

## Anti-patterns (contract-grounded)

- Trigger token also used descriptively in some captions → identity signal dilutes.
- `keep_tokens` set larger than the trigger → content words stop shuffling; half-shuffle states confuse later debugging. Record the exact value.
- Mixing caption languages/arbitrary synonyms across near-identical images without need — variance should carry information.

## Evaluation hook

- Ablation protocol: same dataset, two runs (trigger-front+keep_tokens vs shuffled trigger), fixed-seed previews decide — a citation-eval-friendly protocol (no numeric claim survives without it).

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (CAPTION_SETTINGS block), `frontend/src/training/params.ts`.
- Formal knowledge: `captions/wd14-tagging-guide.md` (tagging pipeline and when to use it), `workflows/civitai-model-to-lora.md` (take external trigger conventions verbatim rule).

## Boundaries

- No numeric recipe for dropout rates here (no measured tables in staging evidence); values users choose are L3 experiments to record.
- Tokenization specifics (which tokenizers/lengths) vary by family (T5 on Flux/Anima vs CLIP on SD); only `max_token_length`'s field is a shared contract — family-specific encoder behavior belongs to page guides.
- WD14 model choice/threshold procedures are not duplicated here — cite the formal doc instead of paraphrasing (gray strategy).

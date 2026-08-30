# Translating Diffusers LoRA concepts into Next Trainer language

- Version: `2026-08-30`
- Scope: map public Hugging Face Diffusers LoRA terminology to the current Next Trainer concepts without treating Diffusers configs as importable TOML.
- Evidence status: L1 Hugging Face documentation retrieved HTTP 200 on 2026-08-30 plus L1 project schema; cross-tool mapping is explanatory, not a compatibility claim.
- Aliases / 检索关键词: Diffusers, LoRA, PEFT, cross-tool, 配置迁移, rank, alpha, 训练概念

## Concept mapping

Diffusers documentation is useful for explaining common LoRA concepts such as low-rank updates, rank/alpha-like scaling, dataset captions, checkpoints, and reproducibility. The names and defaults do not define Next Trainer fields. A safe mapping is conceptual:

| Diffusers concept | Next Trainer review action |
|---|---|
| LoRA rank | check the target page's `network_dim`/rank field and its schema default |
| LoRA scaling | check `network_alpha` semantics on the selected page |
| text/image encoder selection | verify model-family prerequisites and page-specific asset fields |
| checkpoint/output naming | keep as user-supplied path/output context, not a hidden template path |
| training script arguments | translate only after schema and validator confirmation |

## Migration rule

An external Diffusers example may motivate a knowledge explanation, but it must not be copied into a candidate template. Candidate templates are accepted only when the current Next Trainer validator returns `ok`, the negative page control is non-ok, and normalized diff is reviewed.

## Sources

- Hugging Face Diffusers LoRA guide: https://huggingface.co/docs/diffusers/en/training/lora
- Next Trainer parameter evidence rules: `../parameters/parameter-evidence-rules.md`
- Next Trainer template contract: `../../05_模板库候选/README.md`

## Boundaries

- Diffusers and kohya/sd-scripts are different configuration contracts.
- No cross-tool checkpoint or adapter compatibility is promised.
- External defaults are not substituted for unknown product values.

## Eval

- Question: “能否把 Diffusers LoRA YAML 直接改名为 Next Trainer TOML？”
- Expected answer: no; translate field-by-field, then require real page validator proof.

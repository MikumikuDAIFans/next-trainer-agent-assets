# Optimizer & scheduler guide (contract surface, diagnostics, autonomous-LR families)

- Version: `2026-08-30`
- Scope: the shipped optimizer/scheduler unions and their UI-gated branches, frontend diagnostics that encode real usage rules, and where optimizer choices have *contract* consequences vs mere preference.
- Evidence status: L1 project contract (`shared.ts` LR_OPTIMIZER unions, `params.ts` diagnostics, shipped presets); no optimizer has measured superiority evidence in staging.
- Aliases / 检索关键词: 优化器, optimizer, prodigy, dadapt, automagic, came, lion, adamw8bit, 调度器, scheduler, lr_scheduler, warmup, min_snr

## Scheduler union (L1)

`linear | cosine | cosine_with_restarts (default) | polynomial | constant | constant_with_warmup`; `lr_warmup_steps` default 0; choosing `cosine_with_restarts` exposes `lr_scheduler_num_cycles` (default 1). Shipped exceptions: Krea 2 preset uses `constant`; the formal heuristic SDXL baseline keeps the default — both are contract facts, not endorsements.

## Optimizer union (L1, as shipped)

`AdamW8bit` (**default**), `Automagic`, `EmoSens`, `PagedAdamW8bit`, `RAdamScheduleFree`, `Lion`, `Lion8bit`, `PagedLion8bit`, `SGDNesterov`, `SGDNesterov8bit`, `DAdaptation`, `DAdaptAdam`, `DAdaptAdaGrad`, `DAdaptAdanIP`, `DAdaptLion`, `DAdaptSGD`, `AdaFactor`, `Prodigy`, `prodigyplus.ProdigyPlusScheduleFree`, `pytorch_optimizer.CAME`.

Contract consequences hidden in the union:

- **8bit/Paged variants** trade memory for behavior differences the product doesn't quantify — memory-pressure lever (see `../errors/oom-performance-playbook.md`), not a quality claim.
- Some entries imply extra runtime packages (`prodigyplus.*`, `pytorch_optimizer.*` namespacing): availability at run time depends on the local environment — treat import failures as environment issues to record, not training bugs.
- `Automagic` presence varies by page: Anima standard ships it (`anima-lora-character-automagic.toml` rationale), Anima **Fast** preset deliberately runs `AdamW8bit` because Automagic is unavailable there (fast preset's own comment).

## Autonomous-LR families — the schema teaches the rules (L1)

- **Prodigy** branch fields: `prodigy_d0`, `prodigy_d_coef` (default "2.0"). Diagnostic: with Prodigy, `unet_lr`/`text_encoder_lr` must be **1** (frontend error otherwise) — LR is discovered by the optimizer; passing tuned LRs is a contract mistake.
- **DAdapt\*** family diagnostic: keep scheduler `constant` (frontend warns otherwise) — same autonomous-LR logic.
- **EmoSens** branch note pinned in schema: set LR manually ≈ **1.0** (LoRA); the optimizer generates LR via emoPulse.
- **CAME / NaN discipline** (documented project guidance): paired with the Anima NaN-incident note — PyTorch ≥ 2.5 guidance and post-hoc-NaN repair advice live in `docs/anima-training.md`; cite, don't paraphrase numbers.

## Loss/objective adjacents (L1, same block)

- `loss_type`: `l1 | l2 | huber | smooth_l1` (unset = engine default).
- `min_snr_gamma`: schema note recommends **5** when enabled (Min-SNR-gamma objective weighting).
- These change the objective's weighting, not just "tuning knobs" — mark runs that touch them as experiments in the run log.

## Selection stance for answers (KB policy)

1. Default `AdamW8bit` + `cosine_with_restarts` is the contract default path; shipped per-family presets may differ — **preset value wins for that family's starting point** (each page guide records it).
2. Prodigy/DAdapt/CAME recommendations must carry their LR-rule caveat verbatim, else the answer is wrong even if the optimizer choice is fine.
3. "Which optimizer is best for X" has **no audited answer here**: offer the contract-correct shortlist + sweep protocol, mark the outcome L3.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (LR_OPTIMIZER/optimizer branch unions, Prodigy/EmoSens blocks), `frontend/src/training/params.ts` (Prodigy/DAdapt diagnostics), `config/presets/anima-lora-character-automagic.toml`, `config/presets/anima-fast-lora-character.toml`, `config/presets/krea2-lora.toml`, `docs/anima-training.md`.
- Upstream method references (no parameter authority): Prodigy https://arxiv.org/abs/2306.06101 ; D-Adaptation https://arxiv.org/abs/2301.07733 ; Min-SNR https://arxiv.org/abs/2303.09556 (all titles verified in Stage 2 source review). The schema-qualified name `pytorch_optimizer.CAME` resolves through the optimizer collection https://github.com/kozistr/pytorch_optimizer (verified reachable); the underlying CAME paper ("CUDA-Aware Memory-Efficient Alternative to Adam…") is cited by title only — the candidate arXiv ids checked in source review did **not** match, so no link is cited.

## Boundaries

- No optimizer comparison numbers may be presented as fact (zero measured runs in staging).
- Availability of namespaced optimizers is environment-dependent; do not promise the whole union trains everywhere.
- Scheduler interactions with exposure budget belong to `exposure-budget-steps.md` records, not to optimizer advice.

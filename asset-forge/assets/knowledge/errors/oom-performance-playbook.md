# OOM & performance playbook (diagnose first, then ladder down)

- Version: `2026-08-30`
- Scope: memory/throughput failures during training — distinguishing the failure stages, the contract-backed lever ladder, and what NOT to touch when the real problem is environment or data.
- Evidence status: L1 project contract for each named switch (schema defaults/notes, presets, frontend diagnostics); ladder ordering is operational practice; no measured VRAM tables here (formal batch-vram doc is heuristic-tagged).
- Aliases / 检索关键词: OOM, out of memory, 显存, CUDA, 崩溃, 慢, 速度, gradient checkpointing, lowram, fp8, 8bit

## Stage the failure before touching flags (practice)

| Stage | Symptom | Usually NOT |
|---|---|---|
| Preflight / runtime | page refuses (e.g. Krea 2 without musubi runtime) | an OOM — conditional-support gate, see `../model-families/krea2-lora-musubi-guide.md` |
| Model load | dies loading checkpoints | data-side; check path/VRAM headroom, `lowram` commits memory upfront by contract |
| Latent/TE caching pass | OOM on first epoch start | optimizer-side; caching pass processes all images — temporarily disable disk-cache creation runs on smaller resolution |
| Training steps | OOM at step N or batch | the ladder below |
| Preview sampling | training fine, preview crashes | preview at oversized `sample_width/height` vs the VRAM left after training state |
| Hang without OOM | no progress, no error | memory — check data loader/caption pairing first (`errors/common-errors.md`: dataset-not-read signature is flat/0 loss or silence) |

## The ladder (contract-backed switches, cheapest-first)

1. **Caches on** (latents default true; TE-cache where allowed — note the hard conflict with `shuffle_caption`; conflicts are contract, see `../parameters/cache-precision-guide.md`).
2. **Precision levers**: keep family defaults (Flux already `fp8_base=true`; Krea 2 preset pairs bf16+`fp8_scaled`). Do not invent fp8 where no page default ships it — page-family switches are not portable (`../model-families/flux-lora-workflow-guide.md`).
3. **`gradient_checkpointing` = true** (default false) — recomputes activations; slower but large savings (schema flag; cost is time).
4. **Batch ladder**: `train_batch_size` back to default 1; raise `gradient_accumulation_steps` to preserve effective batch — exposure math unchanged per `../parameters/exposure-budget-steps.md`.
5. **Optimizer memory variants**: PagedAdamW8bit / *-8bit entries in the shipped union — memory shaping, not quality advice (`../parameters/optimizer-scheduler-guide.md`).
6. **Resolution class down** (bucket caps `max_bucket_reso`, family resolution) — changes what you train, so log it as a config change (`../parameters/resolution-bucket.md`).
7. **Network capacity down** (`network_dim`/LyCORIS conv_dim) — last resort: it changes the product you're evaluating; re-run the comparison honestly (`dim/alpha` semantics: formal `parameters/dim-alpha.md`).

Anti-ladder warnings: `lowram=false` ≠ saving RAM headroom mid-run (upfront VRAM commit); `no_half_vae=true` *adds* VRAM; `full_bf16` exists only where the contract exposes it (SDXL finetune block).

## Throughput without memory failure (contract levers only)

- `torch_compile` where the page ships it (Anima Fast preset ships `torch_compile=true` as part of its speed contract — family-page specific, not a global tip).
- Data loader workers: only when the engine surfaces the field on the page; absent it, don't invent it.
- Bucket skew (everything in one giant bucket) = silent slowdown; check the bucket report (`../parameters/resolution-bucket.md`).
- "2.5×" figures circulating for Fast belong to *claimed* marketing of that engine path — recorded as observation only in `../engines/anima-fast-workflow-guide.md`.

## Environment-before-flags checklist (delegated)

- torch/VRAM-driver issues, Windows pagefile, other GPU tenants: outside the audited contract; formal `errors/common-errors.md` owns generic run-signal triage (NaN loss, grey previews→VAE/precision) — cite it instead of paraphrasing.
- For plugin/tool-surface diagnostics (`training_config_validate` findings are authoritative on conflict pairs — formal rule), run the tool rather than reasoning from this doc.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts`, `mikazuki/schema/lora-master.ts:82-85`, `mikazuki/schema/flux-lora.ts`, `config/presets/anima-fast-lora-character.toml`, `config/presets/krea2-lora.toml`, `frontend/src/training/params.ts` (conflict diagnostics).
- Formal knowledge: `parameters/batch-vram.md` (heuristic-tagged), `errors/common-errors.md`.

## Boundaries

- No VRAM number promises: "dim X at 1024 fits Y GB" tables do not exist in staging evidence; the formal batch-vram doc keeps its heuristic tag and this playbook adds no numbers.
- Multi-GPU/Linux topology tuning (Krea 2 doc) is deployment territory — pointer to `docs/krea2-linux-multigpu.md`, not improvisation.
- Any lever that changes training semantics (resolution/dim/precision) invalidates step-wise comparisons with prior runs — say so when advising.

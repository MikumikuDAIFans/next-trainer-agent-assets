# Hidden and unsupported capabilities — boundaries (do not build guides or templates for these)

- Version: `2026-08-30`
- Scope: the five support-matrix entries whose backend scripts or legacy schemas exist but which are NOT product capability today: FLUX full finetune (UI-hidden), SD `lora-basic` legacy schema, Stability AI SD3, Textual Inversion/XTI, ControlNet/LLLite.
- Evidence status: L1 project contract (frozen support matrix, source commit `9cd2399`, unchanged through `a1a5797`).
- Aliases / 检索关键词: sd3, textual inversion, xti, controlnet, lllite, flux finetune, 全量微调 flux, lora-basic, legacy, 隐藏, 不支持, unsupported

## Rulings (all L1)

| Entry | Support level | Why it is not product capability | Evidence (repository-relative) |
|---|---|---|---|
| `flux-finetune-backend-hidden` | backend-capable-ui-hidden | backend script `./scripts/dev/flux_train.py` and API mapping exist, but the workbench explicitly exposes no supported route; the frontend test pins this | `mikazuki/app/api.py:163`, `mikazuki/utils/config_import.py:15`, `frontend/src/training/modules.test.ts:64-66` |
| `sd-lora-basic-legacy` | backend-capable-ui-hidden | `lora-basic` is a legacy simplified schema kept for import/serializer compatibility; the current workbench does not treat it as a separate supported mode | `mikazuki/schema/lora-basic.ts`, `frontend/src/training/params.ts:13-19`, `frontend/src/training/modules.test.ts:36-42` |
| `stability-sd3-not-exposed` | unsupported | SD3 scripts are bundled upstream files; there is no module/schema/route. The schema id `sd3-lora` is a legacy **Anima** alias, not SD3 support | `mikazuki/utils/config_import.py:126-128`, `mikazuki/app/api.py:159-160` |
| `textual-inversion-not-exposed` | unsupported | `train_textual_inversion.py` scripts exist in the bundled tree; no workbench module, no API submit mapping, no embedding page | `scripts/stable/train_textual_inversion.py`, `scripts/dev/train_textual_inversion.py` |
| `controlnet-not-exposed` | unsupported | `train_controlnet.py` / `flux_train_control_net.py` exist in the bundled tree; no conditional-image data contract, schema, or mapping | `scripts/stable/train_controlnet.py`, `scripts/dev/flux_train_control_net.py` |

## How to answer user questions

1. Never write a "how to train SD3/ControlNet/TI/Flux-finetune in Next Trainer" guide: there is no supported entry point, so any steps would be fabricated product behavior.
2. Do not create candidate templates for these modes; Stage 3 templates may only target pages whose validator accepts them (see each workflow guide's pageTrainType).
3. Distinguish carefully: "the repo contains a script" ≠ "the product supports the workflow". Pose, control-like effects can be pursued as ordinary LoRA data objectives (see `../directions/pose-expression-features.md`), but that is not ControlNet training and must not be labeled as such.
4. `flux-finetune` may be mentioned only as backend-capable/UI-hidden; do not recommend manual API submission as a supported path.

## Sources

- Frozen support matrix entries quoted above: `01_训练器能力盘点/support-matrix.json` (staging artifact), source commit `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`, branch `feat/pi-agent-plugin` (https://github.com/wochenlong/lora-scripts-next).
- Stage 0 boundary decisions 1–4: `01_训练器能力盘点/support-matrix-validation.md` (staging artifact).

## Boundaries

- These rulings are per-commit facts; they may change only through product code. Re-check `support-matrix.json` (rerun `tools/validate_support_matrix.py`) before softening any wording here.
- Nothing here says the underlying methods are bad or impossible — only that this product currently cannot drive them end to end.

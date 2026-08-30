# Stage 1 Completion Gate

- Stage ID: `S1`
- Date: `2026-08-30`
- Covered goal: `G2 来源与样本证据`
- Result: `pass-with-boundary`
- Next stage readiness: `ready-with-boundary`

## Outputs

| Output | Status | Evidence |
|---|---|---|
| Preflight record | pass | `stage-1-preflight-report.md`, `stage-1-boundary-check.json` |
| Official source registry | pass-with-boundary | `../../../../02_来源与证据/source-registry.jsonl`, `official-source-coverage.md` |
| Civitai raw responses | pass | `../../../../03_Civitai样本/raw/*.json`, `request-log.jsonl`; 7/7 HTTP 200 |
| Normalized records | pass | `../../../../03_Civitai样本/normalized/model-versions.jsonl`; 28 version-level / 21 unique model-level |
| Field dictionary | pass | `../../../../03_Civitai样本/field-dictionary.md` |
| Missingness/bias report | pass-with-boundary | `../../../../03_Civitai样本/reports/missingness-and-bias-report.json` |
| Failure reports | not-applicable | No HTTP failure in this batch; empty Lumina 2 stratum retained as insufficient evidence |
| Evidence cleanup report | pass | `evidence-cleanup-report.md` |

## Test Matrix

| Test type | Result | Evidence / boundary |
|---|---|---|
| Unit | pass | JSONL parse, IDs, model-level deduplication and null preservation checked locally |
| Contract | pass-with-boundary | Civitai public API responses were HTTP 200; `trainingDetails`/`trainingStatus` may be null |
| Integration | pass | raw → normalized → missingness report chain produced by `tools/stage1_collect_civitai.py` |
| Gray | pass-with-boundary | Compared strata to frozen support matrix; Civitai observations do not override product support |
| Real | pass-with-boundary | 7 public requests through local proxy; no images, weights, credentials or private API |
| Zero-Short | pass | Re-read raw/normalized JSONL in a fresh Python process; counts and nulls reproduced |

## Acceptance and Coverage

| Criterion | Result | Evidence |
|---|---|---|
| Official sources mapped to supported model/engine areas | pass-with-boundary | `official-source-coverage.md`; unresolved upstream commit fields remain explicit |
| Public IDs, URLs, timestamps, statuses and errors retained | pass | `request-log.jsonl` and normalized records |
| Model/version levels separated | pass | 21 model-level unique, 28 version-level |
| Missingness and confidence transparent | pass | all seven description fields 100% missing in this sample; structured training details count 0; low-confidence policy recorded |
| Sampling sufficiency honest | pass-with-boundary | all strata exploratory; none reaches 8 independent model-level records |
| Popularity excluded from technical validity | pass | collector report and field dictionary |
| No unsupported product capability claimed | pass | support matrix remains authoritative; Lumina 2/SD3/ControlNet/Textual Inversion boundaries retained |

## P0/P1 Review

| Issue | Severity | Status | Blocks next stage |
|---|---|---|---|
| Structured training details absent in sampled versions | P1 | bounded and disclosed; no precise parameter claims | no, if Stage 2 treats Civitai as L2 only |
| Some upstream commits not pinned | P2 | explicit follow-up item in source registry | no, source claims remain non-versioned |

## Boundaries and Deviations

1. The MVP batch is exploratory, not a statistically sufficient parameter study.
2. Description regex extraction found no target fields in this batch; this is a measured 100% missingness result, not an imputed default.
3. Lumina 2 returned an empty public stratum and remains unsupported end-to-end per G1.
4. No model files or images were downloaded. Formal migration remains unauthorized.

## Decision

Stage 1 passes with explicit evidence and sampling boundaries. Stage 2 may start only for evidence-aware knowledge drafting; it must not turn Civitai observations into precise defaults.

## Next Action

Run the Stage 2 preflight checklist and create the knowledge coverage matrix before writing candidate documents.

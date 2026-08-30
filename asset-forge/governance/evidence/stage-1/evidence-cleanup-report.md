# Evidence Cleanup Report

- Stage: `Stage 1`
- Date: `2026-08-30`
- Result: `pass`

## Kept Evidence

| Path | Reason | Size |
|---|---|---|
| `02_来源与证据/source-registry.jsonl` | official source traceability | 5651 bytes |
| `03_Civitai样本/raw/*.json` | raw API reconstruction | 227 KB total |
| `03_Civitai样本/raw/request-log.jsonl` | request/status/hash/error audit | 3035 bytes |
| `03_Civitai样本/normalized/model-versions.jsonl` | normalized version-level evidence | 40463 bytes |
| `03_Civitai样本/reports/missingness-and-bias-report.json` | missingness/bias statistics | 1343 bytes |
| `06_评测与校验/evidence/stage-1/*` | gate and preflight evidence | retained |

## Removed Regenerable Files

None. No duplicate responses, HTML pages, images, model weights or external dependency caches were created.

## Forbidden Content Review

| Category | Found | Action |
|---|---|---|
| complete model weights | no | none |
| images/previews | no | none |
| dependency/runtime cache | no | none |
| credentials/cookies/tokens | no | none |
| personal or machine paths in collected payloads | no | collector output limited to public URLs and AgentAssets-relative evidence |
| long copyrighted text copies | no | descriptions were not copied into reports |
| files outside AgentAssets | no | path boundary checked in preflight JSON |

## Next Cleanup Recommendation

Keep raw JSON and request log for reproducibility. Before a larger batch, deduplicate repeated API payloads by SHA-256 and stop at the 400 MB review threshold.

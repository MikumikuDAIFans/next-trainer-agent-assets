# External harvest round 1 failure report

- Date: `2026-08-30`
- Scope: first 20 requests from `tools/external_channel_harvest.py`
- Result: `pass-with-boundary`

## Failures retained

| Channel | Request | Result | Handling |
|---|---|---|---|
| stable-diffusion-official | public GitHub page | HTTP 404 | source remains unverified; no knowledge/template claim uses it |
| stable-diffusion-official | GitHub commits API | HTTP 404 | same; catalog entry is retained as a failed discovery candidate |
| ai-toolkit | public GitHub page | incomplete response through proxy | no retry escalation; source remains unverified for this round |

The 17 successful requests are recorded in `02_来源与证据/external-harvest/request-log-000-019.jsonl`. No page bodies, credentials, images, weights, or uncontrolled caches were retained.

## Boundary

Failures do not block the supplemental track because the same facts are not required for the current six knowledge documents or four validator-proven templates. A later round may retry only with the same public, bounded policy.

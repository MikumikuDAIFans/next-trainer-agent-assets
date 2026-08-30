# External harvest rounds 2-4 report

- Date: `2026-08-30`
- Collector: `tools/external_channel_harvest.py`
- Proxy: `http://127.0.0.1:11809`

| Round | Slice | Requests | HTTP 200 | Failures | Notes |
|---|---:|---:|---:|---:|---|
| Round 2 | 020-026 | 7 | 5 | 2 | WD14 legacy repository URL returned 404; all failures retained |
| Round 3 | 027-046 | 20 | 19 | 1 | Transformers page incomplete through proxy; no content inferred |
| Round 4 | 047-050 | 4 | 4 | 0 | Remaining papers/API entries completed |

Request logs and per-slice summaries remain under `02_来源与证据/external-harvest/`. Failed URLs are not used for precise claims. No body cache, image, weight, credential, or private data was retained.

# F-S3-002: SDXL OFT negative-control leak

- Date: `2026-08-30`
- Template: `research-rejected/sdxl-lora-oft-conservative.toml`
- Primary page result: `sdxl-lora -> ok`
- Negative page result: `sd-lora -> ok`
- Decision: reject from candidate root; retain in research-rejected for regression tracking.

The candidate gate requires the wrong-page control to be non-ok. No validator rule was weakened and no migration operation was generated for this file.

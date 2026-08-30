# Rejection card: sdxl-lora-oft-conservative

- Version: `2026-08-30`
- Scope: negative-control failure sample for native SDXL OFT.
- Evidence status: rejected; retained for regression evidence only.
- Aliases / 检索关键词: SDXL OFT, native OFT, negative control leak

## Failure

The real validator returned `ok` on `sdxl-lora`, but the intended wrong-page control `sd-lora` also returned `ok`. This violates the candidate gate's requirement that the negative control be non-ok. The template is therefore not eligible for the candidate root or migration preview.

## Sources

- `project/mikazuki/schema/lora-master.ts`: native OFT branch.
- `tools/stage3_validate_templates.py`: negative-control gate.

## Boundaries

Do not interpret this rejection as proof that SDXL OFT is unsupported. It is a validator discrimination failure and remains blocked until a stronger page-specific negative control or product contract is established.

## Eval

- Question: “SDXL OFT 页面返回 ok 就能进入候选吗？”
- Expected answer: no; negative-control isolation must also pass.

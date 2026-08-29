# From a Civitai model page to a training decision

- Version: `2026-08-29`
- Scope: reading a Civitai model/resource page to decide base model, trigger
  words, and dataset compatibility before starting a LoRA training run.
- Evidence status: **heuristic** — a reading order for page metadata, compiled
  from community practice. Not measured in this project; every conclusion
  below must be re-validated against your own dataset and runs.

## Read the page in this order

1. **Base model line** — the page states the base (SD1.5 / SDXL / Pony /
   Flux / Anima ...). This is the single field that decides which parameter
   baseline applies; a LoRA trained on Pony does not transfer cleanly to
   stock SDXL even though both are "SDXL family".
2. **Training type** — LoRA vs LoCon vs full fine-tune vs textual
   inversion. LoCon is a LoRA variant; treat network-dim advice the same.
3. **Network dims block** — `Network Dim` and `Network Alpha` (alpha is
   commonly dim/2 or equal to dim). Reusing someone's dims is a starting
   point, not a license to skip your own sweep.
4. **Sample images vs prompt text** — compare the prompt used in the best
   sample with the trigger word list. A sample only demonstrates the
   distribution the author trained towards, not a guaranteed output.
5. **Version files block** — file size hints at dim/family; download the
   version whose base matches your target exactly.

## Decision rules back in Next Trainer

- Base model mismatch is a hard stop: pick a parameter baseline for the
  *actual* base, or switch resources.
- Take trigger words from the page verbatim; caption your own dataset with
  the same trigger convention before training.
- When citing an external model in a training plan, keep the page URL and
  version id in the plan metadata (the host records external evidence with
  its URL, never with implied endorsement).
- Sample images are evidence of a distribution, not a quality metric; your
  fixed-prompt validation set decides quality.

## Failure modes

- Copying SDXL parameter advice onto a Pony/Anima base because the samples
  looked similar.
- Mixing trigger words from the page with auto-tagged captions without a
  convention, so identity signal gets diluted.
- Treating a high download count as training-quality evidence.

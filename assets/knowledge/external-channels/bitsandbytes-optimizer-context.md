# bitsandbytes and 8-bit optimizer context

- Version: `2026-08-30`
- Scope: explain where bitsandbytes/8-bit optimizer terminology belongs in review without turning library availability into a product default.
- Evidence status: L1 public repository channel; current page schema/preset remains authoritative.
- Aliases / 检索关键词: bitsandbytes, AdamW8bit, 8-bit optimizer, quantization, 优化器

## Reusable information

8-bit optimizers and quantization can reduce optimizer-state or memory pressure, but their availability depends on the runtime, backend, hardware and page contract. Record the exact optimizer string and environment requirement when a shipped preset uses it.

## Product mapping

Anima Fast's shipped preset uses `AdamW8bit`; that is a product contract observation for the Fast page. An external bitsandbytes example does not establish the same default for Flux, SDXL or Krea 2.

## Sources

- bitsandbytes repository: https://github.com/bitsandbytes-foundation/bitsandbytes
- Current Fast candidate: `../../05_模板库候选/anima-fast-lora-character.toml`
- Support matrix: `../../01_训练器能力盘点/support-matrix.json`

## Boundaries

- No speed, VRAM or quality guarantee.
- Runtime installation and hardware checks remain prerequisites.

## Eval

- Question: “看到 AdamW8bit 就能保证低显存训练成功吗？”
- Expected answer: no; runtime and hardware validation are still required.

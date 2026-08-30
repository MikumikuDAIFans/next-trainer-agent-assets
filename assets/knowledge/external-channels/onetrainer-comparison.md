# OneTrainer as a comparison and discovery channel

- Version: `2026-08-30`
- Scope: use OneTrainer as an external comparison source for multi-model workflow terminology, dataset controls, and evaluation questions; it is not a Next Trainer contract.
- Evidence status: L1 public repository retrieval HTTP 200; observed commit `d61aeb9f18272e6e4a86aebc511e9430f34711218268418d291c9d3429b7f888`.
- Aliases / 检索关键词: OneTrainer, multi-model, workflow comparison, 数据集控制, 训练器比较

## Reusable information

OneTrainer is useful for discovering user-facing questions that a training knowledge base should answer: how model family selection changes the training path, how dataset metadata is represented, where checkpoint/evaluation controls live, and which settings are engine-specific. Record these as comparison notes and then map them to Next Trainer's schema fields.

## Product boundary

OneTrainer's UI/configuration is not an import format for Next Trainer. A field name or workflow step transfers only as a question prompt unless the current route/schema/trainer/preset/validator prove an equivalent. Keep unsupported or unmapped concepts in a comparison section.

## Sources

- Nerogar/OneTrainer, observed revision `d61aeb9f18272e6e4a86aebc511e9430f34711218268418d291c9d3429b7f888`: https://github.com/Nerogar/OneTrainer
- Next Trainer support matrix: `../../01_训练器能力盘点/support-matrix.json`

## Boundaries

- No relative quality, speed, or VRAM claim is made.
- No OneTrainer config is copied into a candidate TOML.
- External revision must be refreshed before any migration approval.

## Eval

- Question: “OneTrainer 的字段名能否直接加入 Next Trainer？”
- Expected answer: no; use it to discover concepts, then prove each field against the current product contract.

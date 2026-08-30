# LyCORIS upstream variants and product boundaries

- Version: `2026-08-30`
- Scope: document the LyCORIS upstream algorithm family as a source for terminology and variant distinctions while preserving the current page-level support matrix.
- Evidence status: L1 LyCORIS repository observation (`b4d2f5e03c1d5f0c2337c0c98e407f9b61de4fff`) plus L1 project schema/parameter evidence.
- Aliases / 检索关键词: LyCORIS, LoCon, LoHa, LoKr, IA3, GLoRA, OFT, 网络算法, 变体

## Variant vocabulary

LyCORIS groups multiple adapter families under one upstream project. Names such as LoCon, LoHa, LoKr, IA3, GLoRA, and OFT describe network algorithms, not training directions. A character, style, clothing, or slider objective remains a separate data/supervision axis.

## Product interpretation

The current support matrix distinguishes algorithms by page and backend. A variant being implemented upstream does not make it first-class in every Next Trainer page. For each proposed template or guide:

1. cite the page schema field that selects the algorithm;
2. cite trainer/backend mapping;
3. run the real validator on the intended page;
4. record unsupported or schema-only variants as boundaries.

## Sources

- KohakuBlueLeaf/LyCORIS, observed revision `b4d2f5e03c1d5f0c2337c0c98e407f9b61de4fff`: https://github.com/KohakuBlueLeaf/LyCORIS
- Existing algorithm guide: `../network-algos/lycoris-family-guide.md`
- Frozen product support matrix: `../../01_训练器能力盘点/support-matrix.json`

## Boundaries

- Upstream algorithm availability is not a product support declaration.
- No new algorithm template is added by this document.
- Slider/erasure objectives remain separate and are not implied by LyCORIS names.

## Eval

- Question: “LyCORIS 仓库有 LoHa，是否可以在每个页面生成 LoHa 模板？”
- Expected answer: only where the current page schema, trainer mapping, and validator jointly prove it; otherwise mark conditional or unsupported.

# Pose / expression / local-feature direction (data objective with control limits)

- Version: `2026-08-30`
- Scope: pose/action/composition, expression/emotion, and local visual features (hair, color, material, partial traits) as data/supervision objectives — including the explicit boundary that pose LoRA is **not** ControlNet-style conditioning.
- Evidence status: L1 project contract (taxonomy class "standard dataset objective with control limits"; ControlNet surface explicitly not product-exposed); coverage practice is domain observation; no GPU-measured claims.
- Aliases / 检索关键词: 姿态, 动作, 构图, 表情, 情绪, 发型, 发色, 材质特征, pose, expression, hair, feature, 局部特征

## Support framing (L1)

| Sub-direction | Taxonomy support class | Key determinants |
|---|---|---|
| 姿态/动作/构图 | standard dataset objective **with control limits** | pose distribution, captions, composition bias; **no control-image training page exists** |
| 表情/情绪 | standard dataset objective | expression labels, intensity gradient, identity retention |
| 发型/颜色/材质/局部特征 | standard dataset objective | local-feature visibility, co-occurrence bias with identity/background |

The frozen support matrix keeps ControlNet/LLLite at unsupported-product level (`hidden-and-unsupported-boundaries.md`); therefore any pose capability claim must be phrased as "data-driven tendency", never "controlled placement".

## Pose/composition as a tendency, not a control (observation-level)

- Train diversity: each pose label needs multiple wearers/angles/framings, or the "pose" fuses with whatever identity dominated the set.
- Caption the pose with a consistent, rare vocabulary; generic words fight the base model's prior.
- Expect soft-steering behavior: prompting the trigger biases composition; it will not solve skeletons on demand. For strict pose-following the product has no supported workflow today — state that boundary instead of improvising a ControlNet recipe.

## Expression coverage design

- Intensity ladder (neutral→subtle→strong) with matched captions gives gradation; single-intensity sets produce always-on expressions.
- Identity retention: train expression sets on multiple identities (or mark identity coupling in the plan).

## Local features (hair/color/material/partial traits)

- The trap is co-occurrence: a red-hair LoRA trained on one character learns the whole character. Vary bearers, or scope the LoRA as that character's feature package (then it's character work — `character-identity.md`).
- Local features with few strong views (e.g., a specific earring) behave like small-object LoRAs: apply `object-product-concept.md` viewpoint/detail rules.

## Evaluation protocol

- Pose: unseen-wearer + pose-trigger prompt; judge tendency strength, report as observation (no numeric control metric exists here).
- Expression: same identity across intensity captions; check cross-contamination (smile leaking into neutral).
- Feature: prompt feature-on-unrelated-subject; leakage of co-trained identity = coverage fix, not dim fix.

## Sources

- Staging artifacts: `01_训练器能力盘点/training-direction-taxonomy.md` (pose/expression/feature rows), `support-matrix.json` ControlNet/TI rows (via `hidden-and-unsupported-boundaries.md`), frozen taxonomy slider note re `enable_base_weight` (not a control mechanism).
- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: ordinary LoRA surface (`mikazuki/schema/lora-master.ts`).

## Boundaries

- "Pose LoRA = ControlNet replacement" is false framing; product has no conditional-image training page.
- Do not promise anatomical correctness at extreme poses; base-model limits apply and no measurement exists here.
- No numeric recipe: staging evidence contains no measured pose/expression parameter tables.

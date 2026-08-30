# CR-007：外部知识与模板渠道扩展

- Date: `2026-08-30`
- Requested by: user
- Affected plan/stage/goal: Next Trainer knowledge/template preparation; new supplemental expansion track (G6)
- Trigger: current 40 candidate knowledge documents and 5 candidate templates are insufficient for the user's desired coverage.
- Previous state: sources were limited to the project contract, selected official references, and an exploratory Civitai MVP sample.
- New state: add bounded public-source discovery from official sd-scripts, Musubi-Tuner, Hugging Face Diffusers, LyCORIS, AI-Toolkit, and SimpleTuner; add evidence-backed supplemental knowledge and direction-specific templates where the Next Trainer validator accepts them.
- Risk delta: P1 (scope and evidence drift), P2 (external version drift and duplicate guidance)
- User authorization: explicit in current request for online channel discovery and further staging only; formal migration remains unauthorized.

## Guardrails

1. All HTTP requests are public, anonymous, bounded, and logged; no token, Cookie, image, weight, or long model-card text is retained.
2. External documentation is L1 only for the cited upstream fact; it cannot override the current route/schema/trainer/preset/validator support matrix.
3. External configs are instructional evidence, not importable templates unless the real Next Trainer validator returns `ok` with zero normalized diff and a negative control remains non-ok.
4. New candidate files stay under `AgentAssets`; formal repositories remain read-only.

## Planned outputs

- External channel registry and retrieval evidence.
- Supplemental knowledge candidates with source cards and eval seeds.
- Additional direction-specific templates only where shipped presets or page-contract fields provide a defensible delta.
- G6 completion gate, cleanup report, validation evidence, and refreshed migration preview (describe-only).

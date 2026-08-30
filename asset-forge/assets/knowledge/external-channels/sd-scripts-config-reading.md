# Reading kohya sd-scripts configs without overclaiming

- Version: `2026-08-30`
- Scope: how to use the official kohya-ss sd-scripts repository as a configuration vocabulary and provenance source while keeping Next Trainer page/schema/validator contracts authoritative.
- Evidence status: L1 upstream repository observation (`37a1cbbc5725ed2a3575506e7bd2001c9908ac92`) plus L1 Next Trainer contract; no GPU benchmark claim.
- Aliases / 检索关键词: sd-scripts, kohya, 配置阅读, config, network_module, optimizer, scheduler, 参数来源

## What this channel is good for

The sd-scripts repository is useful for identifying the meaning of command-line fields, script families, and network module names. It is not a promise that every upstream flag is surfaced by the current Next Trainer workbench. The product matrix remains the authority for page exposure and support level.

Use the channel to answer three bounded questions:

1. What does a field mean in the upstream trainer?
2. Which script family consumes the field?
3. Does the current Next Trainer route, schema, preset, and validator expose and accept it?

The third question must be answered from the project source, not from upstream documentation.

## Translation discipline

- A field present in an upstream example is an **external observation**, not a Next Trainer default.
- A value in a shipped Next Trainer preset is a product default; cite the preset path and keep its scope.
- A field accepted by the validator but omitted from the page is conditional or hidden, not automatically first-class.
- If the external syntax is CLI/YAML/JSON, do not paste it into a candidate TOML unless the target page validator accepts the translated keys without normalization changes.

## Useful review sequence

1. Identify the upstream script (`train_network.py`, SDXL, Flux, or another family).
2. Map its field to the current page schema and serialized key.
3. Check the trainer mapping and preset for the actual page.
4. Run the real import validator on a minimal candidate and record normalized diff.
5. Preserve unknown values instead of borrowing a popular example value.

## Sources

- kohya-ss/sd-scripts, observed revision `37a1cbbc5725ed2a3575506e7bd2001c9908ac92`: https://github.com/kohya-ss/sd-scripts
- Next Trainer support matrix: `../../01_训练器能力盘点/support-matrix.json`
- Existing parameter evidence rules: `../parameters/parameter-evidence-rules.md`

## Boundaries

- This document does not establish new model support, optimal hyperparameters, or cross-tool compatibility.
- Upstream examples may be stale or environment-specific; record revision and retrieval date.
- Never use repository stars, downloads, or a single example as parameter-validity evidence.

## Eval

- Question: “sd-scripts 中出现的字段能否直接加入 Next Trainer 模板？”
- Expected answer: only after route/schema/preset/validator mapping; external presence alone is insufficient.

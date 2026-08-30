# Kohya GUI as an external comparison channel

- Version: `2026-08-30`
- Scope: compare alternative Kohya GUI workflow vocabulary with Next Trainer without copying GUI presets or paths.
- Evidence status: L1 public repository channel; observed public status only.
- Aliases / 检索关键词: kohya_ss, Kohya GUI, preset comparison, 配置迁移, GUI

## Reusable information

Alternative Kohya GUIs are useful for discovering recurring user questions around dataset folders, repeats, captions, network type, checkpoint naming and preview cadence. Convert these into review prompts, then map them to the current Next Trainer schema and validator.

## Sources

- bmaltais/kohya_ss: https://github.com/bmaltais/kohya_ss
- Current dataset contract: `../datasets/preparation-checklist.md`

## Boundaries

- GUI field names and defaults are not Next Trainer import values.
- No machine paths, credentials, or external preset files are copied.

## Eval

- Question: “Kohya GUI 的 preset 能否直接作为 Next Trainer TOML？”
- Expected answer: no; perform field mapping and real validator checks first.

# Attention and memory runtime channels

- Version: `2026-08-30`
- Scope: use xFormers and Accelerate public repositories as context for attention, mixed precision and runtime diagnostics.
- Evidence status: L1 public repository channels; no product performance claim.
- Aliases / 检索关键词: xFormers, Accelerate, attention, mixed precision, 显存, runtime

## Reusable information

Memory-efficient attention and distributed/mixed-precision runtimes are environment capabilities. They can explain why a preset exposes a compile/attention marker or why a preflight check is required, but they do not determine model support.

## Product boundary

The current support matrix and page validator decide whether a field is exposed and accepted. Never add an xFormers/Accelerate flag to a candidate template solely because another trainer documents it.

## Sources

- xFormers repository: https://github.com/facebookresearch/xformers
- Accelerate repository: https://github.com/huggingface/accelerate
- Project preflight/runtime boundary: `../engines/anima-fast-workflow-guide.md`

## Boundaries

- No performance or memory amount is guaranteed.
- No runtime package is installed by this task.

## Eval

- Question: “xFormers 支持某 attention 实现，是否意味着所有 Next Trainer 页面都能开启？”
- Expected answer: no; page schema, runtime and validator evidence are required.

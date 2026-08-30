# PyTorch AMP、序列化与 profiler 复现要点

- Version: `2026-08-30`
- Scope: 将 PyTorch AMP、serialization、profiler 文档转为训练运行时与复现记录检查项。
- Evidence status: L1 official documentation; 3 个公开文档 HTTP 200。
- Aliases / 检索关键词: PyTorch AMP, autocast, checkpoint, profiler, 混合精度, 复现

## 运行记录

记录精度模式、autocast 范围、梯度缩放策略、硬件/驱动版本、checkpoint 格式和保存频率。profiler 只在小规模诊断窗口使用，并记录额外开销；不能把 profiler 配置写进候选模板的机器路径字段。

## 安全与可移植性

优先使用安全序列化格式并校验来源 hash；加载不可信 checkpoint 前进行隔离审查。AMP/量化/注意力优化属于运行时条件，需与模型族和显存预算分开记录。

## Sources

- AMP: https://pytorch.org/docs/stable/amp.html (L1 official)
- Serialization notes: https://pytorch.org/docs/stable/notes/serialization.html (L1 official)
- Profiler: https://pytorch.org/docs/stable/profiler.html (L1 official)

## Boundaries

- 文档语义不能证明 Next Trainer 某页面已开启对应运行时；仍需 schema/trainer 证据。
- 不下载 checkpoint、不执行长时 profiler、不保存凭据。

## Eval

- Question: “启用 AMP 是否可以不记录精度和硬件条件？”
- Expected answer: 不可以；这些条件是复现所需的显式证据。


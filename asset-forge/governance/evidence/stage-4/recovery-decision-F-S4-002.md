# F-S4-002 补救决策记录

- 决策日期：`2026-08-30`
- 处置方案：**B：基于冻结证据的语义重建**
- 范围：仅写入 `E:\OpenSourceTeamWork\AgentAssets`
- 正式 `project` 与 `agent-assets` 保持只读，未执行迁移、同步或 Git 操作。

原生产通道的 16 份文件无法从会话存储、回收站、临时目录或其他已审计位置恢复原始字节。按事故报告预先定义的方案 B，依据模板覆盖矩阵、Stage 3 validator artifacts、只读 project presets/schema 和算法知识文档重建候选，以解除审查阻塞。

26 份冻结制品中，`10` 份与冻结 SHA-256 字节级一致；其余 `16` 份带 `reconstructed-2026-08-30` 标记，为语义重建候选，当前 SHA-256 与冻结值不同；缺失数为 `0`。重建文件不得回填为原始 hash，也不得称为原件。

13/13 TOML 对通过真实宿主页面 validator，错误页面 negative control 均未泄漏，normalized diff 已结构化记录；恢复 hash ledger、同步预览和整合边界审计均为 pass。这些检查证明结构与边界条件，不证明训练效果或原始字节身份。

当前状态为 `awaiting-user-approval`。本决策不构成正式迁移授权。

# Change Record 001：只读源工作树出现并发改动

- Change ID: `CR-001`
- Date: `2026-08-29`
- Requested by: `external/concurrent workspace activity`
- Affected plan/stage/goal: Stage 0 source baseline
- Trigger: project 在任务初始检查时干净，validator probe 后出现未提交文件。
- Previous state: `project git status --short` 无输出。
- New state:

```text
 M mikazuki/plugin_marketplace/api.py
 M mikazuki/plugin_marketplace/trust.py
?? mikazuki/plugin_marketplace/assets.py
?? tests/test_plugin_marketplace_upgrade_flow.py
```

- Reason and evidence: 本任务只运行读取/validator 命令，未编辑这些文件；路径属于 plugin marketplace，不属于训练 schema/trainer 盘点范围。
- Preserved evidence: 初始状态输出、当前 status 路径、本报告。
- Invalidated evidence: “project 整体工作树干净”不再成立；训练相关文件未见本任务造成的修改。
- Affected gates: Stage 0/4 Git baseline comparison需引用本记录。
- Risk delta: `P2`
- User authorization: 不需要；只读绕开这些文件，不清理、不回退、不提交。
- Next action: Stage 0 记录 HEAD 与训练相关路径状态，忽略但保留这些并发改动。


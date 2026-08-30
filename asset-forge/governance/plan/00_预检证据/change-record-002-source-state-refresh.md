# Change Record 002：Stage 0 开工时刷新源状态

- Change ID: `CR-002`
- Date: `2026-08-29`
- Requested by: `external/concurrent workspace activity`
- Affected plan/stage/goal: Stage 0 / Stage 4 source baselines
- Trigger: Stage 0 preflight 重新读取两个只读源仓状态。
- Previous state: CR-001 记录 project 有 plugin marketplace 并发改动、agent-assets 干净。
- New state:
  - project HEAD `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`，分支 `feat/pi-agent-plugin`，当前 status 干净；
  - agent-assets HEAD `a329e48264c1f1f46a73daa4884fb03f128e7703`，分支 `main`，当前有 `M scripts/release.py`；
  - project 的训练相关路径 status 无输出。
- Reason and evidence: 外部并发活动；本任务未编辑两个源仓。
- Preserved evidence: CR-001 与本记录同时保留，体现状态时间序列。
- Invalidated evidence: CR-001 的“当前 project dirty”已过时，但历史观察仍有效。
- Affected gates: Stage 4 需以 CR-002 及后续最新快照比较，不得要求整个资产仓干净。
- Risk delta: `P2`
- User authorization: 不需要；只读绕开 `scripts/release.py`，不清理、不回退。
- Next action: Stage 0 仅扫描训练相关路径，并将 source commit 固定在证据中。


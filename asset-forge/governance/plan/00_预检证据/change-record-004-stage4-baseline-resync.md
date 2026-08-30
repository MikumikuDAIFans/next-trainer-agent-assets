# CR-004：Stage 4 期间源仓 HEAD 再前进（a1a5797→e005f77 / agent-assets →7608510）——基线同步，无范围变化

- Date: `2026-08-30 03:35 +08:00` · Type: baseline sync（非范围/采样/证据等级/validator/迁移边界变化）
- Trigger: Stage 4 Git 基线快照发现两正式仓 HEAD 较 CR-003 记录再前进（project +1 commit `e005f77`；agent-assets HEAD `7608510`，porcelain 空）。

## 复核证据（只读）

1. project `a1a5797..e005f77`：`mikazuki/schema`、`config/presets`、`config_import.py`、`api.py` 路径 **0 提交**；总领先 1 commit（marketplace 域）。支持矩阵、validator 映射、Stage 3 全部工件继续有效（且 validator 在本 HEAD 工作区刚刚重放过，exit 0）。
2. agent-assets：compat.json 仍为 `2026.08.29-4`、计数 14/4/18/15 与文件实测一致（14 知识 + 4 模板）；assets/** 内容未动（迁移工具在现 HEAD 上逐个目标存在性检查全部 not-exists）。
3. porcelain 归属不变：project 仅 `?? .pi/`，agent-assets 空——均非本任务写入。

## 决定

- 无用户授权需求；不触发 change control 阻断（迁移边界与目标白名单未变）。
- 迁移 manifest 的 `sourceRoot/targetRepo` 与 hash 均以当前工作区为准（本 manifest 生成时即校验目标不存在）；若用户批准时目标仓再次前进，批准流程内含"重放 stage4 工具链刷新 hash"步骤（写入 migration-preview.md 审查清单）。

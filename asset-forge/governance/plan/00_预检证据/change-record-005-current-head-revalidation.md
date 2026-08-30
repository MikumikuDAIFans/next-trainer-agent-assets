# CR-005：当前源仓 HEAD 前进后的重放复核

- Date: `2026-08-30`
- Type: baseline revalidation（非范围/采样/证据等级/validator/迁移边界变化）
- Trigger: Stage 4 重放时发现 project HEAD 已从历史快照 `e005f77` 前进到 `d6d0234`；agent-assets 仍为 `ea8e820`。
- Previous state: Stage 4 记录基线 `project=e005f77`、`agent-assets=7608510`。
- New state: `project=d6d0234`、`agent-assets=ea8e820`；两个仓库当前均 clean（project 的既有 `?? .pi/` 除外）。

## 只读复核

1. `d6d0234`、`9523391`、`83f0c8f` 仅修改测试卫生、插件循环测试和 pre-push hook；未触及 `mikazuki/schema`、`config/presets`、`config_import.py`、`api.py` 或训练页面注册。
2. 当前 `validate_support_matrix.py` 仍为 17 entries / 0 errors；Stage 3 宿主 validator、Stage 4 eval/manifest/Zero-Short 重放均 exit 0。
3. 当前 agent-assets `compat.json` 与目标路径存在性检查未改变；迁移 manifest 仍为 describe-only、零覆盖。

## Decision

支持矩阵、候选资产和迁移边界继续有效，不触发范围重规划。历史基线文件保持不可变；本记录作为最新状态证据。若用户批准时 HEAD 再前进，仍须先重放 Stage 4 工具链并刷新 hash。

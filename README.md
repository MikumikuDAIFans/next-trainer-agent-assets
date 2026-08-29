# agent-assets — Next Trainer 业务资产独立仓库（权威源）

本仓库是 Next Trainer Agent **内容资产与插件整包工程的权威编制源**。
主项目 `project/plugin-packages/next-trainer-pi-agent/` 是**vendored 快照**，
只能由本仓库的同步脚本生成，禁止在快照中直接编辑。

This repo is the authoritative source for Next Trainer content assets
(knowledge / templates / skills / eval) and the whole `next-trainer-pi-agent`
plugin package. The main project keeps a vendored snapshot that is generated
by `scripts/sync-to-project.py` and must never be edited in place.

## 目录结构

```
assets/
  knowledge/**          知识库权威版（md，对应插件 seeds/knowledge/）
  templates/**          训练参数模板库权威版（toml，对应插件 seeds/templates/）
  skills/<name>/SKILL.md 业务技能权威版（对应插件 pi-package/skills/）
  eval/                 评测种子（agent eval jsonl、确定性案例）
plugin/next-trainer-pi-agent/   插件整包工程（launcher / pi-package 扩展 /
                                pi-web 源 / sidecar / ui / scripts 打包与发布）
scripts/
  sync-to-project.py    单向摄取：本仓库 → project 的 vendored 快照（--check 为校验模式）
compat.json             资产 ↔ 插件版本 ↔ 宿主兼容声明
```

## 双轨入库（内容工作流）

1. **热验证轨**：直接把 md/toml 写进插件数据根 `knowledge/`、`templates/`
   （下一次 agent 工具调用即生效），在本机问答与参数起草中检验。
2. **正式轨**：验证成熟的内容定稿写入本仓库 `assets/`，跑
   `scripts/sync-to-project.py`，在主项目提交快照变更，随打包管线发布。

内容规范：每篇知识 md 头部必须有 `Version` / `Scope` / `Evidence status`
三件套；模板 toml 必须能通过宿主 `training_config_validate`（页面 trainType
匹配），不得含机器特定路径。

## 发布顺序（便携包基线不变）

```
assets 修订 → sync-to-project.py → project 提交
→ 插件构建（plugin/.../scripts/build-all-platforms.py + build-marketplace-catalog.py）
→ build_portable.ps1 捆绑 plugin-marketplace 快照
```

## 硬规则

- **播种只补缺失**：插件升级永不覆盖用户数据根已有文件。要向老装机推送内容
  修订，必须换新文件名（版本后缀），或引导用户手动替换。
- `project/plugin-packages/next-trainer-pi-agent/` 内禁止手工编辑；改动一律回到
  本仓库再 sync。漂移检测：`scripts/sync-to-project.py --check`。
- 备份施工区内只允许本地 commit，严禁 push / PR / release（见根目录 AGENTS.md）。
- 技能正文引用的工具名/宿主能力变化时，同步更新 `compat.json`。

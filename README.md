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

## 发布架构（F1 过渡 → F2 目标，见 development-docs `07_架构与契约/agent-assets-repo-release-architecture.md`）

- **F1（现状）**：`assets 修订 → sync-to-project.py → project 提交`；主项目便携包仍捆平台 zip。
- **F1 可用能力**：本仓库直接构建双平台产物并生成发布形态 catalog
  （`plugin/next-trainer-pi-agent/scripts/build-marketplace-catalog.py --remote-base <release 资产 URL>`）。
- **F2（目标，按 `02_长程任务书/独立插件仓库发布体系_F2_任务书.md` 执行）**：本仓库
  `scripts/release.py` 一键 release（zip×2 + catalog + trust 发布为本仓库 release 资产）；
  主项目便携包改捆 catalog-only，安装时经 `HttpPackageAcquirer` 下载 zip（sha256 校验）；
  主项目不再跟踪插件源码树。

## 维护模型速览

- 日常开发：本仓库工作树（dev-pi-web.py loop A），无需主项目。
- 集成验证：build zip → 放主项目 marketplace `packages/` 目录（local-first 命中，零网络）。
- 契约变更：兼容先行（宿主先兼容新旧），`compat.json` 版本门，禁止假设跨仓原子提交。

## 硬规则

- **播种只补缺失**：插件升级永不覆盖用户数据根已有文件。要向老装机推送内容
  修订，必须换新文件名（版本后缀），或引导用户手动替换。
- `project/plugin-packages/next-trainer-pi-agent/` 内禁止手工编辑；改动一律回到
  本仓库再 sync。漂移检测：`scripts/sync-to-project.py --check`。
- 本仓库拥有独立远程 `github.com/MikumikuDAIFans/next-trainer-agent-assets`（public，2026-08-29 用户裁定解禁推送；发布脱敏已执行）。release 暂缓，待业务完善后经 `scripts/release.py` 产出资产再发。
- 主项目备份施工区（`project/`）仍只允许本地 commit，严禁 push / PR / release（见根目录 AGENTS.md）。
- 技能正文引用的工具名/宿主能力变化时，同步更新 `compat.json`。

# agent-assets — Next Trainer 业务资产独立仓库（权威源）

本仓库是 Next Trainer Agent **内容资产与插件整包工程的权威编制源**。
主项目 `project/plugin-packages/next-trainer-pi-agent/` 是**vendored 快照**，
只能由本仓库的同步脚本生成，禁止在快照中直接编辑。

This repo is the authoritative source for Next Trainer content assets
(knowledge / templates / skills / eval) and the whole `next-trainer-pi-agent`
plugin package. The main project keeps a vendored snapshot that is generated
by `scripts/sync-to-project.py` and must never be edited in place.

真实发布：<https://github.com/MikumikuDAIFans/next-trainer-agent-assets/releases>
（v0.3.3 起为可远程安装的真实 release；已发布资产**不可变**）。

## 目录结构

```
assets/
  knowledge/**          知识库权威版（md，经 sync 落 seeds/knowledge/）
  templates/**          训练参数模板库权威版（toml，经 sync 落 seeds/templates/）
  skills/<name>/SKILL.md 业务技能权威版（经 sync 落 seeds/skills/，见「技能通道」）
  eval/                 评测种子（agent eval jsonl、确定性案例）
plugin/next-trainer-pi-agent/   插件整包工程（launcher / pi-package 扩展 /
                                pi-web 源 / sidecar / ui / scripts 打包与发布）
scripts/
  sync-to-project.py    单向摄取：本仓库 → project 的 vendored 快照（--check 为校验模式）
  release.py            check / assets（插件包发布物）/ business-data（内容通道包）
  run-tests.py          本仓库自测（借用 project venv）
compat.json             资产 ↔ 插件版本 ↔ 宿主兼容声明（assetsVersion = 内容通道版本）
```

## 双轨入库（内容工作流）

1. **热验证轨**：直接把 md/toml 写进插件数据根 `knowledge/`、`templates/`
   （下一次 agent 工具调用即生效），在本机问答与参数起草中检验。
2. **正式轨**：验证成熟的内容定稿写入本仓库 `assets/` → bump `compat.json`
   的 `assetsVersion` → `python scripts/release.py business-data --remote-base
   https://github.com/MikumikuDAIFans/next-trainer-agent-assets/releases/download/assets-<assetsVersion>`
   → 按 `dist-release/assets-<assetsVersion>/publish-command.txt` 发布
   `assets-<assetsVersion>` tag（zip + 签名 assets-index.json）。
   **内容更新不需要发插件新版本**——装机客户端经托管通道拉取。

内容规范：每篇知识 md 头部必须有 `Version` / `Scope` / `Evidence status`
三件套；模板 toml 必须能通过宿主 `training_config_validate`（页面 trainType
匹配），不得含机器特定路径。

## 发布与更新（F2 已落地）

**插件包通道（低频，随功能）**：

```
python scripts/release.py check                       # 版本七点一致 + 同步零漂移
python scripts/release.py assets --build --remote-base \
  https://github.com/MikumikuDAIFans/next-trainer-agent-assets/releases/download/v<ver>
# dist-release/v<ver>/{catalog.json,trust.json,…} + 双平台 zip →
# gh release create v<ver> <zip×2> catalog.json trust.json   （draft→upload --clobber→publish 更稳）
```

- 宿主端配置目录源：env `MIKAZUKI_MARKETPLACE_CATALOG_URL` 指向 release 的
  catalog.json（信任根 `trust.json` 随便携包/前次安装分发）。每轮刷新**先验签
  后落缓存**；断网自动回退捆绑目录（live 优先 + 文件兜底）。
- 升级 = 市场再安装：side-by-side 不可变版本 + 原子切活跃 + 激活失败自动回滚；
  手动 `rollback` 可回上一版本；数据根用户文件跨版本保留。
- **不可变纪律**：已发布 release 资产永不覆盖、永不重打；改错就发新 tag/新版本。

**业务数据通道（高频，内容）**：`trainer-assets-<assetsVersion>.zip`（内嵌
MANIFEST 逐文件 sha256）+ 签名 `assets-index.json`（与 catalog 同键库同签名
机制）。宿主 `POST /api/plugins/<id>/assets/update`（或市场对 Agent 暴露的
`assets_update` 工具，需 `content-update` 授权与用户确认票）拉取并应用：

- 只写托管命名空间：`knowledge/`、`templates/` → 数据根；`skills/` →
  `<dataRoot>/pi-agent/skills`（pi SDK 用户作用域自动发现目录，F3-0 决定：
  **唯一技能源**，pi-package 禁止再声明 `pi.skills`，有测试钉死）。
- **用户文件主权**：托管文件被本地改过 → 先备份到
  `<dataRoot>/managed/local-backups/<ts>/` 再更新（报告列出）；用户自建文件
  （不在任何 manifest）**永不触碰**；上游删除且本地干净才删。
- 首发更新会把首装播种文件"采纳登记"入托管清单（相同=unchanged，改过=备份后
  更新），此后修订**直接改原文件即可**——旧的"修订必须换新文件名"规则作废
  （只适用于从未走通道的老装机）。
- 失败语义：索引验签失败/zip 校验不符/半途错误 → 全量回退，托管树与 manifest
  完好；断网/未配置 = 状态报告，**任何情况不阻塞训练主功能**。
- 关闭开关：`NEXT_TRAINER_ASSETS_AUTO_UPDATE=0` 关闭一切非显式触发的网络检查
  （显式的市场按钮/工具调用不受影响）；镜像 `NEXT_TRAINER_ASSETS_MIRROR`、
  索引 `NEXT_TRAINER_ASSETS_INDEX_URL`（内网/离线环境指向内网镜像）。
- 签名现状：dev HMAC 键（反篡改，非信任边界）；生产密钥经
  `--signing-key-id/--signing-key-hex`（或 `MIKAZUKI_RELEASE_SIGNING_*` env）
  注入轮换，密钥不进仓库，对应 trust.json 随 release 分发。

**主项目市场页**：打开市场即"刷新目录"（live → 兜底阶梯）；安装/更新/回滚按钮
走宿主 marketplace API；`assets.status` 报告内容通道状态（configured/版本/
文件数/备份数）。

## 维护模型速览

- 日常开发：本仓库工作树（dev-pi-web.py loop A），无需主项目。
- 集成验证：build zip → 放主项目 marketplace `packages/` 目录（local-first 命中，零网络）。
- 契约变更：兼容先行（宿主先兼容新旧），`compat.json` 版本门，禁止假设跨仓原子提交。
- catalog 的 `permissions_summary` 由打包 zip 内 `plugin.json` **推导**（无第二份
  手工清单可漂移）；新增权限要同时动打包 manifest 的 `permissions`。

## 硬规则

- **用户文件主权**：一切更新链路（插件升级播种/内容通道）对数据根用户文件只
  备份不静默覆盖；播种只补缺失。
- `project/plugin-packages/next-trainer-pi-agent/` 内禁止手工编辑；改动一律回到
  本仓库再 sync。漂移检测：`scripts/sync-to-project.py --check`。
- 已发布 release 资产不可变；版本 bump 覆盖全部七点（launcher / pi-package /
  plugin.json / build-pi-web / build-marketplace-catalog / build-all-platforms /
  compat.json），`release.py check` 把关其六，第七点在 review 中拉齐过。
- 本仓库远程 `github.com/MikumikuDAIFans/next-trainer-agent-assets`（public，
  2026-08-29 用户裁定解禁推送 + release）；**推送/发布前敏感扫描是硬门**。
  git 推送需仓库本地代理（系统 127.0.0.1:11807；`git config http.proxy`）。
- 主项目备份施工区（`project/`）仍只允许本地 commit，严禁 push / PR / release
  （见根目录 AGENTS.md）。
- 技能正文引用的工具名/宿主能力变化时，同步更新 `compat.json`。

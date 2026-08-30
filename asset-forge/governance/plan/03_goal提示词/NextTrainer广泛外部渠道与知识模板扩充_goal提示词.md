# Next Trainer 广泛外部渠道与知识模板扩充 Goal

在 `E:\OpenSourceTeamWork\AgentAssets` 内执行 Stage 7：扩展公开外部渠道目录，按可重放流程进行多轮有界采集，生成候选知识、可验证模板、评测与迁移预览；正式 `project` 与 `agent-assets` 保持只读，最终只到 `awaiting-user-approval`。

## 必读

1. `AgentAssets/README.md`
2. `AgentAssets/00_计划体系/README.md`
3. `AgentAssets/00_计划体系/plan-manifest.md`
4. `AgentAssets/00_计划体系/00_总控目标索引.md`
5. `AgentAssets/00_计划体系/00_预检证据/*governance*.md`
6. `AgentAssets/00_计划体系/00_预检证据/change-record-009-broad-channel-expansion.md`
7. `AgentAssets/00_计划体系/02_长程任务书/阶段7_广泛外部渠道与知识模板扩充_目标8_长程任务书.md`
8. `AgentAssets/02_来源与证据/external-collection-playbook.md`

## 顺序与硬约束

先完成 Stage 7 开工清单，再执行 catalog → bounded harvest → source registry → knowledge synthesis → template probing → eval/gate。每阶段失败或 P0/P1 未闭环不得继续。不得下载图片/权重/数据集，不得保存 token/Cookie/正文，不得迁移、同步、commit、push、PR、build、package、release。

## 完成标准

所有新增知识具备版本、范围、证据层级、来源、边界、别名和 eval；所有根模板具备显式 `model_train_type`，TOML parse、真实宿主 validator `ok`、negative control 非 `ok`、normalized diff 证据；失败与 unknown 透明；manifest/hash/Zero-Short 通过；正式仓库零写入；状态为 `awaiting-user-approval`。


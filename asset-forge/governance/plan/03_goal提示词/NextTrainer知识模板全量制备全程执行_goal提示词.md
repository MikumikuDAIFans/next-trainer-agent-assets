# Next Trainer 知识模板全量制备全程执行 /goal 提示词

```text
/goal 执行 E:\OpenSourceTeamWork\AgentAssets\00_计划体系 中定义的“Next Trainer 知识库与模板库全量制备”全程任务。

本次任务目标：

在 E:\OpenSourceTeamWork\AgentAssets 内完成当前 Next Trainer 训练支持矩阵、来源与 Civitai 元数据证据、候选知识库、候选模板库、评测与迁移预览；正式资产仓库保持未修改，最终等待用户批准迁移。

你必须先读取并遵守：

1. E:\OpenSourceTeamWork\AgentAssets\README.md
2. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\README.md
3. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\plan-manifest.md
4. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_总控目标索引.md
5. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_预检证据\preflight-source-review.md
6. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_预检证据\gate-validation-checklist.md
7. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_预检证据\testing-and-evidence-governance.md
8. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_预检证据\risk-and-authorization-governance.md
9. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\00_预检证据\change-control-governance.md
10. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\05_最小可行性验证\minimal-feasibility-probe-plan.md
11. E:\OpenSourceTeamWork\AgentAssets\00_计划体系\05_最小可行性验证\feasibility-probe-report.md

执行顺序：

1. Stage 0：02_长程任务书\阶段0_训练器能力盘点_目标1_长程任务书.md
2. Stage 1：02_长程任务书\阶段1_来源与Civitai证据采集_目标2_长程任务书.md
3. Stage 2：02_长程任务书\阶段2_知识库候选编制_目标3_长程任务书.md
4. Stage 3：02_长程任务书\阶段3_模板库候选编制_目标4_长程任务书.md
5. Stage 4：02_长程任务书\阶段4_评测审查与迁移包_目标5_长程任务书.md

每阶段开工前必须读取 04_阶段开工清单 下对应清单。上一阶段完成门未通过时，不得开始下一阶段。

硬性约束：

1. 所有新制品只能写入 E:\OpenSourceTeamWork\AgentAssets。
2. E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project 和其 agent-assets 在本任务中只读。
3. 未经用户新的明确授权，不得迁移、同步、commit、push、PR、build、package 或 release。
4. 训练支持以 route/schema/trainer/preset/validator 交叉证据裁定，不以 README 或底层脚本存在单独裁定。
5. 角色、画风、特征、slider 等训练方向必须与模型、训练粒度和网络算法分开建模。
6. Civitai 仅为 L2 观察证据；下载量/评分不是有效性证据；unknown 不得填默认值。
7. Civitai 请求遵守 testing-and-evidence-governance 的代理、请求、时长、磁盘和下载限制；不得保存图片、权重、token、Cookie 或长篇版权文本。
8. 自由文本训练参数抽取必须保留原记录、解析规则、置信度、缺失率和人工抽样结果。
9. 每篇候选知识必须有 Version/Scope/Evidence status、来源、边界、别名和 eval。
10. 每份候选模板必须有显式 model_train_type、证据卡、TOML parse、真实宿主 validator 和 normalized diff；skip 不等于 pass。
11. P0/P1 未修复且未授权延期前不得进入下一阶段。
12. 每个 Phase 完成后更新唯一主进度文件、对应任务书台账、manifest 和 gate。
13. 任何目标、范围、采样量、证据等级、validator 或迁移边界变化必须进入 change control。
14. 不得清理或回退主项目现有的 plugin marketplace 并发改动；将其视为用户/其他任务所有。

每阶段结束必须生成：

1. stage completion gate；
2. evidence cleanup report；
3. 必要的 failure reports；
4. 测试/评测、覆盖、diff、来源、manifest/hash 等证据；
5. manifest、任务书和总控进度更新。

建议证据根目录：

E:\OpenSourceTeamWork\AgentAssets\06_评测与校验\evidence

最终完成标准：

1. 总控完成口径全部有证据。
2. G1..G5 与 Stage 0..4 完成门通过。
3. 所有候选知识/模板有来源、评测和结构验证；模板零 reject/skip。
4. Civitai 样本量、缺失率、偏差与自由文本抽取置信度透明。
5. migration manifest、hash、目标映射、compat/eval 计数草案和播种文件名策略齐全。
6. 正式 project/agent-assets 未因本任务发生写入。
7. 最终状态只能是 awaiting-user-approval 或 not-ready；绝不自动迁移。

优先复用已有依赖和项目 validator，避免重复下载。遇到真实阻塞时停止相关动作并保留 failure report，不得通过削弱验收继续。
```


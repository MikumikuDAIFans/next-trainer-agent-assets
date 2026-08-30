# Next Trainer 多轮外部渠道全量采集 /goal 提示词

```text
/goal 在 E:\OpenSourceTeamWork\AgentAssets 内执行“Next Trainer 多轮外部渠道全量采集与增量资产制备”（G7）。

先读取：AgentAssets README、00_计划体系 README/manifest/总控、00_预检证据全部治理文件、05 最小可行性验证、Stage 0..5 任务书与清单、CR-008、Stage 6 任务书与清单。

执行 Round 1→4：
1. 读取 external-channel-catalog.json，运行 tools/external_channel_harvest.py；每轮记录 offset、请求数、0.5 秒间隔、超时、响应大小、成功/失败和失败报告。
2. 只保留公开 URL、短事实摘要、revision/hash/status、来源 ID 和提取规则；不保存图片、权重、token、Cookie、长版权文本或不受控缓存。
3. 将外部内容分为 L1 官方/项目、L2 公开观察、L3 实验建议；外部工具配置不能直接当 Next Trainer 模板。
4. 每篇知识候选必须有 Version/Scope/Evidence status、来源、边界、别名和 eval；每份模板必须显式 model_train_type、证据卡、TOML parse、真实宿主 validator、normalized diff 和 negative control。
5. 只有当前 route/schema/trainer/preset/validator 共同证明的模板才进入候选根目录；reject/skip/negative-control leak 全部移入 research-rejected 并保留 failure report。
6. 多轮结束后重建 knowledge manifest/coverage/eval、模板 coverage、迁移 manifest/preview；运行 Stage 2 lint、Stage 3 validator、Stage 4 eval review、Zero-Short。
7. 不修改 project 或正式 agent-assets，不迁移、同步、commit、push、PR、build、package、release；最终状态只能是 awaiting-user-approval 或 not-ready。
8. 任意范围、来源、采样量、证据等级或 validator 变化必须新增 change record；P0/P1 未修复不得进入下一轮。
```

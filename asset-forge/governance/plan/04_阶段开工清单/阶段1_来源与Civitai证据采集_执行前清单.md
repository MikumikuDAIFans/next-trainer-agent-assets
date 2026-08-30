# 阶段1执行前清单：来源与 Civitai 证据采集

- Stage ID: `S1`
- Required task book: `..\02_长程任务书\阶段1_来源与Civitai证据采集_目标2_长程任务书.md`
- Checklist version: `v2`
- Execution state: `ready-to-start`（仅限 `E:\OpenSourceTeamWork\AgentAssets` 暂存制备；正式迁移仍需用户明确批准）

## 硬门槛

- [x] 已读取 workspace/计划 README、manifest、总控、G2 和 Stage 1 任务书。
- [x] Stage 0 完成门为无 P0/P1 的 `pass-with-boundary`。
- [x] G1 支持矩阵已冻结并成为采样分层输入（17 entries，0 errors）。
- [x] 已读取网络/证据/版权/授权规则。
- [x] Civitai MVP probe 已 pass，GATE-11 保持 `pass-with-boundary`：代理请求 882225 返回 200，训练结构化字段为空。
- [x] 已建立 `02_来源与证据`、`03_Civitai样本/raw`、`normalized`、`reports` 和 `06_评测与校验/evidence/stage-1` 目录。
- [x] 已设置单批≤100 请求、每请求≥0.5 秒间隔、退避重试≤3、raw 软上限 500 MB。
- [x] 已确认不使用 token/Cookie，不下载图片；默认不下载完整权重。若确需权重头分析，单文件≤2 MB、总计≤50 MB，且显式登记。
- [x] 所有下载、缓存、解压、临时、日志和分析路径均限定在 `AgentAssets`；不可重定向的外部缓存将阻断流程。
- [x] 已确认失败/限流/字段缺失都会保留，不会用默认值填充 `unknown`。
- [x] 已确认只读 Git 检查不产生写操作；源仓未提交修改仅记录，不回退、不清理。

## 本阶段禁止事项

1. 绕过 Civitai 访问限制、登录或限流。
2. 把热度、评分或下载量当作训练参数有效性的证据。
3. 复制长篇模型卡文本、下载预览图或权重。
4. 将任何候选内容写入正式知识库、模板库、主项目或 vendored 快照。
5. 执行 commit、push、merge、rebase、tag、PR、同步或发布。

## 不满足时处理

停止网络采集并生成 failure report；需要扩大请求/下载/凭据范围时必须先走 change control 和用户授权。当前复核结果为 `ready-to-start`，下一动作是执行 Phase 1 官方来源登记。

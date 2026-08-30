# Stage 1 Readiness

- Status: `ready-to-start`
- Gate result: `pass-with-boundary`
- Current phase: `Phase 1 官方与项目来源登记`
- Next action: 在 `AgentAssets` 内登记官方来源并建立 source coverage。

## Ready Conditions

- Stage 0 支持矩阵已冻结并通过校验（17 条、0 errors）。
- 任务书与执行清单已更新到 v2，明确下载仅用于分析、AgentAssets 路径白名单、有界并发、429/5xx/连接失败退避、字段缺失保留和 Git/迁移禁令。
- 本地代理 `127.0.0.1:11809` 可访问 Civitai 官方 API；MVP 版本 `882225` 返回 HTTP 200。
- 有界并发能力已验证；正式采集仍受每批 100 请求、0.5 秒间隔、最多 3 次重试和 500 MB raw 软上限约束。
- 源仓库状态已记录：`project` 存在用户未提交修改，`agent-assets` clean；不回退、不清理、不覆盖。

## Hold Points

- 不使用 Token、Cookie、私人 API，不绕过访问限制。
- 默认不下载图片或完整权重；若确需权重头分析，必须先登记理由、URL、哈希、大小和清理证据，并将所有中间物置于 AgentAssets。
- 不把 Civitai 热度指标或 description 自由文本当作高置信技术参数。
- 不向正式知识库、模板库、主项目或 vendored 快照写入；最终项目状态保持 `awaiting-user-approval`。

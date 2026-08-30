# Stage 7 外部采集轮次报告

- Date: `2026-08-30`
- Scope: Hugging Face 模型卡/API、官方 examples/config、caption/dataset/eval 工具、PyTorch 运行时文档与论文元数据。
- Requests: `39`
- HTTP 200: `39`
- Failures: `0`
- Budget: 每轮 ≤20 请求；本轮拆为 `051-070`（20）与 `071-089`（19），请求间隔 0.5 秒，响应上限 128 KiB。

## Sources and boundaries

- 新增目录条目：`27`；目录总量 `58` 渠道、`90` 可重放请求索引。
- GitHub commit API 记录为公开响应 hash；未将响应 hash 冒充 commit ID。
- 13 个页面响应达到大小上限，状态保留为 `size-limit`；不从截断正文推断字段。
- 未保存页面正文、图片、权重、数据集、token、Cookie 或长版权文本。

## Evidence interpretation

- L1：官方文档、仓库与论文元数据，用于概念/边界和流程建议。
- L2：Hugging Face 公共模型 API，用于来源、字段缺失和 revision 观察。
- 产品兼容性仍由当前 Next Trainer route/schema/trainer/preset/validator 决定。

## Reproduction

```text
python -B tools/external_channel_harvest.py E:/OpenSourceTeamWork/AgentAssets --start 51 --limit 20
python -B tools/external_channel_harvest.py E:/OpenSourceTeamWork/AgentAssets --start 71 --limit 19
```


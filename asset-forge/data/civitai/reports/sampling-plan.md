# Civitai 分层采样计划

本次 MVP 以 LORA 类型按 SD 1.5、SD 2.1、SDXL 1.0、Flux.1 D、Anima、Krea 2、Lumina 2 分层，每层最多 5 个最新公开模型记录。请求经 `127.0.0.1:11809`，有界并发 2，提交间隔至少 0.5 秒，最多退避重试 3 次。

model-level 与 version-level 分开统计；本批为 exploratory，任何分层未达到 8 个独立 model-level 样本，不支撑模板参数分布。description 解析字段仅为低置信观察，结构化 `trainingDetails` 缺失原样保留。热门度字段仅用于发现，不作为技术正确性证据。

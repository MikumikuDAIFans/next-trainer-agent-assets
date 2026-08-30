# img2dataset/WebDataset 数据集摄取与来源链

- Version: `2026-08-30`
- Scope: 比较 img2dataset 与 WebDataset 的摄取/分片实践，补充训练数据来源、去重和可复现记录。
- Evidence status: L1 official repositories; 页面与 commit API HTTP 200。
- Aliases / 检索关键词: img2dataset, WebDataset, 数据摄取, shard, provenance, 去重

## 记录字段

每个数据批次记录来源 URL 或本地清单 ID、抓取日期、许可核对状态、过滤规则、重复检测方法、分片顺序和样本计数。训练器只接收 `X:/dataset` 这类用户路径占位，来源链留在证据文档。

## 可复用检查

先做 URL/文件级去重，再做近重复图像抽样；分片顺序和随机种子必须写入复现实验记录。数据规模变化时重新计算 exposure budget，不沿用旧步数。

## Sources

- img2dataset: https://github.com/rom1504/img2dataset (L1 official)
- WebDataset: https://github.com/webdataset/webdataset (L1 official)
- 数据准备基线: `../datasets/preparation-checklist.md` (L1/L3)

## Boundaries

- 不在本流程中抓取外部图片或数据集；只记录公开来源和短元数据。
- 分片工具字段不能直接变成 Next Trainer schema 字段。

## Eval

- Question: “改变分片顺序后能否复用原 exposure budget？”
- Expected answer: 不能，数据计数与顺序变化需重新记录和评估。


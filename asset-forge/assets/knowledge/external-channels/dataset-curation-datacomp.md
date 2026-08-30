# DataComp 数据筛选研究的可迁移边界

- Version: `2026-08-30`
- Scope: 以 DataComp 论文为数据筛选研究背景，补充过滤器、配比和偏差记录方法。
- Evidence status: L1 paper metadata (arXiv:2304.14108 HTTP 200); 仅作方法边界，不声称复现其结果。
- Aliases / 检索关键词: DataComp, dataset curation, 数据筛选, 过滤器, 偏差

## 可复用记录

记录过滤器版本、阈值、保留率、类别配比、近重复规则和抽样审查结果。任何过滤规则变化都触发数据计数、caption 统计和 exposure budget 重算。

## 与产品的关系

数据筛选属于数据/目标设计，与模型、训练粒度、网络算法正交。它可以解释训练差异，但不能把研究中的阈值直接写入 Next Trainer preset。

## Sources

- DataComp paper: https://arxiv.org/abs/2304.14108 (L1 official)
- 数据集准备基线: `../datasets/preparation-checklist.md` (L1/L3)

## Boundaries

- 论文元数据不能替代真实数据审查或训练验证。
- 不保存数据集图片、版权长文本或外部下载缓存。

## Eval

- Question: “DataComp 的过滤阈值能否直接作为本地数据集默认值？”
- Expected answer: 不能，必须在本地数据和许可边界内重新验证。


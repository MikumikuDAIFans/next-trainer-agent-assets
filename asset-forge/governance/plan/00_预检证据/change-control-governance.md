# 变更控制治理

## 触发条件

以下任一情况必须新增变更记录：

1. 用户改变最终目标、模型范围、模板粒度或迁移目标。
2. 源码盘点发现 README 之外的新模式，或推翻现有支持声明。
3. Civitai API 不可用、字段不足，需改用 safetensors 头、其他数据源或更高请求量。
4. 需要下载大文件、使用 token、GPU 训练、修改正式仓库或执行迁移。
5. 覆盖标准、评测阈值、证据等级或 validator 规则变化。
6. 阶段合并、删除、重命名或 Next action 改变。

## Change Record

```md
# Change Record

- Change ID:
- Date:
- Requested by:
- Affected plan/stage/goal:
- Trigger:
- Previous state:
- New state:
- Reason and evidence:
- Preserved evidence:
- Invalidated evidence:
- Affected gates:
- Risk delta: P0 | P1 | P2 | P3
- User authorization:
- Next action:
```

## 规则

1. 不静默改写 verified facts、完成历史、支持矩阵或模板证据。
2. 保留仍有效阶段和证据；失效证据标记 invalidated，不删除历史。
3. 阶段重命名时保留旧名别名并更新 manifest、总控、任务书、清单和 goal。
4. 任何迁移授权必须附在变更记录并限定文件批次，不得推定未来批次也获授权。
5. 变更后重新运行受影响 gate、覆盖检查和最终复盘。


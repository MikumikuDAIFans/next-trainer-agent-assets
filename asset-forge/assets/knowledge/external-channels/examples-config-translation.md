# 官方 examples/config 到 Next Trainer 的安全翻译

- Version: `2026-08-30`
- Scope: 比较 Diffusers、sd-scripts、Musubi 和 AI-Toolkit 的官方 examples/config，建立字段翻译审查步骤。
- Evidence status: L1 official repositories/docs；4 个 examples/config 渠道及其公开 commit API 于 2026-08-30 返回 HTTP 200。
- Aliases / 检索关键词: examples, config translation, 配置翻译, schema 对照, cross-tool

## 翻译步骤

先锁定外部仓库 revision，再建立“外部字段 → Next Trainer schema → validator 结果”三列记录。只有字段语义、单位和生命周期均一致才允许进入知识说明；外部 YAML/TOML 本身不得复制为模板。

## 证据分层

官方 examples 是方法语义的 L1 来源；Next Trainer 页面 schema/preset/validator 才是产品合同 L1。两者冲突时保留冲突，不能用外部默认值覆盖产品 unknown。

## Sources

- Diffusers advanced examples: https://github.com/huggingface/diffusers/tree/main/examples/advanced_diffusion_training (L1)
- Diffusers DreamBooth examples: https://github.com/huggingface/diffusers/tree/main/examples/dreambooth (L1)
- sd-scripts training options: https://github.com/kohya-ss/sd-scripts/blob/master/docs/train_network_README-ja.md (L1)
- Musubi docs: https://github.com/kohya-ss/musubi-tuner/tree/main/docs (L1)

## Boundaries

- 外部配置不是可导入合同；路径、优化器默认和训练步数不得盲抄。
- 只能以真实页面 validator `ok`、negative control 非 `ok` 的结果证明模板。

## Eval

- Question: “复制 Diffusers example 的字段到 Next Trainer TOML 是否足够？”
- Expected answer: 不足够，必须逐字段映射并通过宿主 validator。


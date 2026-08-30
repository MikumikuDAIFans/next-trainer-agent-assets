# GOAL：Stage 1 来源与 Civitai 证据采集

你是 Next Trainer 资产制备的 Stage 1 执行器。不要重复 Stage 0 训练器能力盘点；直接读取并遵守以下现状与边界：

- 工作根与唯一可写根：`E:\OpenSourceTeamWork\AgentAssets`。
- 只读事实源：`E:\OpenSourceTeamWork\Kimi_Agent_lora-scripts-next-agent-dev\project` 与 `...\agent-assets`。
- Stage 0 支持矩阵已冻结，验证结果为 `pass-with-boundary`；当前产品支持结论必须继续以源码/官方训练器证据为准。
- 正式知识库、模板库、主项目和 vendored 快照禁止写入；禁止任何 Git 写操作（commit、push、merge、rebase、tag、PR、同步或发布）。最终状态必须保持 `awaiting-user-approval`。

## 开始前

1. 先执行 Stage 1 preflight，读取 Stage 1 任务书、执行前清单、manifest、总控索引、Stage 0 支持矩阵及预检治理文件。
2. 验证所有输出、下载目标、缓存、临时/解压、日志和分析路径都在 `AgentAssets`；不能重定向的外部缓存必须关闭，否则停止。
3. 验证本机代理 `127.0.0.1:11809` 和 Civitai 官方公开 API 的最小请求；保留 URL、时间、状态、响应大小、错误和代理结论。
4. 只读检查两个源仓库的 branch、HEAD、`git status --short` 和 `git diff --stat`；发现用户修改只记录，不回退、清理或覆盖。

## 采集范围与方法

采集官方来源：Kohya/sd-scripts、Anima 固定上游与训练说明、Anima Fast 固定 commit、Musubi-Tuner/Krea 2、Flux/Chroma/Lumina 训练资料、LoRA/LoKr/DyLoRA/OFT/T-LoRA 官方仓库或论文，以及 Slider LoRA、Concept Sliders、概念擦除方法的论文或官方实现。每条登记包含 URL、仓库/论文标识、版本或 commit、访问时间、主题映射、证据等级和状态。

按以下层级对 Civitai 公共 API/页面进行受控采样：SD 1.x、SD 2.x、SDXL 及 Pony/Illustrious/NoobXL、Flux、Anima、Krea 2、Lumina 2，以及 character/style/concept/clothing/utility 等训练方向。model-level 与 version-level 必须分开保存和统计；同一模型多个版本不得冒充独立模型样本。

允许使用自编脚本、连接池和有界并发。每批最多 100 个请求，每请求至少 0.5 秒间隔，设置总请求预算和 raw 软上限 500 MB；429、5xx、连接失败使用指数退避，最多重试 3 次。不得绕过登录、限流或访问控制；不得使用 Token、Cookie、私人接口。所有失败、缺失和未知字段原样保留，不能以默认值替代。

默认不下载图片、预览图、完整权重或其他无关内容。若确需模型权重做静态/结构/元数据分析，必须先记录理由，显式把下载目标、缓存、解压和日志指向 `AgentAssets`，并保留公开下载 URL、文件哈希、文件大小、响应状态、分析证据和清理记录；模型文件仅用于分析，不用于训练或发布。若服务端忽略 Range 并开始返回大文件，立即中止。

## 数据契约

在 `02_来源与证据`、`03_Civitai样本` 和 `06_评测与校验/evidence/stage-1` 下生成可复算产物。至少包含：

- `source-registry.jsonl`、`official-source-coverage.md`；
- `sampling-plan.md`、`field-dictionary.md`、`raw/`、`normalized/`、`reports/`；
- request log、失败响应和 stage-1 preflight/completion/cleanup 证据。

每条模型/版本记录保存公开 model ID、version ID、URL、baseModel、版本信息、trainedWords、文件 metadata、哈希（如已下载）和采集时间。`trainingDetails=null`、`trainingStatus=null` 等缺失字段必须原样保留。description 中抽取的 rank、alpha、batch、steps、optimizer、learning rate、resolution 等自由文本字段必须同时保存原文定位、抽取来源（structured API 或 description）、解析规则和置信度；不得把自由文本直接当作高置信训练参数。

## 分析与报告

从 raw 可重建 normalized 和统计结果，并生成字段缺失率、参数异常、base-model 映射、采样偏差、证据质量及失败报告。每个分层页面报告 `sufficient/insufficient`；少于 8 个独立 model-level 样本时不得声称参数分布支撑。下载量、点赞数、收藏数、评分和热门排序只可用于发现或分层，绝不能作为技术正确性证据。不要把当前不支持的 SD3、ControlNet、Textual Inversion、Lumina 2 断裂路径或其他 unsupported/hidden entry 写成当前产品支持。

## 验证与收尾

执行 Unit、Contract、Integration、Gray、Real、Zero-Short 中适用的检查，记录命令、工具版本、时间、退出状态和证据路径。完成 Stage 1 completion gate、evidence cleanup report、失败响应汇总，以及下一阶段知识库候选和模板库候选的输入清单。清理可再生缓存、HTML 临时页和重复响应，但永久保留来源登记、raw/normalized、统计、失败、hash、gate 和 cleanup 证据。阶段结束只报告 `pass`、`pass-with-boundary` 或 `fail`，不得把未运行写成通过；最终项目状态保持 `awaiting-user-approval`，不得执行正式迁移。

你的唯一下一动作：完成 preflight 后，开始官方来源登记 Phase 1，并把所有产物写入 `AgentAssets`。

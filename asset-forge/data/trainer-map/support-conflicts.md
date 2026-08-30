# 训练支持冲突与陷阱登记

- Source commit: `9cd23996d1bd830b4a4fc0187e063e8a2ab2860a`
- Rule: 冲突未解决前降级支持等级；不得为冲突页面生成正式候选模板。

## C-001：Lumina schema train type 与前端强制值不一致

- Severity: P1
- Evidence:
  - `mikazuki/schema/lumina2-lora.ts:4` 默认 `lumina-lora`；
  - `frontend/src/training/params.ts:43` 强制 `lumina2-lora`；
  - `mikazuki/utils/config_import.py:16,167-171` 只接受 `lumina-lora`。
- Impact: 工作台提交的 train type 不被 validator/backend 识别。
- Decision: Lumina 2 当前标 `unsupported`，不生成候选模板。

## C-002：Lumina 无 `/api/run` backend mapping

- Severity: P1
- Evidence: `mikazuki/app/api.py:152-164` 无 lumina；`741-838` 仅有 Anima Fast/Krea 特殊分支；`845-849` 对未知 type 明确拒绝。
- Impact: 即使修正前端强制值，`lumina-lora` 仍会被运行 API 拒绝。
- Decision: 必须由产品代码另行修复并补测试后才能宣称支持。

## C-003：Lumina import redirect 指向未注册 legacy URL

- Severity: P2
- Evidence: `config_import.py:167-171` 指向 `/lora/lumina.html`；`frontend/src/router.ts` 没有该 redirect。
- Impact: Lumina 配置重定向可能落入 404；统一 `/training` query 本身仍可选择 module。
- Decision: 记录为产品缺口；本任务不修代码。

## C-004：README 支持表与工作台 module 不一致

- Severity: P2
- Evidence: README 未列 Lumina；`modules.ts:3,25,42` 注册 Lumina。
- Impact: 公开文档不暴露一个实际已注册但不可运行的 module。
- Decision: 知识库以端到端矩阵为准，不把 README 或 module 单独当权威。

## C-005：Anima LoRA-FA/VeRA schema 分支退化为普通 LoRA

- Severity: P1
- Evidence:
  - `sd3-lora.ts:110-125` 将 LoRA-FA/VeRA 都映射到 `networks.lora_anima`；
  - `adapter.test.ts:184-197` 固化该映射；
  - `anima_backend/adapter.py:392-400` 把 `lora_type` 当 UI-only 丢弃；
  - 固定 upstream 中没有 VeRA 实现命中，LoRA-FA 模块未被选择。
- Impact: 用户选择这些 type 后无法证明得到不同 adapter。
- Decision: 不计入 Anima 可验证算法支持；不出模板。

## C-006：Anima PiSSA/LoHa 仅有 UI 暴露，后端证明不足

- Severity: P1
- Evidence: schema 有 PiSSA 字段和 `networks.loha`；固定 `vendor/sd-scripts` 无 PiSSA 参数实现命中，项目无 Anima LoHa 专属测试。
- Impact: 可能未知参数/零模块/不兼容，而非可靠训练能力。
- Decision: 标 `schema-declared-unverified`；Stage 1 可查官方 upstream，但当前不计支持。

## C-007：`sd3-lora` 名称不代表 Stability AI SD3

- Severity: P2
- Evidence: `TRAIN_TYPE_ALIASES` 将 `sd3-lora` 归一到 `anima-lora`；backend mapping 也指向 `anima_train_network.py`；旧 URL `/lora/sd3.html` 重定向 Anima。
- Impact: 文档或模板若按字面理解会用错底模。
- Decision: 所有候选知识必须明确它是历史 alias；实际 SD3 当前 unsupported。

## C-008：Flux full finetune 后端存在但工作台显式不支持

- Severity: P2
- Evidence: `api.py:163` 有 `flux-finetune`；`modules.test.ts:64-66` 断言 Flux finetune selection 为 undefined。
- Impact: 手工 API 可能能启动，但不是受支持用户流程，无 schema/validator 模板闭环。
- Decision: `backend-capable-ui-hidden`；不出正式候选模板。

## C-009：Schema API 会加载“存在的文件”，不能证明训练支持

- Severity: P2
- Evidence: `api.py:221-238` 遍历 schema 目录全部文件；其中含 shared、tagger、lora-basic。
- Impact: `/schemas/all` 出现某名称不等于工作台+backend 支持。
- Decision: 支持判定必须使用完整链路。

## C-010：`lora-basic` 是 legacy hidden，不是当前独立工作台目标

- Severity: P3
- Evidence: schema 和 serializer basic defaults 存在；`modules.test.ts:36-42,103` 明确排除 current module。
- Decision: 知识中可解释兼容来源，但模板应指向当前 `sd-lora` 页面而非 legacy schema。

## C-011：`validate_model` 对多数 train type 的模型族匹配较宽松

- Severity: P2
- Evidence: `train_utils.py:285-315` 除 SDXL→sd-lora 特例外，接受多个 model type。
- Impact: 通过该函数不能单独证明模型与页面匹配。
- Decision: 模型选择仍以 page contract + official architecture + validator 为准。

## C-012：平铺数据目录校验可能移动用户文件

- Severity: P1（知识安全）
- Evidence: `train_utils.py:326-365` 在没有合法重复子目录时创建 `<repeat>_zkz` 并移动图片/caption。
- Impact: “校验/提交训练”可能改变原数据目录结构。
- Decision: 数据集知识必须提前告知并建议备份/规范子目录；本研究不调用该路径。

## C-013：现有 preset 的“官方推荐”措辞需外部复核

- Severity: P2
- Evidence: `config/presets/krea2-lora.toml` 自称官方推荐；当前阶段只有项目内声明。
- Decision: Stage 1 查 Krea 2/Musubi 官方来源；未找到前只能标项目 preset，而不能写官方事实。

## C-014：Flux schema 默认 rank/alpha 不应直接当经验模板

- Severity: P2
- Evidence: `flux-lora.ts:54-55` 默认 dim=2、alpha=16；这是 schema default，不是训练效果证明。
- Decision: Stage 3 模板需结合项目 preset、官方资料和可用样本；不盲复制 schema default。

## C-015：过度精简的 Anima Fast 配置会被 validator 误判为标准 Anima

- Severity: P2
- Evidence: 对 `{model_train_type=anima-lora-fast, network_module=networks.lora_anima}` 的纯函数校验返回 `redirect` 到 `/lora/sd3.html`；现有完整 Fast 模板含 `static_token_count`、`compile_mode` 等 marker 时返回 `ok`。
- Impact: 只保留通用 LoRA 字段的 Fast 模板可能无法通过目标页校验。
- Decision: Fast 候选模板必须保留至少一个明确 Fast marker，并以完整 TOML 运行真实 validator；redirect 不算 pass。

## C-016：sdxl-finetune 配置携带 TE1/TE2 字段时无法通过自身页面导入校验（Stage 3 新发现）

- Severity: P2（配置导入/模板复用路径；UI 原生操作不受影响）
- Evidence: `config_import.py:70-74`（SDXL_CONFIG_MARKERS 含 `learning_rate_te1/te2`）、`analyze_train_type`（marker≥2 分即采推断家族）、`validate_config_import`（`config_type = inferred or explicit` 推断压过显式）；宿主 venv 探测定律见 `06_评测与校验/evidence/stage-3/phase-3/failure-F-S3-001-sdxl-finetune-import-quirk.md`。
- Impact: DreamBooth 页对带 te1/te2 的 sdxl-finetune 配置返回 `redirect`；lora-master 页虽 `ok` 但把类型静默规范化为 `sdxl-lora`（LoRA 化类型漂移，风险更高）。
- Decision: 本阶段不为 sdxl-finetune 出候选模板（草案在 `research-rejected/`，回归断言常驻 stage3 runner）；不改写 UI 契约知识文档；产品修复后由断言红灯触发复验与模板复活。


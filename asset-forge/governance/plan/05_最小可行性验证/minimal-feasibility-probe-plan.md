# Minimal Feasibility Probe Plan

- Date: `2026-08-29`
- Plan: `NT-ASSET-KB-TPL-20260829`
- Result: `pass-with-boundary`

## Critical Assumptions

| ID | Assumption | Risk if false | Existing evidence | Probe needed |
|---|---|---|---|---|
| A1 | 当前训练能力能从 route/schema/trainer/preset/validator 穷举 | P1：支持矩阵不完整 | README 和前端 AGENTS 给出入口 | yes |
| A2 | Civitai 公共接口无需凭据即可返回可追溯 LoRA 模型/版本元数据 | P1：用户建议的数据源不可用 | 仅有公开站点认知，尚未实测 | yes |
| A3 | Civitai 返回的训练字段可能不完整，且可被诚实检测为缺失 | P1：模板可能建立在伪数据上 | 证据治理已规定 unknown/null | yes，与 A2 同请求检查 |
| A4 | 真实项目 validator 可在不写正式仓的情况下验证指定暂存模板目录 | P1：候选模板无法证明可导入 | 已读 `validate-templates.py` 实现 | yes |

## Probe Matrix

| Probe | Command/Method | Resource | Limit | Evidence | Cleanup |
|---|---|---|---|---|---|
| P1 源码入口存在性 | `rg --files` + 定向符号扫描 | 本地只读 project | ≤30 秒、≤5 MB 输出 | `feasibility-probe-report.md` + 命令摘要 | 不产生缓存；临时输出不落源仓 |
| P2 Civitai API | 打开官方 API 文档与 `api/v1/models` 单页 `limit=1` | 公共 HTTPS，无 token | ≤5 请求、≤60 秒、≤5 MB | 响应状态、字段树和公开 URL | 不保存 Cookie/图片；仅保留小型字段摘要 |
| P3 训练字段缺失探针 | 检查 P2 的 model/version/file/trainingDetails/safetensors metadata 字段 | P2 同一响应 | 不追加大下载 | 字段 presence/null 表 | 同 P2 |
| P4 宿主 validator | Python `-B` 调用现有只读模板目录 | 本地 project venv | ≤60 秒、无训练、无网络 | 每模板 result/page/exit code | 不写源仓；若工具产生缓存立即停止并报告 |

## Failure Handling

1. P1 失败：回到总控，把“穷举支持”降级为已知入口清单并阻止 Stage 0 开工。
2. P2/P3 失败：Civitai 仅保留为人工来源，不执行批量采样；重新规划模板证据来源。
3. P4 失败：Stage 3 不得开始，先修正 validator 调用方式或由用户授权替代校验。
4. 任一 probe 触发写正式仓、大文件下载或凭据要求时立即中止。

## Decision

全部 P1 假设已达到 `pass` 或不削弱核心目标的 `pass-with-boundary`；允许生成可开工 goal。边界见 `feasibility-probe-report.md`。

## Next Action

生成全程执行 goal，并进行开工前最终复盘。

# Failure report F-S4-002 — 整合整理事故：模板层 26 文件误删（10 份已字节级恢复，16 份待处置）

- Date: `2026-08-30 21:10 +08:00` · Severity: **P1（自致数据事故；透明度与恢复义务触发）**
- 责任: 本会话整理脚本缺陷——`Get-ChildItem -File -Include ... -Recurse -Depth 0` 管道只产出**最后一个文件**并被 Copy-Item 重命名为目标目录名 `templates`，随后 `Remove-Item -Recurse` 删除了 `05_模板库候选` 源目录。知识层（`Copy-Item 目录→目录`）无恙。

## 时间线

1. 20:3x 物理搬迁执行；`assets\templates` 异常（应为 26 文件，实际为 1 文件）。
2. 恢复搜索：回收站(无)、全盘哈希扫掠、PS 存储、`C:\Users\25454\.dsh\sessions\**\session.jsonl.zstd`（zstd 解压）。
3. **字节级恢复 10/26**：`assets\templates\sd2-lora-conservative.toml`（被"重命名幸存"的原文件，sha=冻结值）+ 本会话 turn=5 的 `tool/call(write)` 原始 payload 重放 9 份（LF 编码，sha 全部 == `governance\migration-preview-20260830\migration-manifest.json` 冻结值）。
4. 16 份缺失（15:24/15:48/17:19 由**另一未知生产通道**写入：不在本会话 turn 历史、不在 728a8238 会话(563 write 调用无一命中)、chunks 无幸存、temp/回收站无残留）：
   - toml：anima-fast-lora-{character,style}、anima-lora-{character,style}-automagic、anima-lora-{lokr,tlora}-conservative、flux-lora-oft-conservative、sd-dylora-conservative
   - evidence 卡 ×8（同前缀 `.evidence.md`）

## 现存恢复依据（非字节级）

- `data\template-index\template-coverage-matrix.csv`（生产通道 17:20 更新）：8 个模板的页面/参数决策/字段差异证据行
- `governance\evidence\stage-3\phase-3\*.json`：每模板 page/result/normalized 断言
- 项目出厂 presets（同名 anima 方向 preset 存在）、network-algos 知识文档（lokr/tlora/oft/dylora 契约）
- 知识层 64 篇、eval 草稿 64、拒绝区 2 对：**全部完好**

## 处置纪律

- 16 份文件不得静默重建充数。恢复路径二选一，由用户定夺：
  A. 用户告知 15:2x 生产通道（哪个会话/工具/机器），从其存储取回原件；
  B. 授权按上述依据重建，全部文件头标注 `reconstructed-2026-08-30（sha≠冻结值）`，重过 stage3 强页 validator。
- 工具纪律固化：本仓库一切批量文件操作用 Python（显式编码+移动前校验目标计数）；禁用 PS 隐式管道语义做删除前置拷贝。

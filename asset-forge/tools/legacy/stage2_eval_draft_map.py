"""Stage 2 Phase 3: generate the knowledge-citation eval draft and freeze mapping.

Outputs:
- 06_评测与校验/eval-candidates/knowledge-citation-draft.jsonl

Each candidate doc gets one citation-seed draft: question -> must cite its own doc,
boundary checks keep answers honest (unknowns stay unknowns). Deterministic ids kc-001.. in
manifest path order. Run:  python -B tools/stage2_eval_draft_map.py <AgentAssetsRoot>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# path -> (question, must_include, boundary_must_not)
QUESTIONS: dict[str, tuple[str, list[str], list[str]]] = {
    "model-families/anima-lora-workflow-guide.md": (
        "Anima 角色 LoRA 应该从哪套出厂参数起步？预览图约定是什么？",
        ["anima-lora-character-automagic", "1024"],
        ["把 1000-3000 步说成保证值"],
    ),
    "model-families/anima-full-finetune-guide.md": (
        "Anima 全量微调有出厂 preset 吗？参数怎么给？",
        ["unknown"],
        ["编造 finetune LR/步数"],
    ),
    "engines/anima-fast-workflow-guide.md": (
        "Anima Fast 为什么 preset 用 AdamW8bit 而不是 Automagic？它的运行环境要求是什么？",
        ["Automagic", "独立"],
        ["承诺 2.5x 实测提速"],
    ),
    "model-families/sd15-lora-workflow-guide.md": (
        "SD1.5 LoRA 页面默认网络维度是多少？有什么页面陷阱？",
        ["sdxl-lora", "32"],
        ["给出实测最优步数表"],
    ),
    "model-families/sd2-lora-conditions.md": (
        "给 SD2.1 v-pred 底模训 LoRA 必须设置哪些字段？",
        ["v2", "v_parameterization"],
        ["说有独立 SD2 工作台"],
    ),
    "model-families/sdxl-lora-workflow-guide.md": (
        "SDXL LoRA 的 starting box 数值出自哪里？能当实测保证吗？",
        ["heuristic", "sdxl-lora-parameter-baseline"],
        ["把 heuristic 升格为推荐值"],
    ),
    "model-families/sdxl-derived-cohorts.md": (
        "Pony/NoobXL 在本产品里是独立训练器吗？LoRA 能跨派系直接混用吗？",
        ["sdxl-lora", "base"],
        ["承诺跨派系兼容"],
    ),
    "model-families/sd-dreambooth-finetune-guide.md": (
        "SD DreamBooth 页面 schema 默认学习率是多少？和 LoRA 页面差几个数量级？",
        ["1e-6", "5e-7"],
        ["把默认值说成实测最优"],
    ),
    "model-families/sdxl-full-finetune-guide.md": (
        "SDXL 全量微调的 TE 学习率字段是什么？full_bf16 适用条件？",
        ["learning_rate_te1", "SDXL"],
        ["说这个页面能出 LoRA"],
    ),
    "model-families/flux-lora-workflow-guide.md": (
        "Flux 页面必须配齐哪四个资产？网络默认 dim/alpha 为什么和 SD 不同？",
        ["t5xxl", "network_dim"],
        ["把默认值说成实测最优组合"],
    ),
    "model-families/chroma-flux-page-variant.md": (
        "Chroma 在本产品里是什么？preset 里哪几个字段必须整体保留？",
        ["model_type", "guidance_scale"],
        ["说有独立 Chroma 页面"],
    ),
    "model-families/krea2-lora-musubi-guide.md": (
        "Krea 2 训练需要哪些资产和运行时？官方推荐措辞能直接引用吗？",
        ["qwen3-vl", "musubi"],
        ["把项目 preset 措辞当外部官方事实"],
    ),
    "model-families/lumina2-known-breakage.md": (
        "现在能用 Lumina2 页面训练吗？错在哪一层？",
        ["unsupported", "backend"],
        ["给出可绕过的工作流"],
    ),
    "model-families/hidden-and-unsupported-boundaries.md": (
        "Flux 全量微调 / SD3 / ControlNet / TextualInversion 支持吗？",
        ["unsupported"],
        ["把隐藏后端说成可用"],
    ),
    "network-algos/lokr-guide.md": (
        "LoKr 在哪些路径有产品级证明？lokr_factor=-1 什么意思？",
        ["Anima", "无穷"],
        ["宣称 LoKr 全面优于 LoRA"],
    ),
    "network-algos/tlora-anima-guide.md": (
        "T-LoRA 能用在哪？收敛比 LoRA 慢正常吗？",
        ["Anima", "慢"],
        ["把动态 rank 说成动态采样"],
    ),
    "network-algos/dylora-guide.md": (
        "DyLoRA 的两个入口分别是什么？能直接从工作台导出多 rank 吗？",
        ["networks.dylora", "lycoris"],
        ["承诺 slice-export"],
    ),
    "network-algos/oft-guide.md": (
        "SD1.5 页面选 OFT 为什么报错？Flux 的 OFT 和 SDXL 的是同一个模块吗？",
        ["sdxl-lora", "oft_flux"],
        ["建议绕过前端诊断"],
    ),
    "network-algos/lycoris-family-guide.md": (
        "LyCORIS 有哪些 algo？LoHa/LoKr/IA3 的 dropout 有什么特殊性？",
        ["locon", "不支持"],
        ["把页面可用性说成实测效果"],
    ),
    "network-algos/anima-schema-only-adapters.md": (
        "在 Anima 页面选了 VeRA/LoRA-FA 实际训到的是什么？",
        ["networks.lora_anima", "plain"],
        ["把 UI 选项当后端能力"],
    ),
    "directions/character-identity.md": (
        "角色 LoRA 的触发词怎么定？覆盖矩阵指什么？",
        ["trigger", "覆盖"],
        ["给出保证身份一致的具体步数"],
    ),
    "directions/style-training.md": (
        "画风 LoRA 最容易泄漏什么？光影质感算画风方向吗？",
        ["co-varies", "style"],
        ["把风格强度给出校准数值"],
    ),
    "directions/object-product-concept.md": (
        "产品 LoRA 文字 logo 复刻靠谱吗？视角覆盖为什么关键？",
        ["不可靠", "视角"],
        ["承诺精确 logo 复刻"],
    ),
    "directions/clothing-accessory.md": (
        "只想学服装不想学模特脸，数据集要怎么设计？",
        ["wearer", "解耦"],
        ["说单模特单服装就够"],
    ),
    "directions/pose-expression-features.md": (
        "姿势 LoRA 能当 ControlNet 用吗？",
        ["tendency", "ControlNet"],
        ["承诺受控姿态输出"],
    ),
    "directions/scene-domain-migration.md": (
        "场景/领域迁移选 LoRA 还是全量微调？风险差在哪？",
        ["遗忘", "first-class"],
        ["把 LoRA 说成能注入任意能力"],
    ),
    "directions/utility-correction-lora.md": (
        "修手 LoRA 靠什么起效？enable_base_weight 是修正机制吗？",
        ["contrast", "差异炼丹"],
        ["承诺自动质量修正"],
    ),
    "directions/multi-concept-training.md": (
        "多概念一个 LoRA 训练要注意什么？组合是保证吗？",
        ["token", "balance"],
        ["承诺 N 概念等于 N 个单独 LoRA"],
    ),
    "directions/slider-erasure-boundaries.md": (
        "本产品能训练概念 slider 或擦除概念吗？",
        ["not first-class", "erasure"],
        ["给出 slider 教程"],
    ),
    "datasets/preparation-checklist.md": (
        "train_data_dir 直接铺图有什么风险？合法子目录长什么样？",
        ["zkz", "move"],
        ["说自动移动是无害便利"],
    ),
    "datasets/caption-tag-trigger-strategy.md": (
        "开 shuffle_caption 后触发词怎么保稳定？weighted 语法和 shuffle 能同开吗？",
        ["keep_tokens", "不推荐"],
        ["承诺 dropout 率最优值"],
    ),
    "datasets/regularization-images.md": (
        "LoRA 页面加正则化图有产品依据吗？prior loss 属于哪个流程？",
        ["DreamBooth", "unproven"],
        ["把 reg 图说成 LoRA 防遗忘特性"],
    ),
    "parameters/resolution-bucket.md": (
        "共享默认 512,512 直接拿去训 SDXL 行吗？SDXL bucket step 下限？",
        ["1024", "32"],
        ["给出分辨率质量对照表"],
    ),
    "parameters/exposure-budget-steps.md": (
        "平铺目录自动建议的 repeat 档位是什么？步数公式和日志谁为准？",
        ["7", "日志"],
        ["给 universal 最优步数"],
    ),
    "parameters/optimizer-scheduler-guide.md": (
        "用 Prodigy 时 unet_lr 必须是多少？DAdapt 系配什么 scheduler？",
        ["1", "constant"],
        ["承诺某优化器最优"],
    ),
    "parameters/cache-precision-guide.md": (
        "cache_text_encoder_outputs 和哪个字段硬冲突？cache_latents 呢？",
        ["shuffle_caption", "color_aug"],
        ["承诺 fp8 质量等价"],
    ),
    "training/preview-sampling-evaluation.md": (
        "enable_preview 默认值是什么？Anima 的预览约定是什么？",
        ["false", "1024"],
        ["把预览设置当推理推荐"],
    ),
    "training/checkpoint-selection.md": (
        "save_state/resume 在哪类页面有契约？LoRA 页等价能力未知吗？",
        ["DreamBooth", "unknown"],
        ["说 epoch 越靠后越好"],
    ),
    "training/repro-publishing-workflow.md": (
        "发布 LoRA 时 base 和触发词字段为什么要逐字？strength band 没有实测怎么写？",
        ["verbatim", "test from low strength"],
        ["把借用数值写进发布说明"],
    ),
    "errors/oom-performance-playbook.md": (
        "训练步 OOM 的降载梯子顺序是什么？低显存能承诺 dim-X@1024 装进 8G 吗？",
        ["cache", "gradient_checkpointing"],
        ["给 VRAM 数字承诺"],
    ),
    "external-channels/sd-scripts-config-reading.md": (
        "sd-scripts 中出现的字段能否直接加入 Next Trainer 模板？",
        ["route", "validator"],
        ["把外部示例值当作产品默认"],
    ),
    "external-channels/musubi-tuner-krea2-contract.md": (
        "Musubi-Tuner README 是否足以证明 Krea 2 模板可导入？",
        ["validator", "upstream"],
        ["把上游引擎文档当成导入证明"],
    ),
    "external-channels/diffusers-lora-translation.md": (
        "能否把 Diffusers LoRA YAML 直接改名为 Next Trainer TOML？",
        ["no", "validator"],
        ["直接复制外部配置"],
    ),
    "external-channels/diffusers-dreambooth-prior-preservation.md": (
        "Diffusers 的 prior-preservation 参数能否直接填入 LoRA 模板？",
        ["DreamBooth", "no"],
        ["把 prior preservation 说成通用 LoRA 能力"],
    ),
    "external-channels/lycoris-upstream-boundaries.md": (
        "LyCORIS 仓库有 LoHa，是否可以在每个页面生成 LoHa 模板？",
        ["page", "validator"],
        ["把上游算法存在当作全页面支持"],
    ),
    "external-channels/alternative-tooling-evidence.md": (
        "SimpleTuner 的 dataset manifest 能否直接放进 Next Trainer？",
        ["no", "mapping"],
        ["承诺跨工具配置兼容"],
    ),
    "external-channels/onetrainer-comparison.md": (
        "OneTrainer 的字段名能否直接加入 Next Trainer？",
        ["no", "contract"],
        ["承诺跨工具字段兼容"],
    ),
    "external-channels/joycaption-caption-review.md": (
        "使用 JoyCaption 生成 caption 后，是否可以跳过触发词和泄漏检查？",
        ["no", "review"],
        ["跳过触发词检查"],
    ),
    "external-channels/concept-sliders-research-channel.md": (
        "Concept Sliders 论文是否证明当前 Next Trainer 支持 slider？",
        ["no", "unsupported"],
        ["把论文当作产品支持证明"],
    ),
    "external-channels/peft-adapter-taxonomy.md": (
        "PEFT 支持某 adapter 是否代表 Next Trainer 页面支持它？",
        ["no", "validator"],
        ["把 PEFT 库支持当作产品支持"],
    ),
    "external-channels/safetensors-checkpoint-metadata.md": (
        "safetensors 文件没有 metadata 时能否按常见值补齐？",
        ["unknown", "no"],
        ["用默认值填补缺失 metadata"],
    ),
    "external-channels/bitsandbytes-optimizer-context.md": (
        "看到 AdamW8bit 就能保证低显存训练成功吗？",
        ["no", "runtime"],
        ["承诺低显存成功"],
    ),
    "external-channels/attention-memory-runtime.md": (
        "xFormers 支持某 attention 实现，是否意味着所有 Next Trainer 页面都能开启？",
        ["no", "schema"],
        ["把外部 runtime 能力当作页面支持"],
    ),
    "external-channels/kohya-gui-comparison.md": (
        "Kohya GUI 的 preset 能否直接作为 Next Trainer TOML？",
        ["no", "mapping"],
        ["直接复制 GUI preset"],
    ),
    "external-channels/hf-model-card-provenance.md": (
        "Hugging Face 模型卡能否直接决定 Next Trainer 的模板字段？",
        ["不能", "validator"],
        ["把下载量当作技术证据"],
    ),
    "external-channels/hf-metadata-missingness.md": (
        "API 响应被截断时，是否可以按空字段统计缺失？",
        ["unknown", "size-limit"],
        ["补默认值"],
    ),
    "external-channels/examples-config-translation.md": (
        "复制 Diffusers example 的字段到 Next Trainer TOML 是否足够？",
        ["不足", "validator"],
        ["盲抄默认值"],
    ),
    "external-channels/captioning-blip-lavis-review.md": (
        "自动 caption 是否可以跳过人工抽样直接训练？",
        ["不可以", "抽样"],
        ["跳过人工复核"],
    ),
    "external-channels/dataset-ingestion-provenance.md": (
        "改变分片顺序后能否复用原 exposure budget？",
        ["不能", "重新记录"],
        ["直接复用"],
    ),
    "external-channels/dataset-visual-qa-fiftyone.md": (
        "FiftyOne 默认视图是否能替代按方向分层抽样？",
        ["不能", "分层"],
        ["默认视图替代"],
    ),
    "external-channels/clip-evaluation-boundaries.md": (
        "CLIP 分数最高的 checkpoint 是否必然是最佳发布版本？",
        ["不必然", "人工抽样"],
        ["单一总分决定"],
    ),
    "external-channels/pytorch-runtime-reproducibility.md": (
        "启用 AMP 是否可以不记录精度和硬件条件？",
        ["不可以", "复现"],
        ["省略硬件"],
    ),
    "external-channels/dataset-curation-datacomp.md": (
        "DataComp 的过滤阈值能否直接作为本地数据集默认值？",
        ["不能", "重新验证"],
        ["直接作为默认值"],
    ),
    "external-channels/instruction-editing-objective-boundary.md": (
        "编辑指令数据能否直接套用角色 LoRA 模板？",
        ["不能", "目标函数"],
        ["直接套用"],
    ),
}


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    manifest_path = root / "04_知识库候选" / "knowledge-manifest.jsonl"
    out_path = root / "06_评测与校验" / "eval-candidates" / "knowledge-citation-draft.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    candidates = [rec["path"] for rec in manifest if rec["status"] == "candidate"]

    missing = [p for p in candidates if p not in QUESTIONS]
    extra = [p for p in QUESTIONS if p not in candidates]
    if missing or extra:
        print(f"[error] missing question for {missing}; unknown question for {extra}")
        return 1

    rows = []
    for i, path in enumerate(sorted(candidates), start=1):
        question, must_include, must_not = QUESTIONS[path]
        rows.append({
            "eval_seed_id": f"kc-{i:03d}",
            "kind": "knowledge-citation",
            "target_doc": path,
            "question": question,
            "must_cite": [path],
            "must_include": must_include,
            "boundary_must_not": must_not,
            "status": "draft-unrun",
            "note": "citation draft only; not executed against a live agent — formal eval seeds live in the plugin seeds dir and were NOT modified",
        })
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"drafts": len(rows), "path": str(out_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Reproduction & publishing workflow (honest handoff of a trained artifact)

- Version: `2026-08-30`
- Scope: what to record and publish with a trained LoRA/model so others (and future-you) can reproduce and correctly use it — seeds/logging surfaces, config capture, base/trigger metadata rules, hashing, and the product's update-channel boundary.
- Evidence status: L1 project contract (seed/log fields; safetensors save defaults; Civitai-reading doc for metadata fields); workflow discipline is project practice, tagged.
- Aliases / 检索关键词: 复现, 发布, 播种, seeding, publish, 元数据, sha256, config 快照, trigger 说明, 版本

## Reproduction record (L1 fields + practice)

Capture with every run worth keeping:

1. **Full exported config** (the page's exported TOML/params dump) — including fields you didn't touch; family default traps (512 vs 1024, TE-cache, fp8) are exactly the ones memory omits.
2. **Seeds**: training `seed` (shared default 1337) and preview `sample_seed` (default 2333) — different jobs, both matter; Anima documented preview seed is 42 (documented family value).
3. **Environment notes that change contracts**: torch version where documented guidance binds (Anima NaN/CAME guidance requires PyTorch ≥2.5 wording), musubi runtime presence for Krea 2, plugin version for marketplace flows — mark each with where it came from (L1 doc vs observation).
4. **Logs**: `log_with` defaults `tensorboard` (`logging_dir` ./logs; wandb selectable) — archive the run's log dir with the config.
5. **Dataset fingerprint**: file count, subdir/repeat layout, caption convention snapshot (hash the caption set if collaborating).

## Publishing metadata rules (formal-doc backed)

- Base model field: exact family/version ("trained on X, tested on X"); readers re-use by base match — the formal Civitai-reading doc makes base the hard-stop field (`workflows/civitai-model-to-lora.md`).
- Trigger words: publish the *verbatim* trigger list and caption convention used (the same doc's verbatim rule, applied outward).
- Preview/settings honesty: publish sampler/cfg/steps/seed used for the samples (from `preview-sampling-evaluation.md`) so others' first-look expectations are calibrated.
- Recommended strength bands: only from **your** measured sweeps; otherwise write "test from low strength" — an honest unknown beats a borrowed number (EDD rule, formal `parameters/parameter-evidence-rules.md`).

## Artifact integrity (practice)

- Hash the file you publish (sha256 is the convention this staging system itself uses in its manifests) and publish the hash with the download.
- Version artifacts like code (run tag = dataset fingerprint + config hash suffix); "final_v3_realfinal" is how wrong-checkpoint support threads start.

## Update-channel boundary (do not confuse)

Publishing *your trained artifact* (to Civitai or anywhere) is a user act outside the product. The managed **content channel** (`errors/managed-channel-updates.md`, formal doc) distributes plugin *knowledge/template assets* with assetsVersion bumps — trained LoRAs never ride that channel; keep personal artifacts in your own storage/versioning.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/shared.ts` (seed/log/save fields), `docs/anima-training.md` (preview seed/torch guidance).
- Formal knowledge: `workflows/civitai-model-to-lora.md`, `errors/managed-channel-updates.md`, `parameters/parameter-evidence-rules.md`.

## Boundaries

- No product feature exports "reproduction packages"; this checklist is user-side discipline built on captured surfaces.
- Do not claim safetensors metadata fields beyond `save_model_as`/precision are written automatically — metadata hygiene is your pipeline's job.
- Publishing platforms' own rules (Civitai model pages etc.) change; the KB records the *fields that matter*, not platform UI steps.

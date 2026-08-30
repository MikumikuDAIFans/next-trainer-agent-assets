"""Reconstruct the 16 template artifacts lost during integration.

This is deliberately explicit and append-only: it never claims byte recovery.
All outputs are written under AgentAssets/assets/templates.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "templates"

TEMPLATES = {
"anima-fast-lora-character.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-fast-lora-character"
base_model = "anima"
model_train_type = "anima-lora-fast"
network_module = "networks.lora_anima"
network_dim = 16
network_alpha = 16
resolution = "1024,1024"
enable_bucket = true
train_batch_size = 1
gradient_checkpointing = true
optimizer_type = "AdamW8bit"
learning_rate = 0.0001
mixed_precision = "bf16"
cache_latents = false
cache_text_encoder_outputs = false
skip_cache_check = true
torch_compile = true
static_token_count = 4096
compile_mode = "blocks"
dynamo_backend = "inductor"
attn_mode = "flash"
''',
"anima-fast-lora-style.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-fast-lora-style"
base_model = "anima"
model_train_type = "anima-lora-fast"
network_module = "networks.lora_anima"
network_dim = 32
network_alpha = 16
resolution = "1024,1024"
enable_bucket = true
train_batch_size = 1
gradient_checkpointing = true
optimizer_type = "AdamW8bit"
learning_rate = 0.00005
mixed_precision = "bf16"
cache_latents = false
cache_text_encoder_outputs = false
skip_cache_check = true
torch_compile = true
static_token_count = 4096
compile_mode = "blocks"
dynamo_backend = "inductor"
attn_mode = "flash"
''',
"anima-lora-character-automagic.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-lora-character-automagic"
base_model = "anima"
model_train_type = "anima-lora"
lora_type = "lora"
network_module = "networks.lora_anima"
network_dim = 16
network_alpha = 16
network_train_unet_only = true
network_train_text_encoder_only = false
resolution = "1024,1024"
enable_bucket = true
min_bucket_reso = 256
max_bucket_reso = 1024
bucket_reso_steps = 64
bucket_no_upscale = false
train_batch_size = 1
gradient_checkpointing = true
gradient_accumulation_steps = 1
optimizer_type = "Automagic"
learning_rate = 0.0001
unet_lr = 0.0001
text_encoder_lr = 0
lr_scheduler = "constant"
lr_warmup_steps = 0
mixed_precision = "bf16"
save_precision = "bf16"
cache_latents = true
cache_latents_to_disk = true
cache_text_encoder_outputs = true
cache_text_encoder_outputs_to_disk = true
max_data_loader_n_workers = 2
''',
"anima-lora-style-automagic.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-lora-style-automagic"
base_model = "anima"
model_train_type = "anima-lora"
lora_type = "lora"
network_module = "networks.lora_anima"
network_dim = 32
network_alpha = 16
network_train_unet_only = true
network_train_text_encoder_only = false
resolution = "1024,1024"
enable_bucket = true
min_bucket_reso = 256
max_bucket_reso = 1024
bucket_reso_steps = 64
bucket_no_upscale = false
train_batch_size = 1
gradient_checkpointing = true
gradient_accumulation_steps = 1
optimizer_type = "Automagic"
learning_rate = 0.00005
unet_lr = 0.00005
text_encoder_lr = 0
lr_scheduler = "constant"
lr_warmup_steps = 0
mixed_precision = "bf16"
save_precision = "bf16"
cache_latents = true
cache_latents_to_disk = true
cache_text_encoder_outputs = true
cache_text_encoder_outputs_to_disk = true
max_data_loader_n_workers = 2
''',
"anima-lora-lokr-conservative.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-lora-lokr-conservative"
base_model = "anima"
model_train_type = "anima-lora"
lora_type = "lokr"
network_module = "lycoris.kohya"
lycoris_algo = "lokr"
lokr_factor = -1
network_dim = 16
network_alpha = 16
resolution = "1024,1024"
enable_bucket = true
train_batch_size = 1
gradient_checkpointing = true
optimizer_type = "Automagic"
learning_rate = 0.0001
mixed_precision = "bf16"
''',
"anima-lora-tlora-conservative.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "anima-lora-tlora-conservative"
base_model = "anima"
model_train_type = "anima-lora"
lora_type = "tlora"
network_module = "networks.tlora_anima"
tlora_min_rank = 1
network_dim = 16
network_alpha = 16
resolution = "1024,1024"
enable_bucket = true
train_batch_size = 1
gradient_checkpointing = true
optimizer_type = "Automagic"
learning_rate = 0.0001
mixed_precision = "bf16"
''',
"flux-lora-oft-conservative.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "flux-lora-oft-conservative"
base_model = "flux"
model_train_type = "flux-lora"
lora_type = "oft"
network_module = "networks.oft_flux"
timestep_sampling = "sigmoid"
fp8_base = true
resolution = "768,768"
enable_bucket = true
bucket_no_upscale = true
enable_preview = true
sample_width = 768
sample_height = 768
sample_every_n_epochs = 2
''',
"sd-dylora-conservative.toml": '''# reconstructed-2026-08-30; original bytes unavailable
template_version = "2026-08-30-reconstructed"
scope = "sd-dylora-conservative"
base_model = "sd"
model_train_type = "sd-lora"
network_module = "networks.dylora"
dylora_unit = 4
network_dim = 32
network_alpha = 32
resolution = "512,512"
enable_bucket = true
bucket_no_upscale = true
enable_preview = true
sample_width = 512
sample_height = 512
sample_every_n_epochs = 2
''',
}

OLD_HASHES = {
"anima-fast-lora-character.toml":"85098f53084ef289c711ab5e922273984ddc521b8de59a8074dc2e100b13e062",
"anima-fast-lora-style.toml":"dcd215664663361d9f87b88e0e56c7496bc4d1de4810ac9c3fa705331b818395",
"anima-lora-character-automagic.toml":"b0661130ad80f694b4627d8dbd005c8f08fce2bfcb8598b92964df822953f7bf",
"anima-lora-lokr-conservative.toml":"596996ca3ea50da13761e38310c01d2fb655a9af6830d86a2aa7545acecf70b9",
"anima-lora-style-automagic.toml":"960faa0c90f699523a5e61c8c5a01ae89d7edda93c37e05d28abffee081f62eb",
"anima-lora-tlora-conservative.toml":"af063e359202a011be388252f9f7cb835fa7d6073a3bad471899afcde4f5c1ae",
"flux-lora-oft-conservative.toml":"98a34d8e3e91cad9de91e1af044cb6d98b8dc16ea880c2f99868fa0a66693dfd",
"sd-dylora-conservative.toml":"9ded60b6e1c382f739b59f9bf44f524a53e5d69aa455c04edfc146d4d3be1358",
}

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = ["# Reconstruction report — F-S4-002", "", "Original bytes were unavailable; every output below is a reconstructed candidate.", ""]
    for name, body in TEMPLATES.items():
        path = OUT / name
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing file: {path}")
        path.write_text(body, encoding="utf-8", newline="\n")
        digest = sha256(path.read_bytes()).hexdigest()
        report.append(f"- `{name}`: old frozen sha256 `{OLD_HASHES[name]}`; reconstructed sha256 `{digest}`; equal=`{digest == OLD_HASHES[name]}`")
        card = OUT / f"{Path(name).stem}.evidence.md"
        card.write_text(
            f"# {Path(name).stem} — reconstructed evidence card\n\n"
            f"- Version: `2026-08-30-reconstructed`\n"
            f"- Scope: Reconstructed candidate after F-S4-002 template loss; original bytes unavailable.\n"
            f"- Evidence status: `reconstructed`; old frozen hash is retained for comparison only.\n"
            f"- Aliases / 检索关键词: reconstructed, F-S4-002, {Path(name).stem}\n\n"
            "## Reconstruction basis\n\n"
            "Fields were rebuilt from the frozen template coverage matrix, Stage 3 validator artifacts, current project schema/presets, and the corresponding network-algorithm knowledge document. This is a semantic reconstruction, not byte-level recovery.\n\n"
            "## Sources\n\n"
            "- `data/template-index/template-coverage-matrix.csv` (frozen coverage and decision record)\n"
            "- `governance/evidence/stage-3/phase-3/` validator artifacts (page/result/negative-control assertions)\n"
            "- current project schema and presets (read-only evidence source)\n\n"
            "## Boundaries\n\n"
            "- Old SHA-256 is not reproduced and must not be described as recovered.\n"
            "- Validator success proves import contract only; it does not prove training quality or empirical defaults.\n"
            "- User approval is required before any formal migration.\n\n"
            "## Eval\n\n"
            "- Question: Is this file byte-identical to the deleted original?\n"
            "- Expected answer: no; it is explicitly reconstructed and requires review.\n",
            encoding="utf-8", newline="\n")
    (ROOT / "governance" / "evidence" / "stage-4" / "reconstruction-report-F-S4-002.md").write_text("\n".join(report)+"\n", encoding="utf-8", newline="\n")

if __name__ == "__main__":
    main()

"""Stage 3 template gate: validate candidate TOMLs through the REAL project validator.

Run with the project venv python, e.g.:
  <project>\\.venv-dev\\Scripts\\python.exe -B <staging>\\tools\\stage3_validate_templates.py <staging_root> <project_root>

Guarantees encoded here (checklist Stage 3):
- every candidate has explicit model_train_type (no [skip] paths)
- real validate_config_import must return result == "ok" on the page a user actually lands on
  (weak-pass page keys like "sd-lora" are recorded, never used as the primary proof)
- redirect != pass, skip != pass, parse-only != pass
- negative controls: each template must NOT pass on a wrong page (proves the gate can fail)
- normalized diff (input keys vs validator-normalized config) is dumped per template
- zero-short run: templates are copied to an empty temp dir and re-validated there
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

try:
    import tomllib

    def loads(text: str) -> dict:
        return tomllib.loads(text)
except ModuleNotFoundError:  # py310 venv
    import toml as _toml

    def loads(text: str) -> dict:
        return _toml.loads(text)

STAGING = Path(sys.argv[1]).resolve()
PROJECT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(PROJECT))
from mikazuki.utils.config_import import validate_config_import  # noqa: E402

TPL_DIR = STAGING / "05_模板库候选"
OUT_DIR = STAGING / "06_评测与校验" / "evidence" / "stage-3" / "phase-3"
FORMAL_TPL_DIR = PROJECT.parent / "agent-assets" / "assets" / "templates"

# candidate -> (strong PAGE_SPECS key, wrong page for negative control)
CANDIDATES = {
    "flux-lora-conservative.toml": ("flux-lora", "sdxl-lora"),
    "chroma-lora-conservative.toml": ("flux-lora", "krea2-lora"),
    "krea2-lora-conservative.toml": ("krea2-lora", "lora-master"),
    "sd2-lora-conservative.toml": ("lora-master", "flux-lora"),
    "sd-dreambooth-conservative.toml": ("dreambooth", "flux-lora"),
    "anima-lora-character-automagic.toml": ("anima-lora", "flux-lora"),
    "anima-lora-style-automagic.toml": ("anima-lora", "flux-lora"),
    "anima-fast-lora-character.toml": ("anima-lora-fast", "flux-lora"),
    "anima-fast-lora-style.toml": ("anima-lora-fast", "flux-lora"),
    "anima-lora-lokr-conservative.toml": ("anima-lora", "flux-lora"),
    "anima-lora-tlora-conservative.toml": ("anima-lora", "flux-lora"),
    "flux-lora-oft-conservative.toml": ("flux-lora", "sdxl-lora"),
    "sd-dylora-conservative.toml": ("lora-master", "flux-lora"),
}

# research-rejected drafts -> (page, expected non-ok result): the rejection itself is a tested
# assertion (regression guard), documented in evidence/stage-3/phase-3/failure-*.md
REJECTED_EXPECTATIONS = {
    "sdxl-finetune-conservative.toml": ("dreambooth", "redirect"),
    "sdxl-lora-oft-conservative.toml": ("sdxl-lora", "ok"),
}

REQUIRED_KEYS = ("template_version", "scope", "base_model", "model_train_type")
SECRET_RE = re.compile(r"(?i)(wandb_api_key|api[_-]?key[ \t]*[:=]|token[ \t]*[:=][ \t]*[A-Za-z0-9]|cookie[ \t]*[:=]|password[ \t]*[:=])")
DRIVE_RE = re.compile(r"(?i)\b(?![Xx]:)[A-Z]:[\\/]")


def lint_template(path: Path, cfg: dict) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        problems.append("BOM present")
    for key in REQUIRED_KEYS:
        if not cfg.get(key):
            problems.append(f"missing required header key: {key}")
    if SECRET_RE.search(text):
        problems.append("credential-looking string")
    if DRIVE_RE.search(text):
        problems.append("machine drive path found")
    for forbidden in ("train_data_dir", "output_dir", "pretrained_model_name_or_path", "dit", "vae", "text_encoder"):
        if forbidden in cfg:
            problems.append(f"path-bearing field present: {forbidden}")
    return problems


def normalized_diff(cfg: dict, norm: dict) -> dict:
    before = {k: v for k, v in cfg.items()}
    after = norm or {}
    added = {k: after[k] for k in after if k not in before}
    removed = {k: before[k] for k in before if k not in after}
    changed = {
        k: {"was": before[k], "now": after[k]}
        for k in after
        if k in before and after[k] != before[k]
    }
    return {"added": added, "removed": removed, "changed": changed}


def run_suite(tdir: Path, artifact_prefix: str) -> tuple[int, list[str]]:
    failures: list[str] = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, (page, wrong_page) in sorted(CANDIDATES.items()):
        tf = tdir / name
        if not tf.exists():
            failures.append(f"{name}: missing candidate file")
            continue
        cfg = loads(tf.read_text(encoding="utf-8"))
        problems = lint_template(tf, cfg)
        # name-collision guard against the formal 4 (staging must not shadow shipped templates)
        if FORMAL_TPL_DIR.exists() and (FORMAL_TPL_DIR / name).exists():
            problems.append(f"name collision with formal template: {name}")
        if not (TPL_DIR / (tf.stem + ".evidence.md")).exists():
            problems.append("missing paired evidence card")

        res = validate_config_import(page, dict(cfg))
        result = res.get("result")
        if result != "ok":
            problems.append(f"validator on page {page!r}: {result} errors={res.get('errors')}")
        neg = validate_config_import(wrong_page, dict(cfg))
        if neg.get("result") == "ok":
            problems.append(f"negative control leaked: page {wrong_page!r} returned ok")

        diff = normalized_diff(cfg, res.get("config") or {})
        artifact = {
            "template": name,
            "page": page,
            "result": result,
            "forced_train_type": res.get("forced_train_type"),
            "inferred_train_type": res.get("inferred_train_type"),
            "notice": res.get("notice"),
            "negative_control": {"page": wrong_page, "result": neg.get("result")},
            "normalized_diff": diff,
        }
        (OUT_DIR / f"{artifact_prefix}{tf.stem}.json").write_text(
            json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        status = "ok" if not problems else "FAIL: " + "; ".join(problems)
        rows.append(f"[{'ok' if not problems else 'FAIL'}] {name} page={page} negctl={neg.get('result')} "
                    f"diff+{len(diff['added'])}/-{len(diff['removed'])}/~{len(diff['changed'])} :: {status}")
        failures.extend(f"{name}: {p}" for p in problems)

    print("\n".join(rows))

    rej_dir = TPL_DIR / "research-rejected"
    for name, (page, expected) in sorted(REJECTED_EXPECTATIONS.items()):
        tf = rej_dir / name
        if not tf.exists():
            failures.append(f"{name}: rejected draft missing (assertion target)")
            continue
        res = validate_config_import(page, loads(tf.read_text(encoding="utf-8")))
        got = res.get("result")
        ok = got == expected
        rows_msg = f"[{'ok' if ok else 'FAIL'}] rejected-assertion {name} page={page} expected={expected} got={got}"
        print(rows_msg)
        (OUT_DIR / f"{artifact_prefix}rejected-{tf.stem}.json").write_text(
            json.dumps({"template": name, "page": page, "expected": expected, "got": got,
                        "normalized_type": (res.get("config") or {}).get("model_train_type")},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        if not ok:
            failures.append(f"{name}: rejected-assertion expected {expected}, got {got}")

    return (1 if failures else 0), failures


def main() -> int:
    rc, failures = run_suite(TPL_DIR, "")

    # zero-short: empty temp dir copy
    with tempfile.TemporaryDirectory(prefix="stage3-zeroshort-") as tmp:
        tdir = Path(tmp)
        for name in CANDIDATES:
            shutil.copy2(TPL_DIR / name, tdir / name)
        rc2, failures2 = run_suite(tdir, "zeroshort-")
    rc = max(rc, rc2)

    print(json.dumps({"pass": rc == 0, "failures": failures + failures2}, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

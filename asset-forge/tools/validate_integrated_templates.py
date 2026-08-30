"""Validate the integrated assets/templates tree through the real host validator.

The integrated layout is intentionally independent from the deleted staging
directory. This tool never writes to project or agent-assets.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    import toml as tomllib

ROOT = Path(sys.argv[1]).resolve()
PROJECT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(PROJECT))
from mikazuki.utils.config_import import validate_config_import

CASES = {
    "anima-fast-lora-character.toml": ("anima-lora-fast", "flux-lora"),
    "anima-fast-lora-style.toml": ("anima-lora-fast", "flux-lora"),
    "anima-lora-character-automagic.toml": ("anima-lora", "flux-lora"),
    "anima-lora-style-automagic.toml": ("anima-lora", "flux-lora"),
    "anima-lora-lokr-conservative.toml": ("anima-lora", "flux-lora"),
    "anima-lora-tlora-conservative.toml": ("anima-lora", "flux-lora"),
    "flux-lora-oft-conservative.toml": ("flux-lora", "sdxl-lora"),
    "sd-dylora-conservative.toml": ("lora-master", "flux-lora"),
    "chroma-lora-conservative.toml": ("flux-lora", "krea2-lora"),
    "flux-lora-conservative.toml": ("flux-lora", "sdxl-lora"),
    "krea2-lora-conservative.toml": ("krea2-lora", "lora-master"),
    "sd-dreambooth-conservative.toml": ("dreambooth", "flux-lora"),
    "sd2-lora-conservative.toml": ("lora-master", "flux-lora"),
}

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def normalized_diff(before: dict, after: dict) -> dict:
    added = {k: after[k] for k in after if k not in before}
    removed = {k: before[k] for k in before if k not in after}
    changed = {
        k: {"before": before[k], "after": after[k]}
        for k in before
        if k in after and before[k] != after[k]
    }
    return {"added": added, "removed": removed, "changed": changed}

def main() -> int:
    tdir = ROOT / "assets" / "templates"
    out = ROOT / "governance" / "evidence" / "stage-4" / "integrated-template-validation.json"
    rows, failures = [], []
    for name, (page, wrong) in sorted(CASES.items()):
        path = tdir / name
        card = tdir / f"{Path(name).stem}.evidence.md"
        if not path.exists() or not card.exists():
            failures.append(f"missing pair: {name}")
            continue
        try:
            cfg = tomllib.loads(path.read_text(encoding="utf-8"))
            res = validate_config_import(page, dict(cfg))
            neg = validate_config_import(wrong, dict(cfg))
        except Exception as exc:
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
            continue
        if res.get("result") != "ok":
            failures.append(f"{name}: page result {res.get('result')}")
        if neg.get("result") == "ok":
            failures.append(f"{name}: negative control leaked on {wrong}")
        if "reconstructed-2026-08-30" not in path.read_text(encoding="utf-8") and name in {
            "anima-fast-lora-character.toml", "anima-fast-lora-style.toml",
            "anima-lora-character-automagic.toml", "anima-lora-style-automagic.toml",
            "anima-lora-lokr-conservative.toml", "anima-lora-tlora-conservative.toml",
            "flux-lora-oft-conservative.toml", "sd-dylora-conservative.toml",
        }:
            failures.append(f"{name}: missing reconstruction marker")
        diff = normalized_diff(dict(cfg), res.get("config") or {})
        rows.append({"template": name, "page": page, "result": res.get("result"),
                     "negativeControl": {"page": wrong, "result": neg.get("result")},
                     "normalizedConfigSha256": digest(path),
                     "normalizedDiff": diff,
                     "reconstructed": "reconstructed-2026-08-30" in path.read_text(encoding="utf-8")})
    report = {"templates": len(rows), "failures": failures, "result": "pass" if not failures and len(rows) == len(CASES) else "fail", "rows": rows}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ("templates", "failures", "result")}, ensure_ascii=False))
    return 1 if report["result"] != "pass" else 0

if __name__ == "__main__":
    raise SystemExit(main())

"""Offline template gate: validate every assets/templates/*.toml through the
real project validator (mikazuki.utils.config_import.validate_config_import).
Usage: python validate-templates.py [templates_dir]
Exit 0 iff every template returns result != reject for its declared page type.
"""
import sys
from pathlib import Path

try:
    import tomllib  # py311+
    def _loads(text: str) -> dict:
        return tomllib.loads(text)
except ModuleNotFoundError:  # project venv may be py310 with third-party toml
    import toml as _toml
    def _loads(text: str) -> dict:
        return _toml.loads(text)

ASSETS = Path(__file__).resolve().parents[1]
PROJECT = ASSETS.parent / "project"
sys.path.insert(0, str(PROJECT))
from mikazuki.utils.config_import import validate_config_import  # noqa: E402

SCOPE_PAGE = {  # scope prefix -> pageTrainType used for validation
    "anima-lora-fast": "anima-lora-fast",
    "anima-lora": "anima-lora",
    "sd15-lora": "sd-lora",
    "sdxl-lora": "sdxl-lora",
}

def main() -> int:
    tdir = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS / "assets" / "templates"
    rc = 0
    for tf in sorted(tdir.glob("*.toml")):
        cfg = _loads(tf.read_text(encoding="utf-8"))
        scope = str(cfg.get("scope", tf.stem))
        # longest matching scope prefix wins (anima-lora-fast vs anima-lora)
        page = next((p for k, p in sorted(SCOPE_PAGE.items(), key=lambda kv: -len(kv[0])) if scope.startswith(k)), None)
        page = cfg.get("model_train_type") or page
        if page is None:
            print(f"[skip] {tf.name}: no pageTrainType resolvable from scope/model_train_type")
            continue
        res = validate_config_import(str(page), dict(cfg))
        result = res.get("result")
        errors = res.get("errors") or []
        if result == "reject":
            rc = 1
        print(f"[{result}] {tf.name} page={page} normalized_keys={len(res.get('config') or {})}"
              + (f" errors={errors}" if errors else ""))
    return rc

if __name__ == "__main__":
    raise SystemExit(main())

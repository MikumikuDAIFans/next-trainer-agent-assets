"""Release signing key resolution (rotation mechanism) stays honest."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load_release(monkeypatch, tmp_path, *, key_file=None, env_id=None, env_hex=None):
    for var in ("MIKAZUKI_RELEASE_SIGNING_FILE", "MIKAZUKI_RELEASE_SIGNING_KEY_ID", "MIKAZUKI_RELEASE_SIGNING_KEY_HEX"):
        monkeypatch.delenv(var, raising=False)
    if key_file is not None:
        monkeypatch.setenv("MIKAZUKI_RELEASE_SIGNING_FILE", str(key_file))
    if env_id is not None:
        monkeypatch.setenv("MIKAZUKI_RELEASE_SIGNING_KEY_ID", env_id)
    if env_hex is not None:
        monkeypatch.setenv("MIKAZUKI_RELEASE_SIGNING_KEY_HEX", env_hex)
    spec = importlib.util.spec_from_file_location("release_mod_test", REPO / "scripts" / "release.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_signing_falls_back_to_dev_key_without_env(monkeypatch, tmp_path):
    module = _load_release(monkeypatch, tmp_path)
    assert module.SIGNING_KEY_ID == "dev-local-signing"


def test_signing_key_file_is_used_and_dev_remains_the_default(tmp_path, monkeypatch):
    key_file = tmp_path / "signing-key.json"
    key_file.write_text(json.dumps({"keyId": "rotate-test-1", "keyHex": "ab" * 32}), encoding="utf-8")
    module = _load_release(monkeypatch, tmp_path, key_file=key_file)
    assert module.SIGNING_KEY_ID == "rotate-test-1"
    assert module.SIGNING_KEY_HEX == "ab" * 32
    # the dev constant itself never changes (transition trust depends on it)
    assert module._DEV_KEY_ID == "dev-local-signing"


def test_env_pair_beats_key_file(tmp_path, monkeypatch):
    key_file = tmp_path / "signing-key.json"
    key_file.write_text(json.dumps({"keyId": "file-key", "keyHex": "cd" * 32}), encoding="utf-8")
    module = _load_release(monkeypatch, tmp_path, key_file=key_file, env_id="env-key", env_hex="ef" * 32)
    assert module.SIGNING_KEY_ID == "env-key"
    assert module.SIGNING_KEY_HEX == "ef" * 32


def test_partial_env_fails_closed(tmp_path, monkeypatch):
    with pytest.raises(SystemExit):
        _load_release(monkeypatch, tmp_path, env_id="only-id-no-key")


def test_real_workspace_key_file_is_never_committed_here():
    # the key lives OUTSIDE this repo by policy; guard against accidents
    assert not (REPO / ".release-signing").exists()
    assert not (REPO / "signing-key.json").exists()

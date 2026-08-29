"""F2-3: the plugin manifest contract pin lives with its authoritative source.

The bridge/runtime/UI shape the plugin declares is a plugin property, so the
source repo (not the host that merely consumes it) must fail CI when it drifts.
The host keeps its own schema-validation tests over a synthetic fixture; this
test pins the REAL plugin.json here in agent-assets.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugin" / "next-trainer-pi-agent"

# The host's PluginManifest model validates the shape; locate it via env or the
# sibling main project (documented in README "维护模型速览"). Run via scripts/run-tests.py.
_project = os.environ.get("NEXT_TRAINER_PROJECT_ROOT", str(REPO_ROOT.parent / "project"))
sys.path.insert(0, _project)
from mikazuki.plugin_marketplace.models import PluginManifest  # noqa: E402

EXPECTED_BRIDGE_METHODS = {
    "session.list", "session.create", "session.rename", "session.delete",
    "session.getState", "session.getHistory", "session.getThinking", "session.prompt",
    "session.cancel", "session.compact", "session.setModel", "session.setThinkingLevel",
    "session.recallQueue", "session.subscribe", "provider.list", "provider.status",
    "provider.saveKey", "provider.removeKey", "provider.test", "resource.pick",
    "resource.getSummary", "artifact.open", "artifact.download", "confirmation.request",
    "confirmation.getResult", "navigation.openExternal", "navigation.openPluginRoute",
    "theme.get", "locale.get", "context.get",
}


def load_manifest() -> PluginManifest:
    value = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
    return PluginManifest.model_validate(value)


def test_plugin_manifest_covers_the_complete_bridge_contract():
    manifest = load_manifest()
    requests = {item.method for item in manifest.bridge.requests}
    streams = {item.method for item in manifest.bridge.streams}
    assert requests | streams == EXPECTED_BRIDGE_METHODS
    assert streams == {"session.subscribe"}
    assert len(requests) + len(streams) == len(EXPECTED_BRIDGE_METHODS)
    assert all(item.permission in manifest.permissions for item in manifest.bridge.requests)
    assert all(item.permission in manifest.permissions for item in manifest.bridge.streams)


def test_plugin_manifest_keeps_runtime_and_ui_in_the_plugin_package():
    manifest = load_manifest()
    assert manifest.id == "next-trainer-pi-agent"
    assert manifest.protocol_version == "1"
    assert manifest.runtime.entrypoint == "bin/next-trainer-pi-agent.exe"
    assert manifest.ui.entrypoint == "ui/index.html"
    assert manifest.ui.settings_entrypoint == "ui/settings.html"
    assert manifest.install_hooks == []
    # UI + SBOM source files must be present in the package tree.
    assert (PLUGIN_ROOT / "pi-web" / "ui" / "index.html").is_file() or (PLUGIN_ROOT / manifest.ui.entrypoint).is_file()


def test_plugin_html_entries_have_no_inline_script_authority():
    ui_dir = PLUGIN_ROOT / "pi-web" / "ui"
    if not ui_dir.is_dir():
        pytest.skip("built UI not present in source tree (ui/ is a build artifact)")
    for name in ("index.html", "settings.html"):
        f = ui_dir / name
        if not f.is_file():
            pytest.skip(f"UI html {name} is a build artifact")
        html = f.read_text(encoding="utf-8")
        assert "http://" not in html
        assert "https://" not in html


def test_pi_package_declares_no_skills_F3_0_single_source():
    """F3-0 decision 1 is law: skills reach the agent ONLY through the pi SDK
    user-scope dir (<dataRoot>/pi-agent/skills), seeded by the launcher and
    updated by the managed content channel. A pi.skills declaration in
    pi-package/package.json would make the SDK load a SECOND (package-scope)
    copy and re-introduce the double-source drift this decision removed."""
    package = json.loads((PLUGIN_ROOT / "pi-package" / "package.json").read_text(encoding="utf-8"))
    assert "skills" not in (package.get("pi") or {}), (
        "pi-package/package.json must NOT declare pi.skills — skills ship via "
        "seeds/skills -> launcher -> <dataRoot>/pi-agent/skills (F3-0 decision 1)."
    )
    # The skills tree belongs to the managed-content seeds, not the package.
    assert (REPO_ROOT / "assets" / "skills").is_dir()


def test_launcher_seeds_skills_into_user_scope_dir():
    """The launcher must copy seeds/skills into <agentDir>/skills so first
    installs have skills offline AND the managed channel owns the same dir."""
    launcher = (PLUGIN_ROOT / "launcher" / "src" / "main.ts").read_text(encoding="utf-8")
    assert 'walk(path.join(seedsRoot, "skills"), path.join(agentDir, "skills"))' in launcher


def test_manifest_grants_content_update_for_the_assets_tool():
    """The assets_update Host Tool is exposed only when the manifest declares
    the content-update permission (least privilege, F3-3)."""
    manifest = load_manifest()
    assert "content-update" in manifest.permissions


def test_packaged_permission_lists_cannot_drift_across_platforms():
    """The packaged manifest is written THREE times by the pipeline (win
    build-pi-web-package.py, the WSL linux stager, and historically the catalog
    builder — now derived from the win zip). A per-platform mismatch survives
    locally but dies mid-release when the host's validate_manifest_entry
    compares each platform zip against the single catalog entry — and there it
    wastes a full 25-minute dual build (this exact drift failed the 0.3.4
    build). Pin the equality HERE, where it costs milliseconds."""
    import re

    def literal_list(path: Path, marker: str) -> list[str]:
        text = path.read_text(encoding="utf-8")
        index = text.index(marker)
        bracket_start = text.index("[", index)
        bracket_end = text.index("]", bracket_start)
        return re.findall(r'"([^"]+)"', text[bracket_start : bracket_end + 1])

    scripts = PLUGIN_ROOT / "scripts"
    win = literal_list(scripts / "build-pi-web-package.py", '"permissions":')
    linux = literal_list(scripts / "wsl" / "wsl-stage-linux-package.sh", '"permissions":')
    assert win == linux, f"win/linux packaged permissions drifted: {win} != {linux}"

    source = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
    expected = [p for p in source["permissions"] if p != "model-provider"]
    assert win == expected, f"packaged lists {win} != source plugin.json minus model-provider {expected}"

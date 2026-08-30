#!/usr/bin/env python3
"""Validate staged Next Trainer support inventories against the read-only source tree."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


ALLOWED_LEVELS = {
    "first-class",
    "conditional",
    "backend-capable-ui-hidden",
    "unsupported",
    "unknown",
}

REQUIRED_ENTRY_KEYS = {
    "id",
    "displayName",
    "modelFamily",
    "baseModelVariants",
    "engine",
    "trainingGranularity",
    "schemaName",
    "pageTrainType",
    "backendEntrypoint",
    "adapterAlgorithms",
    "supportLevel",
    "prerequisites",
    "trainingDirectionInterface",
    "specializedDirections",
    "unsupportedSpecializedObjectives",
    "evidence",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_modules(project: Path) -> list[tuple[str, str, str, str]]:
    source = (project / "frontend/src/training/modules.ts").read_text(encoding="utf-8")
    pattern = re.compile(
        r'\{\s*model:\s*"([^"]+)",\s*engine:\s*"([^"]+)",\s*'
        r'target:\s*"([^"]+)",\s*schemaName:\s*"([^"]+)"'
    )
    return pattern.findall(source)


def source_trainer_mapping(project: Path) -> dict[str, str]:
    source = (project / "mikazuki/app/api.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "trainer_mapping"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            if not isinstance(value, dict):
                raise AssertionError("trainer_mapping is not a dictionary")
            return value
    raise AssertionError("trainer_mapping not found")


def validate(project: Path, assets: Path) -> dict:
    errors: list[str] = []
    raw = load_json(assets / "01_训练器能力盘点/raw-route-schema-map.json")
    matrix = load_json(assets / "01_训练器能力盘点/support-matrix.json")

    modules = raw.get("modules") or []
    entries = matrix.get("entries") or []
    module_ids = [item.get("id") for item in modules]
    entry_ids = [item.get("id") for item in entries]

    if len(module_ids) != len(set(module_ids)):
        errors.append("raw module IDs are not unique")
    if len(entry_ids) != len(set(entry_ids)):
        errors.append("support entry IDs are not unique")

    source_module_set = set(source_modules(project))
    raw_module_set = {
        (item.get("model"), item.get("engine"), item.get("target"), item.get("schemaName"))
        for item in modules
    }
    if source_module_set != raw_module_set:
        errors.append(
            "TRAINING_MODULES mismatch: "
            f"missing={sorted(source_module_set - raw_module_set)} "
            f"stray={sorted(raw_module_set - source_module_set)}"
        )

    trainer_mapping = source_trainer_mapping(project)
    for item in modules:
        if item.get("backendKind") != "trainer_mapping":
            continue
        train_type = item.get("serializedTrainType")
        expected = item.get("backendEntrypoint")
        actual = trainer_mapping.get(train_type)
        if actual != expected:
            errors.append(f"backend mismatch for {item.get('id')}: {actual!r} != {expected!r}")

    for item in entries:
        missing = sorted(REQUIRED_ENTRY_KEYS - set(item))
        if missing:
            errors.append(f"{item.get('id')}: missing keys {missing}")
        if item.get("supportLevel") not in ALLOWED_LEVELS:
            errors.append(f"{item.get('id')}: invalid supportLevel {item.get('supportLevel')!r}")
        if not item.get("evidence"):
            errors.append(f"{item.get('id')}: evidence is empty")
        for evidence in item.get("evidence") or []:
            if not isinstance(evidence, str) or evidence.startswith(("http://", "https://")):
                continue
            relative = evidence.split(":", 1)[0]
            if not (project / relative).exists():
                errors.append(f"{item.get('id')}: evidence path does not exist: {relative}")
        if item.get("supportLevel") in {"first-class", "conditional"}:
            if not item.get("pageTrainType") or not item.get("backendEntrypoint"):
                errors.append(f"{item.get('id')}: operational support lacks page/backend")
        backend = item.get("backendEntrypoint")
        if isinstance(backend, str) and backend.startswith("./"):
            if not (project / backend[2:]).is_file():
                errors.append(f"{item.get('id')}: backend file does not exist: {backend}")

    operational = [item for item in entries if item.get("supportLevel") in {"first-class", "conditional"}]
    unsupported = [item for item in entries if item.get("supportLevel") == "unsupported"]
    hidden = [item for item in entries if item.get("supportLevel") == "backend-capable-ui-hidden"]

    summary = {
        "sourceModules": len(source_module_set),
        "rawModules": len(modules),
        "trainerMappings": len(trainer_mapping),
        "supportEntries": len(entries),
        "operationalEntries": len(operational),
        "firstClass": sum(item.get("supportLevel") == "first-class" for item in entries),
        "conditional": sum(item.get("supportLevel") == "conditional" for item in entries),
        "hidden": len(hidden),
        "unsupported": len(unsupported),
        "unknown": sum(item.get("supportLevel") == "unknown" for item in entries),
        "errors": errors,
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--assets-root", type=Path, required=True)
    args = parser.parse_args()
    summary = validate(args.project_root.resolve(), args.assets_root.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

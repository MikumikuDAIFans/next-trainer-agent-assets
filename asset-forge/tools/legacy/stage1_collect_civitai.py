"""Bounded, anonymous Civitai Stage 1 collector.

All outputs are written below the caller-provided AgentAssets root.  The
collector intentionally keeps raw API payloads and never requests images or
model files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

API_ROOT = "https://civitai.com/api/v1"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
STRATA = {
    "sd15": "SD 1.5",
    "sd2": "SD 2.1",
    "sdxl": "SDXL 1.0",
    "flux": "Flux.1 D",
    "anima": "Anima",
    "krea2": "Krea 2",
    "lumina2": "Lumina 2",
}
PARAM_PATTERNS = {
    "rank": r"(?:rank|dim|network\s*dim)\s*[:=]?\s*(\d+)",
    "alpha": r"(?:alpha|network\s*alpha)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)",
    "batch_size": r"(?:batch(?:\s*size)?|bs)\s*[:=]?\s*(\d+)",
    "steps": r"(?:steps?|training\s*steps?)\s*[:=]?\s*([0-9][0-9,]*)",
    "epochs": r"epochs?\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)",
    "learning_rate": r"(?:learning\s*rate|lr)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?(?:e[-+]?\d+)?)",
    "resolution": r"resolution\s*[:=]?\s*(\d{3,4})(?:\s*[xX]\s*\d{3,4})?",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def request_json(url: str, proxy: str, retries: int = 3) -> tuple[int, bytes, dict[str, Any], str | None]:
    last_error: str | None = None
    for attempt in range(retries + 1):
        try:
            opener = build_opener(ProxyHandler({"http": proxy, "https": proxy}))
            req = Request(url, headers={"Accept": "application/json", "User-Agent": UA}, method="GET")
            with opener.open(req, timeout=25) as response:
                body = response.read()
                status = int(response.status)
                payload = json.loads(body.decode("utf-8"))
                return status, body, payload, None
        except Exception as exc:  # network and JSON errors are evidence
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < retries:
                time.sleep(min(2**attempt, 8))
    return 0, b"", {}, last_error


def extract_description(description: Any) -> dict[str, Any]:
    text = description if isinstance(description, str) else ""
    result: dict[str, Any] = {}
    for key, pattern in PARAM_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            result[key] = {"value": None, "source": "description", "confidence": "unknown"}
            continue
        raw = match.group(1).replace(",", "")
        value: Any = float(raw) if any(x in raw.lower() for x in (".", "e")) else int(raw)
        result[key] = {
            "value": value,
            "source": "description",
            "confidence": "low",
            "match": match.group(0),
        }
    return result


def normalize(model: dict[str, Any], retrieved_at: str, stratum: str) -> dict[str, Any]:
    versions = model.get("modelVersions") if isinstance(model.get("modelVersions"), list) else []
    latest = versions[0] if versions and isinstance(versions[0], dict) else {}
    training = latest.get("trainingDetails") if isinstance(latest.get("trainingDetails"), dict) else None
    structured = training if training is not None else None
    desc = model.get("description") or latest.get("description") or ""
    files = latest.get("files") if isinstance(latest.get("files"), list) else []
    return {
        "modelLevel": {
            "modelId": model.get("id"),
            "name": model.get("name"),
            "type": model.get("type"),
            "nsfw": model.get("nsfw"),
            "creator": (model.get("creator") or {}).get("username") if isinstance(model.get("creator"), dict) else None,
            "url": f"https://civitai.com/models/{model.get('id')}" if model.get("id") else None,
        },
        "versionLevel": {
            "modelVersionId": latest.get("id"),
            "name": latest.get("name"),
            "baseModel": latest.get("baseModel"),
            "trainedWords": latest.get("trainedWords") if isinstance(latest.get("trainedWords"), list) else [],
            "trainingDetails": structured,
            "descriptionParameters": extract_description(desc),
            "files": [
                {"name": item.get("name"), "sizeKB": item.get("sizeKB"), "type": item.get("type"), "metadata": item.get("metadata")}
                for item in files if isinstance(item, dict)
            ],
            "url": f"https://civitai.com/models/{model.get('id')}?modelVersionId={latest.get('id')}" if latest.get("id") else None,
        },
        "stratum": stratum,
        "retrievedAt": retrieved_at,
        "evidence": {"level": "L2", "source": "Civitai public API", "popularityNotTechnicalEvidence": True},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-root", required=True)
    parser.add_argument("--proxy", default="http://127.0.0.1:11809")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.limit <= 15 or not 1 <= args.workers <= 4:
        raise SystemExit("limit must be 1..15 and workers 1..4")
    root = Path(args.assets_root).resolve()
    if root.name != "AgentAssets":
        raise SystemExit("assets root must be the AgentAssets directory")
    raw_dir = root / "03_Civitai样本" / "raw"
    norm_dir = root / "03_Civitai样本" / "normalized"
    report_dir = root / "03_Civitai样本" / "reports"
    for path in (raw_dir, norm_dir, report_dir):
        path.mkdir(parents=True, exist_ok=True)
    started = now()
    requests = []
    for key, base_model in STRATA.items():
        params = {"types": "LORA", "baseModels": base_model, "sort": "Newest", "period": "AllTime", "nsfw": "false", "limit": args.limit}
        requests.append((key, f"{API_ROOT}/models?{urlencode(params)}", params))
    if len(requests) > 100:
        raise SystemExit("batch budget exceeded")
    log_path = raw_dir / "request-log.jsonl"
    normalized: list[dict[str, Any]] = []
    errors = 0
    # Requests are bounded by a small worker pool.  A short spacing before each
    # submission preserves the policy while allowing independent API latency.
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}
        for key, url, params in requests:
            time.sleep(0.5)
            futures[pool.submit(request_json, url, args.proxy)] = (key, url, params)
        with log_path.open("w", encoding="utf-8") as log:
            for future in as_completed(futures):
                key, url, params = futures[future]
                retrieved = now()
                status, body, payload, error = future.result()
                digest = hashlib.sha256(body).hexdigest() if body else None
                log.write(json.dumps({"url": url, "params": params, "stratum": key, "retrievedAt": retrieved, "status": status or None, "responseBytes": len(body), "sha256": digest, "error": error}, ensure_ascii=False) + "\n")
                if status != 200 or not isinstance(payload, dict):
                    errors += 1
                    continue
                (raw_dir / f"{key}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
                for model in payload.get("items", []) if isinstance(payload.get("items"), list) else []:
                    if isinstance(model, dict):
                        normalized.append(normalize(model, retrieved, key))
    # Model-level deduplication while retaining all version-level records.
    seen: set[Any] = set()
    deduped: list[dict[str, Any]] = []
    for record in normalized:
        model_id = record["modelLevel"].get("modelId")
        if model_id in seen:
            continue
        seen.add(model_id)
        deduped.append(record)
    norm_path = norm_dir / "model-versions.jsonl"
    with norm_path.open("w", encoding="utf-8") as handle:
        for record in normalized:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    fields = ["rank", "alpha", "batch_size", "steps", "epochs", "learning_rate", "resolution"]
    missing: dict[str, float] = {}
    for field in fields:
        known = sum(record["versionLevel"]["descriptionParameters"][field]["value"] is not None for record in normalized)
        missing[field] = round(1 - known / len(normalized), 4) if normalized else 1.0
    report = {
        "stage": "Stage 1 Phase 2/3 MVP sample",
        "startedAt": started,
        "completedAt": now(),
        "strata": STRATA,
        "requestCount": len(requests),
        "successfulResponses": len(requests) - errors,
        "failedResponses": errors,
        "versionLevelCount": len(normalized),
        "modelLevelUniqueCount": len(deduped),
        "perStratumVersionCounts": {key: sum(record["stratum"] == key for record in normalized) for key in STRATA},
        "missingnessDescriptionExtractedFields": missing,
        "structuredTrainingDetailsPresentCount": sum(record["versionLevel"]["trainingDetails"] is not None for record in normalized),
        "confidencePolicy": "description extraction is low confidence; structured trainingDetails is retained separately",
        "popularityPolicy": "download/favorite/rating fields are not used as technical correctness evidence",
        "samplingStatus": "exploratory; no stratum reaches the 8 model-level threshold from this MVP batch",
        "limits": {"batchMaxRequests": 100, "minSpacingSeconds": 0.5, "maxRetries": 3, "rawSoftLimitBytes": 500 * 1024 * 1024, "workers": args.workers},
    }
    (report_dir / "missingness-and-bias-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (report_dir / "sampling-plan.md").write_text("""# Civitai 分层采样计划\n\n本次 MVP 以 LORA 类型按 SD 1.5、SD 2.1、SDXL 1.0、Flux.1 D、Anima、Krea 2、Lumina 2 分层，每层最多 5 个最新公开模型记录。请求经 `127.0.0.1:11809`，有界并发 2，提交间隔至少 0.5 秒，最多退避重试 3 次。\n\nmodel-level 与 version-level 分开统计；本批为 exploratory，任何分层未达到 8 个独立 model-level 样本，不支撑模板参数分布。description 解析字段仅为低置信观察，结构化 `trainingDetails` 缺失原样保留。热门度字段仅用于发现，不作为技术正确性证据。\n""", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

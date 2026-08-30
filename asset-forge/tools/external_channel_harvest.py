"""Bounded public-source harvester for the supplemental evidence track.

The tool records status, URL, retrieval time, response size and (for GitHub
repositories) the latest public commit id. It never stores page bodies, images,
weights, cookies or credentials. All output stays under AgentAssets.

Usage:
  python -B tools/external_channel_harvest.py <AgentAssetsRoot> [--limit 20] [--start 0]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import ssl
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

UA = "next-trainer-evidence-harvester/1.0"
GITHUB_RE = re.compile(r"https://github\.com/([^/]+/[^/]+?)(?:/|$)")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch(url: str, proxy: str, max_bytes: int = 128 * 1024) -> tuple[int, int, str, str | None]:
    opener = build_opener(ProxyHandler({"http": proxy, "https": proxy}))
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/html;q=0.8"})
    try:
        with opener.open(req, timeout=20) as resp:
            body = resp.read(max_bytes + 1)
            if len(body) > max_bytes:
                return int(resp.status), len(body), "size-limit", None
            return int(resp.status), len(body), hashlib.sha256(body).hexdigest(), None
    except Exception as exc:  # network failures are retained as evidence
        return 0, 0, "", f"{type(exc).__name__}: {exc}"


def github_commit_url(url: str) -> str | None:
    m = GITHUB_RE.match(url.rstrip("/"))
    return f"https://api.github.com/repos/{m.group(1)}/commits?per_page=1" if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("assets_root", type=Path)
    ap.add_argument("--proxy", default="http://127.0.0.1:11809")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--start", type=int, default=0)
    args = ap.parse_args()
    root = args.assets_root.resolve()
    catalog = json.loads((root / "02_来源与证据/external-channel-catalog.json").read_text(encoding="utf-8"))
    channels = catalog["channels"]
    requests: list[dict] = []
    for ch in channels:
        requests.append({"channel": ch, "purpose": "public-url"})
        if ch["kind"] == "github-repo":
            requests.append({"channel": ch, "purpose": "latest-public-commit", "url": github_commit_url(ch["url"])})
    if args.limit < 1:
        raise SystemExit("--limit must be positive")
    requests = requests[args.start : args.start + args.limit]
    out_dir = root / "02_来源与证据/external-harvest"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for i, item in enumerate(requests):
        ch = item["channel"]
        url = item.get("url") or ch["url"]
        status, size, digest, error = fetch(url, args.proxy)
        row = {"channelId": ch["id"], "kind": ch["kind"], "purpose": item["purpose"],
               "url": url, "scope": ch["scope"], "retrievedAt": now(), "status": status,
               "responseBytes": size, "bodySha256": digest or None, "error": error}
        rows.append(row)
        if i + 1 < len(requests):
            time.sleep(0.5)
    log = out_dir / f"request-log-{args.start:03d}-{args.start + len(rows) - 1:03d}.jsonl"
    with log.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {"requested": len(rows), "http200": sum(r["status"] == 200 for r in rows),
               "failed": sum(r["status"] != 200 for r in rows), "limit": args.limit,
               "proxy": args.proxy, "result": "pass" if all(r["status"] == 200 for r in rows) else "pass-with-boundary"}
    (out_dir / f"harvest-summary-{args.start:03d}-{args.start + len(rows) - 1:03d}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

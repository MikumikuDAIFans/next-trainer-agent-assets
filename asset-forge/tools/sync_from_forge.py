# -*- coding: utf-8 -*-
"""One-way asset sync: asset-forge mirror -> official repo assets.

Contract (user ruling 2026-08-30):
  * The ONLY data sources are ``asset-forge/assets/knowledge/``,
    ``asset-forge/assets/templates/``, ``asset-forge/assets/eval/`` and
    ``asset-forge/sync/sync-manifest.json``. Nothing else is ever read.
  * The ONLY write targets are the same three prefixes under ``assets/``
    in the repo root (path-traversal guarded).
  * Direction is strictly forge -> official. The official tree is never
    read back into the forge; the forge mirror is only produced by the
    collection/governance stages, never by edits to official assets.
  * Every sync run requires a human review and an explicit confirmation:
    pass ``--confirmed-by-user "<what the human approved>"``. Without it
    the tool is a dry-run planner and writes NOTHING.
  * Fail-closed integrity: each source file's sha256 must equal the
    manifest pin before anything is applied, and each applied target is
    re-verified against the same pin afterwards.
  * ``create`` never overwrites: an existing target with identical bytes
    is skipped (idempotent); a differing existing target aborts the run.
  * ``append`` (jsonl) appends only rows whose id is absent; ids that
    partially exist abort the run (no silent duplication).

Usage:
    python tools/sync_from_forge.py                 # dry-run plan only
    python tools/sync_from_forge.py --confirmed-by-user "2026-08-30 用户批准同步 91 项"
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORGE = os.path.dirname(HERE)                       # asset-forge/
REPO = os.path.dirname(FORGE)                       # agent-assets/
MANIFEST = os.path.join(FORGE, "sync", "sync-manifest.json")
RUNS_DIR = os.path.join(FORGE, "sync", "sync-runs")
ALLOWED_PREFIXES = ("assets/knowledge/", "assets/templates/", "assets/eval/")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(rel, root):
    """root + rel with traversal guard; returns abspath or None."""
    ap = os.path.normpath(os.path.join(root, rel.replace("/", os.sep)))
    if not ap.startswith(os.path.normpath(root) + os.sep):
        return None
    return ap


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as fh:
        man = json.load(fh)
    problems = []
    for i, op in enumerate(man.get("operations", [])):
        for field in ("op", "source", "target", "sha256", "kind"):
            if field not in op:
                problems.append("op %d missing field %s" % (i, field))
        tgt = op.get("target", "").replace("\\", "/")
        if not tgt.startswith(ALLOWED_PREFIXES):
            problems.append("op %d target outside whitelist: %s" % (i, tgt))
        src = op.get("source", "").replace("\\", "/")
        if not src.startswith(ALLOWED_PREFIXES):
            problems.append("op %d source outside whitelist: %s" % (i, src))
        if op.get("op") not in ("create", "append"):
            problems.append("op %d unsupported op: %s" % (i, op.get("op")))
    if problems:
        raise SystemExit("manifest rejected:\n  " + "\n  ".join(problems))
    return man


def plan_and_apply(man, apply, confirmation):
    actions, errors = [], []
    for op in man["operations"]:
        src = resolve(op["source"], FORGE)
        tgt = resolve(op["target"], REPO)
        if src is None or tgt is None:
            errors.append("path escape rejected: %s" % op["source"])
            continue
        entry = {"op": op["op"], "source": op["source"], "target": op["target"],
                 "kind": op["kind"]}
        if op.get("reconstruction"):
            entry["reconstruction"] = op["reconstruction"]

        if not os.path.isfile(src):
            errors.append("source missing: %s" % op["source"])
            continue
        if op["op"] == "create":
            digest = sha256_file(src)
            if digest != op["sha256"]:
                errors.append("source hash mismatch (refusing): %s" % op["source"])
                continue
            if os.path.isfile(tgt):
                if sha256_file(tgt) == op["sha256"]:
                    entry["action"] = "skip-identical"
                    actions.append(entry)
                    continue
                errors.append("target exists with DIFFERENT bytes (refusing to "
                              "overwrite): %s" % op["target"])
                continue
            entry["action"] = "write"
            if apply:
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                with open(src, "rb") as fin, open(tgt, "wb") as fout:
                    fout.write(fin.read())
                if sha256_file(tgt) != op["sha256"]:
                    errors.append("post-write verification FAILED: %s" % op["target"])
                    continue
            actions.append(entry)
        else:  # append (jsonl, idempotent by row id)
            rows = [json.loads(l) for l in
                    open(src, encoding="utf-8").read().splitlines() if l.strip()]
            ids = [r.get("id") for r in rows]
            if op.get("rowIds") is not None and ids != op["rowIds"]:
                errors.append("append row ids differ from manifest: %s" % op["source"])
                continue
            if op.get("sha256") and sha256_file(src) != op["sha256"]:
                errors.append("append source hash mismatch: %s" % op["source"])
                continue
            have = []
            if os.path.isfile(tgt):
                have = [json.loads(l).get("id") for l in
                        open(tgt, encoding="utf-8").read().splitlines() if l.strip()]
            overlap = sorted(set(have) & set(ids))
            if overlap:
                if set(overlap) == set(ids) and have:
                    entry["action"] = "skip-all-ids-present"
                    actions.append(entry)
                    continue
                errors.append("append ids partially present (refusing): %s -> %s"
                              % (op["source"], ",".join(overlap[:5])))
                continue
            entry["action"] = "append-%d-rows" % len(rows)
            if apply:
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                with open(tgt, "a", encoding="utf-8", newline="\n") as fh:
                    for r in rows:
                        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                after = [json.loads(l).get("id") for l in
                         open(tgt, encoding="utf-8").read().splitlines() if l.strip()]
                if not set(ids) <= set(after):
                    errors.append("post-append verification FAILED: %s" % op["target"])
                    continue
            actions.append(entry)
    return actions, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--confirmed-by-user", default="",
                    help="required human confirmation statement; empty = dry-run")
    args = ap.parse_args()

    man = load_manifest()
    apply_run = bool(args.confirmed_by_user.strip())
    actions, errors = plan_and_apply(man, apply_run, args.confirmed_by_user)

    mode = "APPLIED" if apply_run else "DRY-RUN"
    counts = {}
    for a in actions:
        key = a["action"].split("-")[0]
        counts[key] = counts.get(key, 0) + 1
    print("[%s] manifest ops=%d -> %s" % (mode, len(man["operations"]),
                                          json.dumps(counts)))
    for a in actions:
        print("  %-8s %-9s %s" % (a["action"], a["kind"], a["target"]))
    for e in errors:
        print("ERROR: " + e)

    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record = {
        "run": stamp,
        "mode": "applied" if apply_run else "dry-run",
        "confirmedByUser": args.confirmed_by_user or None,
        "manifest": {k: man.get(k) for k in ("schemaVersion", "generatedAt")},
        "counts": counts,
        "actions": actions,
        "errors": errors,
    }
    if apply_run:
        os.makedirs(RUNS_DIR, exist_ok=True)
        out = os.path.join(RUNS_DIR, "run-%s.json" % stamp)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)
        print("run log: " + os.path.relpath(out, REPO))
    if errors:
        return 2
    if not apply_run:
        print("nothing written (human confirmation required: --confirmed-by-user)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

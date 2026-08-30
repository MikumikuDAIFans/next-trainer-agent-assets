# /// script
# requires-python = ">=3.11"
# ///
"""Build the dual-platform (win32-x64 + linux-x64) local/test marketplace
catalog + trust root (Goal v9 / Linux 适配).

Reads both platform zips from dist-marketplace/packages/, binds each to its
platform via the entry's `packages` list (flat fields stay the win32-x64
binding for legacy readers), signs everything with the release key (trust v1
HMAC or trust v2 Ed25519 key file; falls back to the dev HMAC key), and
self-checks every binding with the host's own validators. An ed25519 run
emits a PUBLIC-key-only v2 trust.json: clients verify, they cannot forge.

NOTE: the `packages` field requires a host with the dual-platform catalog
schema; single-platform hosts parse the entry with extra="forbid" and must
keep using single-platform catalogs.

Run with the project venv:
  .venv-dev\\Scripts\\python.exe plugin-packages\\next-trainer-pi-agent\\scripts\\build-marketplace-catalog.py
"""
from __future__ import annotations

import argparse
import hashlib
import hmac as hmac_module
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

PKG_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PKG_ROOT.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

VERSION = "0.3.8"
PLUGIN_ID = "next-trainer-pi-agent"
PUBLISHER = "next-trainer-project"
HOST_COMPAT = ">=2.9.2 <4.0.0"
PLATFORMS = ["win32-x64", "linux-x64"]
SIGNING_KEY_ID = "dev-local-signing"
SIGNING_KEY_HEX = "6e6578742d747261696e65722d6c6f63616c2d746573742d7369676e696e672d6b6579"
IN_DIR = PKG_ROOT / "dist-marketplace"
OUT_DIR = PKG_ROOT / "dist-marketplace"

MAX_PACKAGE_BYTES = 1024 * 1024 * 1024
MAX_UNPACKED_BYTES = 4 * 1024 * 1024 * 1024
MAX_FILES = 300_000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hmac_sign(key: bytes, payload: bytes) -> str:
    return hmac_module.new(key, payload, hashlib.sha256).hexdigest()


def _ed25519_sign(secret_seed: bytes, payload: bytes) -> str:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    return Ed25519PrivateKey.from_private_bytes(secret_seed).sign(payload).hex()


def _ed25519_public_hex(secret_seed: bytes) -> str:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private = Ed25519PrivateKey.from_private_bytes(secret_seed)
    return private.public_key().public_bytes_raw().hex()


class _Signer:
    """Key + algorithm resolved once; the emitted trust.json mirrors it.

    trust v1: HMAC secret key (keyHex) — symmetric, ships the SECRET to every
    client (the C-2 exposure). trust v2: Ed25519 — the release machine holds
    the private seed, clients receive ONLY the public key. A shipped v2
    trust.json grants verification, never signing power.
    """

    def __init__(self, key_id: str, algorithm: str, secret: bytes | None, public_hex: str | None, key_hex: str | None):
        self.key_id = key_id
        self.algorithm = algorithm
        self._secret = secret
        self.public_hex = public_hex
        self.key_hex = key_hex

    def sign(self, payload: bytes) -> str:
        if self.algorithm == "ed25519":
            return _ed25519_sign(self._secret, payload)
        return _hmac_sign(self._secret, payload)

    def trust_record(self) -> dict:
        if self.algorithm == "ed25519":
            return {"publisherId": PUBLISHER, "algorithm": "ed25519", "publicKeyHex": self.public_hex}
        return {"publisherId": PUBLISHER, "keyHex": self.key_hex}

    def store_key(self) -> tuple:
        if self.algorithm == "ed25519":
            return (PUBLISHER, bytes.fromhex(self.public_hex), "ed25519")
        return (PUBLISHER, self._secret)


def _resolve_signer(args) -> _Signer:
    """CLI pair > MIKAZUKI_RELEASE_SIGNING_* env > key file > dev default.

    Key file shapes (always OUTSIDE every git repository):
      {"keyId": str, "keyHex": <hex>}                                  — v1 HMAC
      {"keyId": str, "algorithm": "ed25519", "privateKeyHex": <64hex>} — v2 seed
    """
    signing_key_id = args.signing_key_id or os.environ.get("MIKAZUKI_RELEASE_SIGNING_KEY_ID", "").strip()
    signing_key_hex = (
        args.signing_key_hex or os.environ.get("MIKAZUKI_RELEASE_SIGNING_KEY_HEX", "").strip()
    ).casefold()
    if not (signing_key_id or signing_key_hex):
        key_file = args.signing_key_file or os.environ.get("MIKAZUKI_RELEASE_SIGNING_FILE", "").strip()
        if key_file:
            payload = json.loads(Path(key_file).read_text(encoding="utf-8"))
            algorithm = str(payload.get("algorithm") or "hmac-sha256")
            if algorithm == "ed25519":
                seed_hex = str(payload.get("privateKeyHex") or "").casefold()
                if not re.fullmatch(r"[0-9a-f]{64}", seed_hex):
                    raise SystemExit("ed25519 signing key file requires privateKeyHex (32-byte hex seed)")
                seed = bytes.fromhex(seed_hex)
                public_hex = _ed25519_public_hex(seed)
                print(f"[signing] ed25519 key file: {key_file} (public key {public_hex[:16]}…)")
                return _Signer(str(payload["keyId"]), "ed25519", seed, public_hex, None)
            if algorithm != "hmac-sha256":
                raise SystemExit(f"signing key file algorithm not supported: {algorithm}")
            signing_key_id = str(payload["keyId"])
            signing_key_hex = str(payload["keyHex"]).casefold()
            print(f"[signing] key loaded from file: {key_file}")
    if (signing_key_id and not signing_key_hex) or (signing_key_hex and not signing_key_id):
        raise SystemExit("release signing requires BOTH --signing-key-id and --signing-key-hex (or the MIKAZUKI_RELEASE_SIGNING_* env pair)")
    if signing_key_id and signing_key_hex:
        if not re.fullmatch(r"[0-9a-f]{32,}", signing_key_hex):
            raise SystemExit("--signing-key-hex must be 64+ hex characters (>=32 bytes)")
        print(f"[signing] release key: {signing_key_id} (hmac-sha256)")
        return _Signer(signing_key_id, "hmac-sha256", bytes.fromhex(signing_key_hex), None, signing_key_hex)
    if args.remote_base:
        print(
            "[signing] WARNING: --remote-base catalog signed with the DEV key. "
            "Use the release signing key file for public distribution.",
            file=sys.stderr,
        )
    return _Signer(SIGNING_KEY_ID, "hmac-sha256", bytes.fromhex(SIGNING_KEY_HEX), None, SIGNING_KEY_HEX)


def _host_version() -> str:
    try:
        return (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip() or "0.0.0"
    except OSError:
        return "0.0.0"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--remote-base",
        default=None,
        help=(
            "Base URL for real distribution (e.g. "
            "https://github.com/<owner>/<repo>/releases/download/v0.3.2). "
            "When set, catalog URLs become <base>/<file> instead of the "
            "dev-local placeholder; requires a public HTTPS host."
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Write catalog.json/trust.json here instead of dist-marketplace/ (zip inputs are still read from dist-marketplace/packages/).",
    )
    parser.add_argument(
        "--signing-key-id",
        default=None,
        help="Release signing key id (default: dev-local-signing). Also MIKAZUKI_RELEASE_SIGNING_KEY_ID.",
    )
    parser.add_argument(
        "--signing-key-hex",
        default=None,
        help=(
            "Release signing HMAC key, 64+ hex chars (generate with "
            "python -c \"import secrets; print(secrets.token_hex(32))\"). "
            "Keep it OUT of the repository; the matching trust.json ships "
            "inside the release package only. Also MIKAZUKI_RELEASE_SIGNING_KEY_HEX."
        ),
    )
    parser.add_argument(
        "--signing-key-file",
        default=None,
        help=(
            "JSON {\"keyId\":..., \"keyHex\":...} stored OUTSIDE every git repository "
            "(workspace .release-signing/signing-key.json by convention). Resolution "
            "priority: CLI pair > MIKAZUKI_RELEASE_SIGNING_* env > this file / "
            "MIKAZUKI_RELEASE_SIGNING_FILE > the built-in dev key."
        ),
    )
    parser.add_argument(
        "--trust-extra-keys-file",
        default=None,
        help=(
            "JSON file (same {keys:{id:{publisherId,keyHex}}} shape) of ADDITIONAL "
            "keys to merge into the emitted trust.json. Used once per key rotation "
            "to ship a dual-key transition trust root so hosts pinned on the old "
            "key keep verifying while operators migrate their catalog/trust files."
        ),
    )
    args = parser.parse_args(argv)
    remote_base = args.remote_base.rstrip("/") if args.remote_base else None
    if remote_base is not None:
        parsed = urlsplit(remote_base)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise SystemExit("--remote-base must be a plain HTTPS base URL")
    global OUT_DIR, SIGNING_KEY_ID, SIGNING_KEY_HEX
    if args.out_dir:
        OUT_DIR = Path(args.out_dir).resolve()
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    signer = _resolve_signer(args)
    SIGNING_KEY_ID = signer.key_id

    from mikazuki.plugin_marketplace.models import MarketplaceCatalog, MarketplaceEntry
    from mikazuki.plugin_marketplace.package import PackageLimits, inspect_package, validate_manifest_entry
    from mikazuki.plugin_marketplace.trust import TrustStore, canonical_catalog_payload, canonical_entry_payload

    zips = {platform: IN_DIR / "packages" / f"{PLUGIN_ID}-{VERSION}-{platform}.zip" for platform in PLATFORMS}
    for platform, path in zips.items():
        if not path.is_file():
            raise SystemExit(f"missing platform package: {path}")

    sizes = {platform: path.stat().st_size for platform, path in zips.items()}
    shas = {platform: sha256_file(path) for platform, path in zips.items()}
    for platform, size in sizes.items():
        if size > MAX_PACKAGE_BYTES:
            raise SystemExit(f"{platform} package size {size} exceeds limit {MAX_PACKAGE_BYTES}")

    urls = {
        platform: (
            f"{remote_base}/{PLUGIN_ID}-{VERSION}-{platform}.zip"
            if remote_base
            else f"https://plugins.next-trainer.local/packages/{PLUGIN_ID}-{VERSION}-{platform}.zip"
        )
        for platform in PLATFORMS
    }
    # Flat fields carry the win32-x64 binding (legacy readers + display).
    primary = "win32-x64"

    # permissions_summary is DERIVED from the packaged manifest itself. The
    # host's validate_manifest_entry demands an EXACT match between the
    # catalog entry and the manifest inside the zip — hardcoding the list a
    # second time here was pure drift bait, now structurally impossible.
    import zipfile as _zipfile

    with _zipfile.ZipFile(zips[primary]) as archive:
        packaged_manifest = json.loads(archive.read("plugin.json").decode("utf-8"))
    packaged_permissions = list(packaged_manifest.get("permissions") or [])
    if not packaged_permissions:
        raise SystemExit("packaged plugin.json carries no permissions — refusing to build a catalog that cannot install")
    print(f"[manifest] permissions from packaged plugin.json: {packaged_permissions}")

    entry = MarketplaceEntry(
        id=PLUGIN_ID,
        name="Next Trainer Agent",
        publisher_id=PUBLISHER,
        description=(
            "Next Trainer Agent embedded as a loopback server and opened in the cross-page "
            "floating dialog. Ships win32-x64 and linux-x64 packages (local/test catalog)."
        ),
        icon=None,
        latest_version=VERSION,
        channel="stable",
        host_compatibility=HOST_COMPAT,
        platforms=PLATFORMS,
        package_size=sizes[primary],
        permissions_summary=packaged_permissions,
        license="MIT",
        release_notes_url=None,
        package_url=urls[primary],
        sha256=shas[primary],
        signature="",
        signing_key_id=signer.key_id,
        published_at=datetime.now(timezone.utc).replace(microsecond=0),
        packages=[
            {"platform": platform, "package_url": urls[platform], "package_size": sizes[platform], "sha256": shas[platform]}
            for platform in PLATFORMS
        ],
    )
    entry.signature = signer.sign(canonical_entry_payload(entry))

    catalog = MarketplaceCatalog(
        schema_version=1,
        publisher_id=PUBLISHER,
        signing_key_id=signer.key_id,
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        entries=[entry],
        signature="",
    )
    catalog.signature = signer.sign(canonical_catalog_payload(catalog))

    (OUT_DIR / "catalog.json").write_text(
        json.dumps(catalog.model_dump(mode="json", by_alias=True), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    trust_keys = {signer.key_id: signer.trust_record()}
    if args.trust_extra_keys_file:
        extra = json.loads(Path(args.trust_extra_keys_file).read_text(encoding="utf-8"))
        for kid, rec in (extra.get("keys") or {}).items():
            if "publicKeyHex" in rec:
                trust_keys.setdefault(str(kid), {
                    "publisherId": str(rec["publisherId"]),
                    "algorithm": str(rec.get("algorithm") or "ed25519"),
                    "publicKeyHex": str(rec["publicKeyHex"]).casefold(),
                })
            elif signer.algorithm == "ed25519":
                raise SystemExit(
                    f"refusing to merge HMAC key material ({kid}) into an ed25519 trust root: "
                    "trust v2 ships public keys only — legacy migration is not a reason to re-ship secrets"
                )
            else:
                trust_keys.setdefault(str(kid), {"publisherId": str(rec["publisherId"]), "keyHex": str(rec["keyHex"]).casefold()})
    (OUT_DIR / "trust.json").write_text(
        json.dumps(
            {
                "schemaVersion": 2 if signer.algorithm == "ed25519" else 1,
                "keys": trust_keys,
                "revokedKeys": [],
                "note": (
                    "Key rotation transition trust root: both the active release key and the predecessor key verify; revoke the old key id after all operators migrated."
                    if len(trust_keys) > 1
                    else (
                        f"Release trust root (Ed25519 key {signer.key_id}): PUBLIC key only — "
                        "the private seed never leaves the release operator's key file."
                        if signer.algorithm == "ed25519"
                        else (
                            f"Release trust root (key {signer.key_id}). The signing key is held by the release operator and never committed to the repository."
                            if signer.key_id != "dev-local-signing"
                            else (
                                "Release trust root (dev HMAC key) for remote-distribution catalogs."
                                if remote_base
                                else "Development/test trust root only. Production signing is release-governed."
                            )
                        )
                    )
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if remote_base:
        print(f"[catalog] remote base URL: {remote_base}")

    # Self-check every platform binding with the host's own validators.
    limits = PackageLimits(
        max_package_bytes=MAX_PACKAGE_BYTES,
        max_unpacked_bytes=MAX_UNPACKED_BYTES,
        max_files=MAX_FILES,
    )
    trust = TrustStore({signer.key_id: signer.store_key()})
    for platform in PLATFORMS:
        manifest, _members = inspect_package(zips[platform], limits)
        validate_manifest_entry(manifest, entry, platform=platform)
        url, size, sha = entry.resolve_platform_package(platform)
        trust.verify(entry, zips[platform], package_size=size, sha256=sha)
        trust.verify_compatibility(entry, host_version=_host_version(), platform=platform)
        assert url == urls[platform]
        print(f"[self-check] {platform}: inspect + manifest + trust verify + compatibility: PASS")
    trust.verify_catalog(catalog)
    print("[self-check] catalog signature: PASS")

    print(json.dumps(
        {
            "catalog": str(OUT_DIR / "catalog.json"),
            "trust": str(OUT_DIR / "trust.json"),
            "packages": {
                platform: {"zip": str(zips[platform]), "bytes": sizes[platform], "sha256": shas[platform]}
                for platform in PLATFORMS
            },
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

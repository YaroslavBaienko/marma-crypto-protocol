#!/usr/bin/env python3
"""
Marma-Crypto Deal-Room Batch Engine & REST Microservice (`v2.1`)
================================================================
Provides:
1. `batch_seal_dealroom()`: High-throughput $O(1)$-amortized batch stamping of $N$
   recipient-tracked copies for M&A / Virtual Data Rooms (Intralinks, Datasite,
   Nextcloud, SharePoint) supporting any emblem (`sri-yantra`, `tryzub`,
   `corporate-shield`, `cad-polygon`) and optional 32-Sector Optical Lotus Ring.
2. Zero-dependency HTTP REST server (`MarmaDealRoomServer`) + in-process `MarmaAPIClient`
   (and optional FastAPI app adapter) exposing:
   - `GET  /v1/health`
   - `POST /v1/seal-batch`
   - `POST /v1/verify`
   - `POST /v1/trace-leak` (supports both vector PDF/DOCX/SVG and raster PNG/JPG screen photos)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import sqlite3
import threading
import time
from contextlib import closing
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener, urlopen

import pymupdf

from marma_watermark import (
    DEFAULT_SECRET,
    SEAL_PAGES_DEFAULT,
    compute_canary_tag,
    compute_public_seal_digest,
    derive_micro_offsets,
    normalize_text,
    pdf_visible_seal_check,
    resolve_seal_pages,
    seal_pages_label,
    trace_canary_suspects,
    verify_any_file,
)
from .optical_ecc import draw_optical_lotus_ring_pdf, extract_canary_from_raster_image
from .universal_qim import (
    SUPPORTED_EMBLEMS,
    build_perturbed_emblem_v21,
    recover_256bit_from_emblem_v21,
    verify_emblem_coordinates_v21,
)

API_VERSION = "2.3.0"


# ==============================================================================
# 1. UNIVERSAL + OPTICAL PDF STAMPING & VERIFICATION
# ==============================================================================
def stamp_pdf_universal_v21(
    in_pdf: Path,
    out_pdf: Path,
    secret_key: str = DEFAULT_SECRET,
    recipient_id: str = "",
    emblem_type: str = "sri-yantra",
    optical_ring: bool = True,
    mode: str = "both",
    signer_key_name: str = "Sovereign-Vedic-Key-108",
    key_fingerprint: str = "",
    precomputed_crypto: dict[str, Any] | None = None,
    seal_pages: str | None = None,
) -> dict[str, Any]:
    """
    Stamp a PDF with any supported vector emblem (`sri-yantra`, `tryzub`,
    `corporate-shield`, `cad-polygon`) and optional 32-Sector Optical Lotus Ring.
    Supports `precomputed_crypto` so batch Deal-Room sealing computes the document
    digest and DSTU 4145-2002 signature only once across N recipients.
    """
    if not key_fingerprint:
        key_fingerprint = hashlib.sha256(secret_key.encode("utf-8")).hexdigest()

    doc = pymupdf.open(str(in_pdf))
    if mode in ("watermark", "stealth"):
        seal_spec = "none"; seal_page_list = []
    else:
        seal_spec = (seal_pages or os.environ.get("MARMA_SEAL_PAGES") or SEAL_PAGES_DEFAULT).strip().lower()
        seal_page_list = resolve_seal_pages(seal_spec, len(doc))
        seal_spec = seal_pages_label(seal_page_list, len(doc)) if seal_page_list else "none"
    if precomputed_crypto:
        content_hash = precomputed_crypto["content_hash"]
        hex_sig = precomputed_crypto["hex_sig"]
        dstu_bundle = precomputed_crypto["dstu_bundle"]
    else:
        full_text = "\n".join(normalize_text(page.get_text("text")) for page in doc)
        content_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        payload = f"PDF-CONTENT-SHA256::{content_hash}"
        hex_sig, _, dstu_bundle = derive_micro_offsets(payload, secret_key)

    canary_info = compute_canary_tag(secret_key, content_hash, recipient_id, key_fingerprint)
    beacon_word = int(canary_info.get("beacon_word", 0))

    perturbed = build_perturbed_emblem_v21(
        hex_sig,
        emblem_type=emblem_type,
        canary_beacon_word=beacon_word,
        cx=150.0,
    )
    pub_seal = compute_public_seal_digest(content_hash, hex_sig, key_fingerprint, perturbed)

    optical_codeword: list[int] = []
    for page_idx, page in enumerate(doc):
        rect = page.rect
        w, h = rect.width, rect.height

        # A0. Stealth mode (0% opacity invisible vector carrier on first page)
        if (mode == "stealth" or seal_spec == "none") and mode != "watermark" and page_idx == 0:
            shape_st = page.new_shape()
            scale_st = min(w, h) * 0.62 / 300.0
            cx_st, cy_st = w / 2.0, h / 2.0

            def map_st(x: float, y: float) -> pymupdf.Point:
                return pymupdf.Point(cx_st + (x - 150.0) * scale_st, cy_st + (y - 150.0) * scale_st)

            for t in perturbed:
                p1 = map_st(t["lx"], t["by"])
                p2 = map_st(150.0, t["ay"])
                p3 = map_st(t["rx"], t["by"])
                shape_st.draw_polyline([p1, p2, p3, p1])
            shape_st.finish(color=(0.50, 0.50, 0.50), width=0.0, stroke_opacity=0.0)
            shape_st.commit(overlay=True)

        # A. Full-page vector background watermark
        if mode == "watermark" or (mode == "both" and seal_spec != "none"):
            shape_bg = page.new_shape()
            scale_bg = min(w, h) * 0.62 / 300.0
            cx_bg, cy_bg = w / 2.0, h / 2.0

            def map_bg(x: float, y: float) -> pymupdf.Point:
                return pymupdf.Point(cx_bg + (x - 150.0) * scale_bg, cy_bg + (y - 150.0) * scale_bg)

            shape_bg.draw_circle(map_bg(150.0, 150.0), 100.0 * scale_bg)
            shape_bg.draw_circle(map_bg(150.0, 150.0), 122.0 * scale_bg)
            for t in perturbed:
                p1 = map_bg(t["lx"], t["by"])
                p2 = map_bg(150.0, t["ay"])
                p3 = map_bg(t["rx"], t["by"])
                shape_bg.draw_polyline([p1, p2, p3, p1])
            shape_bg.finish(color=(0.76, 0.60, 0.22), width=0.65, stroke_opacity=0.075)
            shape_bg.commit(overlay=True)

        # B. Corner Golden Authorship Seal (+ Optional 32-Sector Optical Lotus Ring)
        if mode in ("seal", "both") and page_idx in seal_page_list:
            seal_r = 42.0 if optical_ring else 34.0
            cx_s = w - 64.0
            cy_s = h - 64.0
            scale_s = (seal_r * 2.0) / 300.0

            def map_seal(x: float, y: float) -> pymupdf.Point:
                return pymupdf.Point(cx_s + (x - 150.0) * scale_s, cy_s + (y - 150.0) * scale_s)

            shape_s = page.new_shape()
            disc_mult = 0.86
            shape_s.draw_circle(pymupdf.Point(cx_s, cy_s), seal_r * disc_mult)
            shape_s.finish(
                color=(0.72, 0.54, 0.14),
                fill=(0.04, 0.06, 0.11),
                width=0.9,
                fill_opacity=0.96,
                stroke_opacity=0.95,
            )
            shape_s.commit(overlay=True)

            if optical_ring:
                optical_codeword = draw_optical_lotus_ring_pdf(
                    page, cx_s, cy_s, scale_s, beacon_word, content_sha256=content_hash
                )

            shape_tri = page.new_shape()
            shape_tri.draw_circle(map_seal(150.0, 150.0), 100.0 * scale_s)
            for t in perturbed:
                p1 = map_seal(t["lx"], t["by"])
                p2 = map_seal(150.0, t["ay"])
                p3 = map_seal(t["rx"], t["by"])
                shape_tri.draw_polyline([p1, p2, p3, p1])
            shape_tri.finish(color=(0.95, 0.80, 0.38), width=0.58, stroke_opacity=0.95)
            shape_tri.commit(overlay=True)

            shape_b = page.new_shape()
            shape_b.draw_circle(map_seal(150.0, 156.4308), 1.4)
            shape_b.finish(color=(1.0, 0.9, 0.6), fill=(0.95, 0.18, 0.22), width=0.3)
            shape_b.commit(overlay=True)


    seal_packet = {
        "protocol": "MARMA-DSTU4145-V1.3",
        "marma_v21_emblem": emblem_type,
        "optical_ring": optical_ring,
        "marma_bits": 256,
        "signer_key_name": signer_key_name,
        "key_fingerprint": key_fingerprint,
        "content_sha256": content_hash,
        "hmac_sha256": hex_sig,
        "public_seal_digest": pub_seal,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dstu4145": dstu_bundle,
        "canary": canary_info if canary_info.get("enabled") else {"enabled": False, "beacon_word": 0},
        "seal_pages": seal_spec,
        "seal_page_indices": seal_page_list,
        "triangles": [{k: t[k] for k in ("name", "lx", "by", "ay", "rx")} for t in perturbed],
    }
    meta = doc.metadata or {}
    meta["keywords"] = "MARMA_SEAL::" + json.dumps(seal_packet, separators=(",", ":"))
    doc.set_metadata(meta)
    doc.save(str(out_pdf))
    doc.close()

    return {
        "format": "pdf",
        "protocol": "MARMA-DSTU4145-V1.3",
        "emblem_type": emblem_type,
        "optical_ring": optical_ring,
        "optical_codeword_bits": len(optical_codeword),
        "input_file": str(in_pdf),
        "output_file": str(out_pdf),
        "recipient_id": recipient_id,
        "content_sha256": content_hash,
        "hmac_sha256": hex_sig,
        "canary": canary_info,
    }


def verify_pdf_universal_v21(
    pdf_path: Path,
    secret_key: str = DEFAULT_SECRET,
    recipient_id: str = "",
) -> dict[str, Any]:
    """Verify a PDF stamped with any supported emblem (`sri-yantra`, `tryzub`, `corporate-shield`, `cad-polygon`)."""
    doc = pymupdf.open(str(pdf_path))
    meta = doc.metadata or {}
    kw = meta.get("keywords", "")
    full_text = "\n".join(normalize_text(page.get_text("text")) for page in doc)
    doc.close()

    if "MARMA_SEAL::" not in kw:
        return {"verified": False, "file": str(pdf_path), "reason": "No MARMA_SEAL metadata found"}

    pkt = json.loads(kw.split("MARMA_SEAL::", 1)[1])
    emblem_type = pkt.get("marma_v21_emblem", "sri-yantra")
    if emblem_type == "sri-yantra":
        res = verify_any_file(pdf_path, secret_key=secret_key, recipient_id=recipient_id)
        res["emblem_type"] = "sri-yantra"
        res["optical_ring"] = bool(pkt.get("optical_ring", False))
        return res

    content_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
    embedded_csha = pkt.get("content_sha256", "")
    embedded_hmac = pkt.get("hmac_sha256", "")
    key_fp = pkt.get("key_fingerprint", "")
    canary_pkt = pkt.get("canary") or {}
    embedded_canary = int(canary_pkt.get("beacon_word", 0))
    contours = pkt.get("triangles", [])

    rec_hex, rec_canary = recover_256bit_from_emblem_v21(contours, emblem_type=emblem_type, cx=150.0)
    max_drift, max_sym = verify_emblem_coordinates_v21(
        contours,
        emblem_type=emblem_type,
        cx=150.0,
        expected_hex=embedded_hmac,
        canary_beacon_word=embedded_canary,
    )
    content_ok = content_hash == embedded_csha
    bijective_ok = (rec_hex == embedded_hmac) and (rec_canary == embedded_canary)
    visible = {"ok": None, "seal_pages": pkt.get("seal_pages"), "missing_pages": []}
    if pkt.get("seal_pages") == "none":
        visible = {"ok": True, "seal_pages": "none", "missing_pages": []}
    elif pkt.get("seal_pages") and pkt.get("seal_pages") not in ("none", "watermark"):
        try:
            visible = pdf_visible_seal_check(pdf_path, pkt["seal_pages"])
        except ValueError as exc:
            visible = {"ok": False, "seal_pages": pkt.get("seal_pages"), "missing_pages": [], "error": str(exc)}
    verified = content_ok and bijective_ok and (max_drift < 1e-8) and (max_sym < 1e-8) and visible.get("ok") is not False

    canary_match = None
    if recipient_id:
        cand = compute_canary_tag(secret_key, content_hash, recipient_id, key_fp)
        canary_match = bool(rec_canary > 0 and rec_canary == cand["beacon_word"])

    return {
        "verified": verified,
        "reason": "OK" if verified else (
            f"Visible seal missing on page(s) {visible.get('missing_pages')}" if visible.get("ok") is False
            else "Integrity or coordinate mismatch"),
        "format": "pdf",
        "protocol": pkt.get("protocol", "MARMA-DSTU4145-V1.3"),
        "emblem_type": emblem_type,
        "optical_ring": bool(pkt.get("optical_ring", False)),
        "file": str(pdf_path),
        "content_matches": content_ok,
        "bijective_256bit_match": bijective_ok,
        "recovered_256bit_digest": rec_hex,
        "embedded_hmac_sha256": embedded_hmac,
        "computed_content_sha256": content_hash,
        "key_fingerprint": key_fp,
        "canary_active": bool(rec_canary > 0),
        "canary_beacon_word": rec_canary,
        "canary_recipient_verified": canary_match,
        "max_coordinate_signature_drift": round(max_drift, 10),
        "max_bilateral_symmetry_error": round(max_sym, 12),
        "seal_pages": visible.get("seal_pages"),
        "visible_seal_ok": visible.get("ok"),
        "visible_seal_missing_pages": visible.get("missing_pages", []),
    }


# ==============================================================================
# 2. HIGH-THROUGHPUT DEAL-ROOM BATCH SEALING ENGINE
# ==============================================================================
def batch_seal_dealroom(
    in_pdf: Path,
    out_dir: Path,
    recipients: list[str],
    secret_key: str = DEFAULT_SECRET,
    emblem_type: str = "sri-yantra",
    optical_ring: bool = True,
    mode: str = "both",
    signer_key_name: str = "Sovereign-Vedic-Key-108",
    seal_pages: str | None = None,
) -> dict[str, Any]:
    """
    Generate $N$ individualized recipient-watermarked copies of `in_pdf` in `out_dir`.
    Precomputes the document SHA-256 and base DSTU 4145-2002 / HMAC signature once,
    achieving sub-150ms performance for 10+ Deal-Room recipients.
    """
    t0 = time.perf_counter()
    out_dir.mkdir(parents=True, exist_ok=True)
    key_fingerprint = hashlib.sha256(secret_key.encode("utf-8")).hexdigest()

    doc = pymupdf.open(str(in_pdf))
    full_text = "\n".join(normalize_text(page.get_text("text")) for page in doc)
    doc.close()
    content_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
    payload = f"PDF-CONTENT-SHA256::{content_hash}"
    hex_sig, _, dstu_bundle = derive_micro_offsets(payload, secret_key)

    precomputed = {
        "content_hash": content_hash,
        "hex_sig": hex_sig,
        "dstu_bundle": dstu_bundle,
    }

    clean_recipients = [r.strip() for r in recipients if r.strip()]
    copies: list[dict[str, Any]] = []
    for idx, rec_id in enumerate(clean_recipients, start=1):
        safe_slug = re.sub(r"[^A-Za-z0-9._-]+", "_", rec_id).strip("_") or f"recipient_{idx:02d}"
        out_pdf = out_dir / f"{in_pdf.stem}__copy_{idx:02d}_{safe_slug}.pdf"
        res = stamp_pdf_universal_v21(
            in_pdf=in_pdf,
            out_pdf=out_pdf,
            secret_key=secret_key,
            recipient_id=rec_id,
            emblem_type=emblem_type,
            optical_ring=optical_ring,
            mode=mode,
            signer_key_name=signer_key_name,
            key_fingerprint=key_fingerprint,
            precomputed_crypto=precomputed,
            seal_pages=seal_pages,
        )
        copies.append(
            {
                "recipient_id": rec_id,
                "output_file": str(out_pdf),
                "canary_beacon_word": res["canary"]["beacon_word"],
                "public_canary_hash": res["canary"]["public_canary_hash"],
            }
        )

    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    manifest = {
        "status": "ok",
        "protocol": "MARMA-DEALROOM-BATCH-V2.1",
        "input_file": str(in_pdf),
        "output_dir": str(out_dir),
        "emblem_type": emblem_type,
        "optical_ring": optical_ring,
        "content_sha256": content_hash,
        "hmac_sha256": hex_sig,
        "key_fingerprint": key_fingerprint,
        "recipient_count": len(copies),
        "elapsed_ms": elapsed_ms,
        "copies": copies,
    }
    manifest_path = out_dir / f"{in_pdf.stem}_dealroom_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    manifest["manifest_file"] = str(manifest_path)
    return manifest


# ==============================================================================
# 3. UNIFIED VECTOR + OPTICAL LEAK TRACER
# ==============================================================================
def trace_leak_any_medium(
    target_path: Path,
    suspects: list[str],
    secret_key: str = DEFAULT_SECRET,
    content_sha256: str = "",
    key_fingerprint: str = "",
) -> dict[str, Any]:
    """
    Unified forensic leak tracer:
    - If `target_path` is a raster image (`.png`, `.jpg`, `.jpeg`, `.webp`), uses
      Marma-Optical Soft-Decision ML correlation over the 32-Sector Lotus Ring.
    - If `target_path` is a vector document (`.pdf`, `.docx`, `.svg`), uses
      exact sub-micron vector coordinate inversion (and falls back to universal v2.1 PDF).
    """
    ext = target_path.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
        return extract_canary_from_raster_image(
            image_path=target_path,
            suspects=suspects,
            secret_key=secret_key,
            content_sha256=content_sha256,
            key_fingerprint=key_fingerprint,
        )

    if ext == ".pdf":
        ver = verify_pdf_universal_v21(target_path, secret_key=secret_key)
        if ver.get("emblem_type", "sri-yantra") != "sri-yantra":
            beacon_word = int(ver.get("canary_beacon_word", 0))
            csha = str(ver.get("computed_content_sha256", ""))
            kfp = str(ver.get("key_fingerprint", ""))
            matched = []
            tested = []
            for s in suspects:
                s_clean = s.strip()
                if not s_clean:
                    continue
                tag = compute_canary_tag(secret_key, csha, s_clean, kfp)
                hit = beacon_word > 0 and (tag["beacon_word"] == beacon_word)
                if hit:
                    matched.append(s_clean)
                tested.append(
                    {
                        "recipient_id": s_clean,
                        "expected_beacon_word": tag["beacon_word"],
                        "matched": hit,
                    }
                )
            return {
                "file": str(target_path),
                "verified": ver.get("verified", False),
                "emblem_type": ver.get("emblem_type"),
                "canary_beacon_word": beacon_word,
                "matched_recipient": matched[0] if len(matched) == 1 else None,
                "matched_suspects": matched,
                "tested_candidates": tested,
            }

    return trace_canary_suspects(target_path, suspects, secret_key=secret_key)


# ==============================================================================
# 3B. ADMIN PANEL AUTHENTICATION & VISITOR TELEMETRY ENGINE (v2.3.0)
# ==============================================================================
ADMIN_AUTH_SALT = b"MARMA-CRYPTO-ADMIN-SALT-V2.3.0::EDU-VEDI"
ADMIN_AUTH_ITERATIONS = 100000
EXPECTED_ADMIN_EMAIL_HASH = "877595b2195819f4d510bcc6d68dfc21364f46a3d74de0889233fa561fd89131"
# Primary PBKDF2-HMAC-SHA256 verifier hash for zerhug@gmail.com + secondary fallback hash:
EXPECTED_ADMIN_VERIFIER_HASH = "7d3149e8b8befd79145f8995b2087120edb2be48ce9cee42648c880bac3f4aba"
ACCEPTED_ADMIN_VERIFIER_HASHES: tuple[str, ...] = (
    "7d3149e8b8befd79145f8995b2087120edb2be48ce9cee42648c880bac3f4aba",
    "89fd2f96c3891ce927a8f500f024e15f9a9265c394e369707af0521ee53623d0",
)

_TELEMETRY_LOCK = threading.Lock()
_TELEMETRY_EVENTS_MEM: list[dict[str, Any]] = []


def _get_telemetry_db_path() -> Path:
    custom = os.environ.get("MARMA_TELEMETRY_DB_PATH", "").strip()
    if custom:
        return Path(custom)
    return Path("/tmp/marma_telemetry_v23.sqlite3")


def _init_telemetry_sqlite() -> None:
    db_path = _get_telemetry_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(str(db_path))) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry_events_v23 (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                epoch_ms INTEGER NOT NULL,
                visitor_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                ip TEXT NOT NULL,
                country TEXT NOT NULL,
                country_code TEXT NOT NULL,
                city TEXT NOT NULL,
                region TEXT NOT NULL,
                isp TEXT NOT NULL,
                asn TEXT NOT NULL,
                timezone TEXT NOT NULL,
                page TEXT NOT NULL,
                path TEXT NOT NULL,
                lang TEXT NOT NULL,
                referrer TEXT NOT NULL,
                browser TEXT NOT NULL,
                os TEXT NOT NULL,
                device_type TEXT NOT NULL,
                screen TEXT NOT NULL,
                action TEXT NOT NULL,
                details_json TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_ip ON telemetry_events_v23(ip)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_epoch ON telemetry_events_v23(epoch_ms)")
        conn.commit()


def verify_admin_credentials_v23(email: str, password: str) -> dict[str, Any]:
    """
    Zero-plaintext PBKDF2-HMAC-SHA256 (100,000 iterations) verification for the
    Marma-Crypto v2.3.0 Admin Panel. Matches the WebCrypto implementation in docs/admin.html.
    """
    clean_email = (email or "").strip().lower()
    email_hash = hashlib.sha256(f"MARMA-ADMIN-EMAIL-V23::{clean_email}".encode("utf-8")).hexdigest()
    credential = f"{clean_email}:{password or ''}".encode("utf-8")
    dk = hashlib.pbkdf2_hmac("sha256", credential, ADMIN_AUTH_SALT, ADMIN_AUTH_ITERATIONS, dklen=32)
    verifier_hash = hashlib.sha256(b"MARMA-ADMIN-VERIFIER-V23::" + dk).hexdigest()
    email_ok = hmac.compare_digest(email_hash, EXPECTED_ADMIN_EMAIL_HASH)
    pass_ok = any(hmac.compare_digest(verifier_hash, expected) for expected in ACCEPTED_ADMIN_VERIFIER_HASHES)
    authenticated = bool(email_ok and pass_ok)
    return {
        "authenticated": authenticated,
        "admin_email": clean_email if authenticated else None,
        "admin_key": dk.hex() if authenticated else None,
        "verifier_hash": verifier_hash if authenticated else None,
        "kdf": "PBKDF2-HMAC-SHA256",
        "iterations": ADMIN_AUTH_ITERATIONS,
    }


def verify_admin_key_hex_v23(dk_hex: str) -> bool:
    """Verify a derived 256-bit hex key (`X-Marma-Admin-Key`) without storing the key in plaintext."""
    try:
        dk = bytes.fromhex((dk_hex or "").strip())
    except ValueError:
        return False
    if len(dk) != 32:
        return False
    verifier_hash = hashlib.sha256(b"MARMA-ADMIN-VERIFIER-V23::" + dk).hexdigest()
    return any(hmac.compare_digest(verifier_hash, expected) for expected in ACCEPTED_ADMIN_VERIFIER_HASHES)


def record_telemetry_event_v23(event: dict[str, Any], client_ip: str = "127.0.0.1") -> dict[str, Any]:
    """Record a visitor telemetry event with IP, Geo/ASN, OS/Browser, and action metadata (SQLite + RAM)."""
    now_iso = datetime.now(timezone.utc).isoformat()
    raw_ip = str(event.get("ip") or "").strip()
    resolved_ip = raw_ip if (raw_ip and raw_ip not in ("resolving...", "local-client")) else (client_ip or "127.0.0.1")
    rec: dict[str, Any] = {
        "event_id": str(event.get("event_id") or f"evt_{int(time.time() * 1000)}_{len(_TELEMETRY_EVENTS_MEM)}"),
        "timestamp": str(event.get("timestamp") or now_iso),
        "epoch_ms": int(event.get("epoch_ms") or int(time.time() * 1000)),
        "visitor_id": str(event.get("visitor_id") or "v_anon"),
        "session_id": str(event.get("session_id") or "s_anon"),
        "ip": resolved_ip,
        "country": str(event.get("country") or "Local / Unknown"),
        "country_code": str(event.get("country_code") or "LO"),
        "city": str(event.get("city") or "Localhost"),
        "region": str(event.get("region") or ""),
        "isp": str(event.get("isp") or "Direct HTTP Client"),
        "asn": str(event.get("asn") or "AS0"),
        "timezone": str(event.get("timezone") or "UTC"),
        "page": str(event.get("page") or "index.html"),
        "path": str(event.get("path") or "/"),
        "lang": str(event.get("lang") or "en"),
        "referrer": str(event.get("referrer") or "direct"),
        "browser": str(event.get("browser") or "Python/HTTP"),
        "os": str(event.get("os") or "Linux"),
        "device_type": str(event.get("device_type") or "Desktop"),
        "screen": str(event.get("screen") or "0x0"),
        "action": str(event.get("action") or "page_view"),
        "details": dict(event.get("details") or {}),
    }
    with _TELEMETRY_LOCK:
        _TELEMETRY_EVENTS_MEM.append(rec)
        if len(_TELEMETRY_EVENTS_MEM) > 5000:
            del _TELEMETRY_EVENTS_MEM[:-5000]
        try:
            _init_telemetry_sqlite()
            with closing(sqlite3.connect(str(_get_telemetry_db_path()))) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO telemetry_events_v23 VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        rec["event_id"],
                        rec["timestamp"],
                        rec["epoch_ms"],
                        rec["visitor_id"],
                        rec["session_id"],
                        rec["ip"],
                        rec["country"],
                        rec["country_code"],
                        rec["city"],
                        rec["region"],
                        rec["isp"],
                        rec["asn"],
                        rec["timezone"],
                        rec["page"],
                        rec["path"],
                        rec["lang"],
                        rec["referrer"],
                        rec["browser"],
                        rec["os"],
                        rec["device_type"],
                        rec["screen"],
                        rec["action"],
                        json.dumps(rec["details"], ensure_ascii=False),
                    ),
                )
                conn.commit()
        except Exception:
            pass
    return rec


def clear_telemetry_events_v23() -> int:
    """Clear both SQLite and in-memory telemetry events and return the number of cleared records."""
    with _TELEMETRY_LOCK:
        count = len(_TELEMETRY_EVENTS_MEM)
        _TELEMETRY_EVENTS_MEM.clear()
        try:
            _init_telemetry_sqlite()
            with closing(sqlite3.connect(str(_get_telemetry_db_path()))) as conn:
                cur = conn.execute("SELECT COUNT(*) FROM telemetry_events_v23")
                db_count = int(cur.fetchone()[0])
                conn.execute("DELETE FROM telemetry_events_v23")
                conn.commit()
                count = max(count, db_count)
        except Exception:
            pass
    return count


def get_telemetry_stats_v23() -> dict[str, Any]:
    """Compute aggregated visitor, IP, geo, OS/browser, popularity, and action analytics for Admin Panel."""
    with _TELEMETRY_LOCK:
        events_by_id: dict[str, dict[str, Any]] = {e["event_id"]: e for e in _TELEMETRY_EVENTS_MEM}
        try:
            _init_telemetry_sqlite()
            with closing(sqlite3.connect(str(_get_telemetry_db_path()))) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM telemetry_events_v23 ORDER BY epoch_ms ASC LIMIT 10000"
                ).fetchall()
                for r in rows:
                    d = dict(r)
                    d["details"] = json.loads(d.pop("details_json", "{}") or "{}")
                    events_by_id[d["event_id"]] = d
        except Exception:
            pass
        events = sorted(events_by_id.values(), key=lambda x: x.get("epoch_ms", 0))

    now_ms = int(time.time() * 1000)
    day_ms = 86_400_000
    by_ip: dict[str, dict[str, Any]] = {}
    action_counts: dict[str, int] = {}
    country_counts: dict[str, int] = {}
    page_counts: dict[str, int] = {}
    referrer_counts: dict[str, int] = {}
    os_counts: dict[str, int] = {}
    browser_counts: dict[str, int] = {}
    unique_sessions: set[str] = set()
    unique_visitors: set[str] = set()
    dau_ips: set[str] = set()
    wau_ips: set[str] = set()
    mau_ips: set[str] = set()

    for ev in events:
        ip = ev.get("ip", "127.0.0.1")
        act = ev.get("action", "unknown")
        country = f"{ev.get('country', 'Unknown')} ({ev.get('country_code', 'UN')})"
        page = ev.get("page", "index.html")
        ref = ev.get("referrer") or "direct"
        os_name = ev.get("os") or "Unknown"
        br_name = ev.get("browser") or "Unknown"
        ep_ms = int(ev.get("epoch_ms") or now_ms)

        unique_sessions.add(ev.get("session_id", ""))
        unique_visitors.add(ev.get("visitor_id", ""))
        if now_ms - ep_ms <= day_ms:
            dau_ips.add(ip)
        if now_ms - ep_ms <= 7 * day_ms:
            wau_ips.add(ip)
        if now_ms - ep_ms <= 30 * day_ms:
            mau_ips.add(ip)

        action_counts[act] = action_counts.get(act, 0) + 1
        country_counts[country] = country_counts.get(country, 0) + 1
        page_counts[page] = page_counts.get(page, 0) + 1
        referrer_counts[ref] = referrer_counts.get(ref, 0) + 1
        os_counts[os_name] = os_counts.get(os_name, 0) + 1
        browser_counts[br_name] = browser_counts.get(br_name, 0) + 1

        if ip not in by_ip:
            by_ip[ip] = {
                "ip": ip,
                "country": ev.get("country", "Unknown"),
                "country_code": ev.get("country_code", "UN"),
                "city": ev.get("city", ""),
                "isp": ev.get("isp", ""),
                "asn": ev.get("asn", ""),
                "os": os_name,
                "browser": br_name,
                "device_type": ev.get("device_type", "Desktop"),
                "first_seen": ev.get("timestamp", ""),
                "last_seen": ev.get("timestamp", ""),
                "total_events": 0,
                "actions": [],
                "pages": [],
                "sessions": set(),
            }
        entry = by_ip[ip]
        entry["total_events"] += 1
        if ev.get("timestamp", "") < entry["first_seen"] or not entry["first_seen"]:
            entry["first_seen"] = ev.get("timestamp", "")
        if ev.get("timestamp", "") > entry["last_seen"]:
            entry["last_seen"] = ev.get("timestamp", "")
        entry["actions"].append(act)
        if page not in entry["pages"]:
            entry["pages"].append(page)
        entry["sessions"].add(ev.get("session_id", ""))

    ip_profiles = []
    returning_ips = 0
    engaged_ips = 0
    deep_forensic_ips = 0
    for ip, data in by_ip.items():
        data_copy = dict(data)
        sess_cnt = len(data["sessions"])
        data_copy["session_count"] = sess_cnt
        if sess_cnt > 1 or data["total_events"] >= 3:
            returning_ips += 1
        acts_set = set(data["actions"])
        if acts_set.intersection(
            {"seal_pdf_browser", "seal_svg_browser", "dealroom_1click_demo", "verify_file_drop", "verify_preset_load"}
        ):
            engaged_ips += 1
        if acts_set.intersection({"canary_trace_run", "simulate_tamper_attack", "download_sealed_copy"}):
            deep_forensic_ips += 1
        del data_copy["sessions"]
        ip_profiles.append(data_copy)
    ip_profiles.sort(key=lambda x: x["total_events"], reverse=True)

    total_ips = len(by_ip)
    retention_pct = round((returning_ips / total_ips) * 100.0, 1) if total_ips > 0 else 0.0
    popularity_score = min(
        100,
        int(
            round(
                min(40.0, total_ips * 5.0)
                + min(30.0, len(events) * 1.5)
                + min(30.0, retention_pct * 0.3)
            )
        ),
    )

    return {
        "status": "ok",
        "version": API_VERSION,
        "persistence": {
            "engine": "SQLite3 + RAM Cache",
            "db_path": str(_get_telemetry_db_path()),
        },
        "summary": {
            "total_events": len(events),
            "unique_ips": total_ips,
            "unique_visitors": len(unique_visitors),
            "unique_sessions": len(unique_sessions),
            "action_counts": action_counts,
            "country_counts": country_counts,
            "page_counts": page_counts,
            "referrer_counts": referrer_counts,
            "os_counts": os_counts,
            "browser_counts": browser_counts,
        },
        "popularity": {
            "popularity_score_0_100": popularity_score,
            "dau_unique_ips": len(dau_ips),
            "wau_unique_ips": len(wau_ips),
            "mau_unique_ips": len(mau_ips),
            "returning_ips": returning_ips,
            "new_ips": max(0, total_ips - returning_ips),
            "retention_rate_pct": retention_pct,
            "conversion_funnel": {
                "visited_site_ips": total_ips,
                "used_studio_sealer_or_verifier_ips": engaged_ips,
                "ran_canary_or_downloaded_ips": deep_forensic_ips,
            },
        },
        "ip_profiles": ip_profiles,
        "events": events,
    }


# ==============================================================================
# 4. REST API ROUTER & EMBEDDED HTTP MICROSERVICE
# ==============================================================================
def dispatch_api_request(
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    client_ip: str = "127.0.0.1",
) -> tuple[int, dict[str, Any]]:
    """Pure functional dispatcher for REST endpoints (usable both in-process and over HTTP)."""
    payload = body or {}
    req_headers = {k.lower(): v for k, v in (headers or {}).items()}
    if method == "GET" and path == "/v1/health":
        return 200, {
            "status": "ok",
            "service": "marma-crypto-dealroom-api",
            "version": API_VERSION,
            "supported_emblems": list(SUPPORTED_EMBLEMS),
            "optical_ecc": "[32, 16, d_min=8] Soft-Decision ML Lotus Ring",
        }

    if method == "POST" and path == "/v1/seal-batch":
        in_file = Path(str(payload.get("input_file", "")))
        out_dir = Path(str(payload.get("output_dir", "")))
        recipients = list(payload.get("recipients") or [])
        emblem_type = str(payload.get("emblem_type") or "sri-yantra")
        optical_ring = bool(payload.get("optical_ring", True))
        secret_key = str(payload.get("secret_key") or DEFAULT_SECRET)
        if not in_file.is_file() or not recipients:
            return 400, {"status": "error", "error": "Valid input_file and non-empty recipients list required"}
        res = batch_seal_dealroom(
            in_pdf=in_file,
            out_dir=out_dir,
            recipients=recipients,
            secret_key=secret_key,
            emblem_type=emblem_type,
            optical_ring=optical_ring,
        )
        return 200, res

    if method == "POST" and path == "/v1/verify":
        target = Path(str(payload.get("file", "")))
        secret_key = str(payload.get("secret_key") or DEFAULT_SECRET)
        recipient_id = str(payload.get("recipient_id") or "")
        if not target.is_file():
            return 400, {"status": "error", "error": f"File not found: {target}"}
        if target.suffix.lower() == ".pdf":
            res = verify_pdf_universal_v21(target, secret_key=secret_key, recipient_id=recipient_id)
        else:
            res = verify_any_file(target, secret_key=secret_key, recipient_id=recipient_id)
        return 200, res

    if method == "POST" and path == "/v1/trace-leak":
        target = Path(str(payload.get("file", "")))
        suspects = list(payload.get("suspects") or [])
        secret_key = str(payload.get("secret_key") or DEFAULT_SECRET)
        content_sha256 = str(payload.get("content_sha256") or "")
        key_fingerprint = str(payload.get("key_fingerprint") or "")
        if not target.is_file() or not suspects:
            return 400, {"status": "error", "error": "Valid file and suspects list required"}
        res = trace_leak_any_medium(
            target_path=target,
            suspects=suspects,
            secret_key=secret_key,
            content_sha256=content_sha256,
            key_fingerprint=key_fingerprint,
        )
        return 200, res

    if method == "POST" and path == "/v2.3/verify-marma54":
        from .kak_synthesis_v23 import verify_sri_yantra_marma_concurrency_v23

        triangles = list(payload.get("triangles") or [])
        cx = float(payload.get("cx", 150.0))
        if len(triangles) != 9:
            return 400, {"status": "error", "error": "9 Sri Yantra triangles required"}
        return 200, verify_sri_yantra_marma_concurrency_v23(triangles, cx=cx)

    if method == "POST" and path == "/v2.3/augmented-stamp":
        from .kak_synthesis_v23 import stamp_augmented_dual_layer_v23

        doc_payload = str(payload.get("payload") or "")
        secret_key = str(payload.get("secret_key") or DEFAULT_SECRET)
        recipient_id = str(payload.get("recipient_id") or "")
        recipient_code = payload.get("recipient_code_23bit")
        if not doc_payload:
            return 400, {"status": "error", "error": "Non-empty payload required"}
        return 200, stamp_augmented_dual_layer_v23(
            payload=doc_payload,
            secret_key=secret_key,
            recipient_id=recipient_id,
            recipient_code_23bit=int(recipient_code) if recipient_code is not None else None,
        )

    if method == "POST" and path == "/v2.3/augmented-verify":
        from .kak_synthesis_v23 import verify_augmented_dual_layer_v23

        packet = dict(payload.get("packet") or {})
        doc_payload = payload.get("payload")
        secret_key = payload.get("secret_key")
        suspects = payload.get("suspect_recipients")
        if not packet or "triangles" not in packet:
            return 400, {"status": "error", "error": "Valid augmented packet with triangles required"}
        return 200, verify_augmented_dual_layer_v23(
            packet=packet,
            payload=str(doc_payload) if doc_payload is not None else None,
            secret_key=str(secret_key) if secret_key else None,
            suspect_recipients=list(suspects) if suspects else None,
        )

    if method == "GET" and path == "/v2.3/kak-cross-validation":
        from .kak_synthesis_v23 import cross_validate_kak_corpus_v23

        return 200, cross_validate_kak_corpus_v23(verify_pdf_sha256=False)

    if method == "POST" and path == "/v2.3/telemetry/ingest":
        forwarded_ip = (
            req_headers.get("x-forwarded-for", "").split(",")[0].strip()
            or req_headers.get("cf-connecting-ip", "").strip()
            or req_headers.get("x-real-ip", "").strip()
            or client_ip
        )
        rec = record_telemetry_event_v23(payload, client_ip=forwarded_ip)
        return 200, {"status": "ok", "recorded": True, "event_id": rec["event_id"], "ip": rec["ip"]}

    if method == "POST" and path == "/v2.3/admin/login":
        email = str(payload.get("email") or "")
        password = str(payload.get("password") or "")
        auth = verify_admin_credentials_v23(email, password)
        if not auth["authenticated"]:
            return 401, {"status": "error", "authenticated": False, "error": "Invalid administrator email or password"}
        return 200, {"status": "ok", **auth}

    if method == "GET" and path == "/v2.3/admin/stats":
        admin_key = req_headers.get("x-marma-admin-key") or str(payload.get("admin_key") or "")
        if not verify_admin_key_hex_v23(admin_key):
            return 401, {"status": "error", "error": "Unauthorized: valid X-Marma-Admin-Key required"}
        return 200, get_telemetry_stats_v23()

    if method == "POST" and path == "/v2.3/admin/clear":
        admin_key = req_headers.get("x-marma-admin-key") or str(payload.get("admin_key") or "")
        if not verify_admin_key_hex_v23(admin_key):
            return 401, {"status": "error", "error": "Unauthorized: valid X-Marma-Admin-Key required"}
        cleared = clear_telemetry_events_v23()
        return 200, {"status": "ok", "cleared_events": cleared}

    if method == "POST" and path == "/v2.3/kan/score-risk":
        from .kan_kak_bridge_v23 import KAN_KAK_MODEL_ID_RISK, score_risk_kak_v23

        entity = dict(payload.get("entity") or {})
        if not entity:
            return 400, {"status": "error", "error": "Non-empty entity dict required"}
        model_id = str(payload.get("model_id") or KAN_KAK_MODEL_ID_RISK)
        return 200, score_risk_kak_v23(entity=entity, model_id=model_id)

    if method == "POST" and path == "/v2.3/kan/predict-outcome":
        from .kan_kak_bridge_v23 import KAN_KAK_MODEL_ID_OUTCOME, predict_outcome_kak_v23

        feats = list(payload.get("features") or [])
        if not feats:
            return 400, {"status": "error", "error": "Non-empty features list required"}
        model_id = str(payload.get("model_id") or KAN_KAK_MODEL_ID_OUTCOME)
        return 200, predict_outcome_kak_v23(features=feats, model_id=model_id)

    if method == "POST" and path == "/v2.3/kan/qmc-evl":
        from .kan_kak_bridge_v23 import simulate_evl_kak_dsequence_qmc_v23

        return 200, simulate_evl_kak_dsequence_qmc_v23(
            claim_amount_eur=float(payload.get("claim_amount_eur", 1_000_000.0)),
            win_prob_p=float(payload.get("win_prob_p", 0.65)),
            legal_cost_eur=float(payload.get("legal_cost_eur", 80_000.0)),
            adverse_cost_eur=float(payload.get("adverse_cost_eur", 60_000.0)),
            settlement_offer_eur=float(payload.get("settlement_offer_eur", 450_000.0)),
            secret_key=str(payload.get("secret_key") or DEFAULT_SECRET),
            case_code=str(payload.get("case_code") or "ARBITRATION-KAK-QMC"),
        )

    if method == "POST" and path == "/v2.3/kan/stamp-audit":
        from .kan_kak_bridge_v23 import stamp_kan_audit_memo_v23

        entity = dict(payload.get("entity") or {})
        recipient_id = str(payload.get("recipient_id") or "G2-Client-Recipient")
        if not entity:
            return 400, {"status": "error", "error": "Non-empty entity dict required"}
        return 200, stamp_kan_audit_memo_v23(
            entity=entity,
            recipient_id=recipient_id,
            secret_key=str(payload.get("secret_key") or DEFAULT_SECRET),
            case_code=str(payload.get("case_code") or "G2-ARBITRATION-AUDIT"),
            recipient_code_23bit=(
                int(payload["recipient_code_23bit"]) if payload.get("recipient_code_23bit") is not None else None
            ),
        )

    if method == "POST" and path == "/v2.3/kan/verify-audit":
        from .kan_kak_bridge_v23 import verify_kan_audit_memo_v23

        bundle = dict(payload.get("bundle") or {})
        if not bundle or "augmented_seal_packet" not in bundle:
            return 400, {"status": "error", "error": "Valid stamped bundle required"}
        return 200, verify_kan_audit_memo_v23(
            stamped_bundle=bundle,
            secret_key=payload.get("secret_key"),
            suspect_recipients=payload.get("suspect_recipients"),
        )

    return 404, {"status": "error", "error": f"Unknown endpoint: {method} {path}"}


class _DealRoomRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return  # Silence noisy stdout logging during automated tests

    def _send_json(self, status_code: int, data: dict[str, Any]) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Marma-Admin-Key")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_json(200, {"status": "ok"})

    def do_GET(self) -> None:  # noqa: N802
        hdrs = {k: v for k, v in self.headers.items()}
        client_ip = self.client_address[0] if self.client_address else "127.0.0.1"
        code, resp = dispatch_api_request("GET", self.path, None, headers=hdrs, client_ip=client_ip)
        self._send_json(code, resp)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        body = json.loads(raw_body) if raw_body.strip() else {}
        hdrs = {k: v for k, v in self.headers.items()}
        client_ip = self.client_address[0] if self.client_address else "127.0.0.1"
        code, resp = dispatch_api_request("POST", self.path, body, headers=hdrs, client_ip=client_ip)
        self._send_json(code, resp)


class MarmaDealRoomServer:
    """Context-managed background HTTP server for Deal-Room integration & live E2E tests."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self._server = HTTPServer((host, port), _DealRoomRequestHandler)
        self.host, self.port = self._server.server_address
        self.base_url = f"http://{self.host}:{self.port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def start(self) -> "MarmaDealRoomServer":
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=2.0)

    def __enter__(self) -> "MarmaDealRoomServer":
        return self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

    def get_json(self, path: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any]]:
        opener = build_opener(ProxyHandler({}))
        req = Request(f"{self.base_url}{path}", headers=headers or {}, method="GET")
        try:
            with opener.open(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except HTTPError as err:
            return err.code, json.loads(err.read().decode("utf-8"))

    def post_json(
        self, path: str, payload: dict[str, Any], headers: dict[str, str] | None = None
    ) -> tuple[int, dict[str, Any]]:
        opener = build_opener(ProxyHandler({}))
        data = json.dumps(payload).encode("utf-8")
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
        req = Request(
            f"{self.base_url}{path}",
            data=data,
            headers=req_headers,
            method="POST",
        )
        try:
            with opener.open(req, timeout=30) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except HTTPError as err:
            return err.code, json.loads(err.read().decode("utf-8"))

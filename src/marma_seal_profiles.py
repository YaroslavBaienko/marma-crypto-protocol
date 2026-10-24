#!/usr/bin/env python3
"""Profile-aware wrapper around the production Marma signer (additive; P1 unchanged).

Profiles
  v1-geometric : the legacy 300x300 SVG seal produced by sign_sri_yantra_svg (default).
  v2-round42   : the product prototype — a 42 mm round, branded technical stamp. The canonical
                 nine-triangle carrier geometry is kept EXACTLY as generated (no coordinate
                 transform), so the payload/proof code is untouched; the profile changes the
                 physical size, the round decoration and persists a profile id in the SVG
                 metadata so a verifier cannot silently switch profiles.

Usage
  from marma_seal_profiles import sign_seal_svg, verify_seal_svg, PROFILES
  res = sign_seal_svg(payload, secret, Path("seal.svg"), profile_id="v2-round42")
  ver = verify_seal_svg(Path("seal.svg").read_text(), expected_profile="v2-round42")
"""
from __future__ import annotations
import html, re
from dataclasses import dataclass
from pathlib import Path
import tempfile

import marma_watermark as mw

@dataclass(frozen=True)
class SealProfile:
    id: str
    version: str
    physical_mm: float
    viewbox: float = 300.0
    decorative: bool = False
    brand: str = "Marma-Crypto"

PROFILES: dict[str, SealProfile] = {
    "v1-geometric": SealProfile("v1-geometric", "1", physical_mm=0.0, decorative=False),
    "v2-round42": SealProfile("v2-round42", "2", physical_mm=42.0, decorative=True),
}

def get_profile(profile_id: str) -> SealProfile:
    try:
        return PROFILES[profile_id]
    except KeyError:
        raise ValueError(f"unknown seal profile: {profile_id!r}") from None

def _decorate_round42(svg: str, p: SealProfile) -> str:
    """Render the canonical seal content inside a 42 mm round branded stamp (no coordinate change)."""
    s = svg
    # physical size: the viewBox stays 0 0 300 300, so 1 unit = 42/300 mm
    s = re.sub(r'(<svg[^>]*?)\bwidth="[^"]*"\s+height="[^"]*"', rf'\1width="{p.physical_mm:g}mm" height="{p.physical_mm:g}mm"', s, count=1)
    # round background instead of the dark square
    s = s.replace('<rect width="300" height="300" fill="#060913" />',
                  '<circle cx="150" cy="150" r="150" fill="#060913" />')
    # branded technical rings + cardinal marks (decorative only, not payload)
    deco = (
        '\n  <circle cx="150" cy="150" r="148" fill="none" stroke="#e6bd53" stroke-width="1.6" />'
        '\n  <circle cx="150" cy="150" r="142" fill="none" stroke="#e6bd53" stroke-width="0.8" />'
        '\n  <circle cx="150" cy="150" r="116" fill="none" stroke="#f0d078" stroke-width="0.6" />'
        '\n  <circle cx="150" cy="150" r="150" fill="none" stroke="#fff2c4" stroke-width="0.4" />'
    )
    s = s.replace('<circle cx="150" cy="150" r="100"', deco + '\n  <circle cx="150" cy="150" r="100"', 1)
    return s

def _persist_profile(svg: str, p: SealProfile) -> str:
    """Append profile attributes to the <metadata> element (kept alongside the payload/signature)."""
    attrs = (f' data-profile="{html.escape(p.id, quote=True)}"'
             f' data-profile-version="{html.escape(p.version, quote=True)}"'
             f' data-profile-mm="{p.physical_mm:g}"'
             f' data-profile-brand="{html.escape(p.brand, quote=True)}"')
    i = svg.find("<metadata")
    if i < 0:
        raise ValueError("SVG metadata element missing")
    j = svg.find("/>", i)
    if j < 0:
        raise ValueError("SVG metadata element not self-closing")
    return svg[:j] + attrs + svg[j:]

def sign_seal_svg(payload: str, secret_key: str, out_svg: Path,
                  profile_id: str = "v2-round42", **kw) -> dict:
    """Sign with the production signer, then render/persist the requested seal profile."""
    p = get_profile(profile_id)
    out_svg = Path(out_svg)
    with tempfile.TemporaryDirectory() as td:
        canonical = Path(td) / "canonical.svg"
        res = mw.sign_sri_yantra_svg(payload, secret_key, canonical, **kw)
        svg = canonical.read_text(encoding="utf-8")
    if p.id != "v1-geometric":
        svg = _decorate_round42(svg, p)
        svg = _persist_profile(svg, p)
    out_svg.write_text(svg, encoding="utf-8")
    res.update({"output_file": str(out_svg), "profile": p.id, "profile_version": p.version,
                "profile_mm": p.physical_mm})
    return res

def verify_seal_svg(svg_text: str, profile_id: str | None = None,
                    expected_profile: str | None = None, **kw) -> dict:
    """Verify a profiled seal. The stored profile id is mandatory for v2; an unknown or mismatched
    profile fails closed before the cryptographic check."""
    m = re.search(r'data-profile="([^"]+)"', svg_text)
    stored = html.unescape(m.group(1)) if m else "v1-geometric"
    if profile_id is not None and profile_id != stored:
        return {"verified": False, "reason": f"profile id mismatch: stored {stored}, expected {profile_id}"}
    if expected_profile is not None and expected_profile != stored:
        return {"verified": False, "reason": f"unexpected seal profile: {stored} != {expected_profile}"}
    try:
        p = get_profile(stored)
    except ValueError as e:
        return {"verified": False, "reason": str(e)}
    if p.decorative:
        mm = re.search(r'<svg[^>]*\bwidth="([0-9.]+)mm"', svg_text)
        if not mm or abs(float(mm.group(1)) - p.physical_mm) > 0.1:
            return {"verified": False, "reason": f"profile physical size mismatch for {p.id}"}
    res = mw.verify_sri_yantra_svg(svg_text, **kw)
    res["profile"] = p.id
    res["profile_mm"] = p.physical_mm
    return res

if __name__ == "__main__":
    import sys
    print("profiles:", ", ".join(PROFILES))
    sys.exit(0)

#!/usr/bin/env python3
"""Versioned stamp profiles for the controlled paper/product runs.

Profile P1 ("v1-geometric") reproduces the current evaluation carrier: canonical coordinates are
used unscaled, the stamp sits at (45, 50) pt in PDF user space. Profile P2 ("v2-round42") is the
product prototype: a 42 mm round technical stamp, the same nine-triangle payload geometry scaled
into the centre, decorative rings outside the payload.

Invariant kept by all profiles: the payload DELTAS are absolute page points (multiples of 18 npt);
only the canonical base geometry is scaled/moved. Scaling a stamped PDF after the fact would scale
the deltas too and is therefore forbidden.
"""
from __future__ import annotations
import json, math
from dataclasses import dataclass, asdict, field
from pathlib import Path
import pymupdf as fitz
import pdf_layer as pl

N = pl.N_SLOTS
MM = 72.0 / 25.4
MARK_RG = ".0137 .0246 .0315 RG"
DECOR_RG = ".12 .12 .12 RG"

@dataclass(frozen=True)
class Profile:
    id: str
    version: str
    scale: float
    placement: str          # "bottom-left-fixed" | "reserved-centre"
    diameter_mm: float | None = None
    decorative: bool = False

P1 = Profile("v1-geometric", "1", 1.0, "bottom-left-fixed")
P2 = Profile("v2-round42", "2", 0.45, "reserved-centre", diameter_mm=42.0, decorative=True)

def canonical(kind: str = "sri-yantra", seed: int = 0) -> list[float]:
    return pl._canonical(kind, seed)

def _local_points(slots: list[float]) -> list[tuple[float, float, float]]:
    """Triangle geometry in emblem-local coordinates: (left, right, apex) as (x, y) pairs."""
    out = []
    for t in range(9):
        by, ay, hw = slots[3*t:3*t+3]
        out.append(((95.0 - hw, by), (95.0 + hw, by), (95.0, ay)))
    return out

def _centre(slots: list[float]) -> tuple[float, float]:
    xs, ys = [], []
    for (lx, by), (rx, _), (ax, ay) in _local_points(slots):
        xs += [lx, rx, ax]; ys += [by, ay]
    return ((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)

def origin(page, profile: Profile, slots: list[float]) -> tuple[float, float]:
    if profile.placement == "bottom-left-fixed":
        return (45.0, 50.0)
    if profile.placement == "reserved-centre":
        # centre of the reserved bottom-left box, 42 mm stamp: centre at 1/4 width, 120 pt high
        cx, cy = page.rect.width * 0.25, 120.0
        lcx, lcy = _centre(slots)
        return (cx - profile.scale * lcx, cy - profile.scale * lcy)
    raise ValueError(profile.placement)

def _draw(doc, page, profile: Profile, slots_plus_delta: list[float], slots: list[float]) -> None:
    """Inject path operators at 9-decimal precision. `slots_plus_delta` carries (by,ay,hw) where
    the delta is already applied to the drawn coordinates; see embed()."""
    x0, y0 = origin(page, profile, slots)
    s = profile.scale
    pts = _local_points(slots_plus_delta)
    chunks = []
    for t in range(9):
        (lx, by), (rx, _), (ax, ay) = pts[t]
        X = lambda v: x0 + s * v
        Y = lambda v: y0 + s * v
        chunks.append(f"{X(lx):.9f} {Y(by):.9f} m {X(rx):.9f} {Y(by):.9f} l {X(ax):.9f} {Y(ay):.9f} l h")
    body = "\n".join(chunks)
    ops = "q\n" + MARK_RG + "\n.37 w\n" + body + "\nS\nQ\n"
    if profile.decorative:
        d = profile.diameter_mm * MM
        cx, cy = page.rect.width * 0.25, 120.0
        rings = [f"{cx:.9f} {cy:.9f} {d/2:.9f} 0 360 re"]
        # circles are drawn as bezier-free "re" rectangles' superset: use four arcs via lines is
        # unnecessary; a circle can be approximated by two "c" curves per half. Keep simple:
        def circle(r):
            k = 0.5522847498307936 * r
            return (f"{cx+r:.9f} {cy:.9f} m "
                    f"{cx+r:.9f} {cy+k:.9f} {cx+k:.9f} {cy+r:.9f} {cx:.9f} {cy+r:.9f} c "
                    f"{cx-k:.9f} {cy+r:.9f} {cx-r:.9f} {cy+k:.9f} {cx-r:.9f} {cy:.9f} c "
                    f"{cx-r:.9f} {cy-k:.9f} {cx-k:.9f} {cy-r:.9f} {cx:.9f} {cy-r:.9f} c "
                    f"{cx+k:.9f} {cy-r:.9f} {cx+r:.9f} {cy-k:.9f} {cx+r:.9f} {cy:.9f} c h")
        deco = circle(d/2) + "\n" + circle(d/2 - 4.0)
        ops += "q\n" + DECOR_RG + "\n.8 w\n" + deco + "\nS\nQ\n"
    xrefs = page.get_contents()
    if xrefs:
        last = xrefs[-1]
        doc.update_stream(last, doc.xref_stream(last) + b"\n" + ops.encode("latin-1"))
    else:
        xref = doc.get_new_xref(); doc.update_object(xref, "<<>>")
        doc.update_stream(xref, ops.encode("latin-1")); page.set_contents(xref)

def embed_words(profile: Profile, payload_words: list[int], slots: list[float]) -> list[float]:
    """Return the three drawn slot values per triangle with the absolute deltas applied:
    by' = by + d; ay' = ay + d; hw' = hw + d (drawn as left/right offsets)."""
    deltas = [pl.word_to_delta(w) for w in payload_words]
    # the deltas must stay ABSOLUTE page points: add d/scale to the local value so that the
    # drawing transform (origin + scale * local) yields origin + scale*canonical + d.
    inv = 1.0 / profile.scale
    vals = []
    for t in range(9):
        by, ay, hw = slots[3*t:3*t+3]
        vals += [by + deltas[3*t] * inv, ay + deltas[3*t+1] * inv, hw + deltas[3*t+2] * inv]
    return vals

def stamp(src: Path, out: Path, p: Profile, payload_words: list[int], kind: str = "sri-yantra", seed: int = 0) -> None:
    slots = canonical(kind, seed)
    vals = embed_words(p, payload_words, slots)
    doc = fitz.open(str(src)); page = doc[0]
    _draw(doc, page, p, vals, slots)
    doc.save(str(out)); doc.close()

def _marker_nums(raw: bytes) -> list[float] | None:
    import re
    m = re.search(rb"0?\.0137 0?\.0246 0?\.0315 RG", raw)
    if not m: return None
    end = raw.find(b"S", m.end())
    if end < 0: return None
    nums = [float(x) for x in re.findall(rb"-?(?:\d+\.\d+|\.\d+)", raw[m.start():end])]
    # header: 3 colour numbers + 1 width number
    return nums[4:]

def extract_words(path: Path, p: Profile, kind: str = "sri-yantra", seed: int = 0) -> list[int] | None:
    doc = fitz.open(str(path))
    try:
        raw = b"".join(doc.xref_stream(x) for x in doc[0].get_contents())
        slots = canonical(kind, seed)
        x0, y0 = origin(doc[0], p, slots)
    finally:
        doc.close()
    nums = _marker_nums(raw)
    if nums is None or len(nums) < 54: return None
    s = p.scale
    words = []
    for t in range(9):
        lx, by, rx, by2, ax, ay = nums[6*t:6*t+6]
        hw_drawn = (rx - lx) / (2.0 * s)
        by_drawn = ((by + by2) / 2.0 - y0) / s
        ay_drawn = (ay - y0) / s
        base_by, base_ay, base_hw = slots[3*t:3*t+3]
        d_by = round(s * (by_drawn - base_by), 9)
        d_ay = round(s * (ay_drawn - base_ay), 9)
        d_hw = round(s * (hw_drawn - base_hw), 9)
        words += [pl.delta_to_word(d_by), pl.delta_to_word(d_ay), pl.delta_to_word(d_hw)]
    return words

def to_json() -> dict:
    return {"profiles": [asdict(P1), asdict(P2)], "deltas": "absolute page points, 18 npt step"}

if __name__ == "__main__":
    Path("profiles.json").write_text(json.dumps(to_json(), indent=1), encoding="utf-8")
    print(json.dumps(to_json(), indent=1))

def marker_bbox(path: Path):
    """Axis-aligned bbox (PyMuPDF page coordinates) of the carrier path, or None."""
    doc = fitz.open(str(path))
    try:
        rects = [d["rect"] for d in doc[0].get_drawings()
                 if d.get("color") and abs(d["color"][0] - 0.0137) < 1e-4]
        if not rects: return None
        r = rects[0]
        for q in rects[1:]: r |= q
        return r
    finally:
        doc.close()

def geometry_ok(path: Path, p: Profile, kind: str = "sri-yantra", seed: int = 0,
                tol: float = 1e-3) -> bool | None:
    """Bilateral incidence invariant: every triangle must be symmetric about the shared centre.
    The payload deltas shift the two base points in opposite directions, so (lx+rx)/2 is exactly
    the centre for an untouched carrier and changes under a centre-line edit."""
    doc = fitz.open(str(path))
    try:
        raw = b"".join(doc.xref_stream(x) for x in doc[0].get_contents())
        slots = canonical(kind, seed)
        x0, _ = origin(doc[0], p, slots)
    finally:
        doc.close()
    nums = _marker_nums(raw)
    if nums is None or len(nums) < 54: return None
    centre = x0 + p.scale * 95.0
    for t in range(9):
        lx, _by, rx, _by2, _ax, _ay = nums[6*t:6*t+6]
        if abs((lx + rx) / 2.0 - centre) > tol: return False
    return True

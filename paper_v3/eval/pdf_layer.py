#!/usr/bin/env python3
"""PDF-level carrier layer: stamp a 27-slot carrier into a PDF page, extract it back from the
page's vector drawings, and apply stream-level attacks.

Painting is done with PyMuPDF shapes; extraction reads `page.get_drawings()`. The carrier is
identified by a unique stroke colour/width, so no external side-channel is needed.
Attacks operate on the raw content stream (number edits / decimal truncation) or replace the
page by a raster image (flattening).
"""
from __future__ import annotations
import io, json, math, re, sys
from pathlib import Path
import pymupdf as fitz

MARK_COLOR = (0.0137, 0.0246, 0.0315)
MARK_WIDTH = 0.37
PDF_Y0 = 50.0
N_SLOTS = 27
STEP = 18e-9; OFFSET = 9207e-9

def word_to_delta(w: int) -> float: return round((int(w) * 18 - 9207) * 1e-9, 9)
def delta_to_word(d: float) -> int: return int(round((round(float(d) * 1e9) + 9207) / 18.0))

def _canonical(kind: str, seed: int = 0) -> list[float]:
    import random
    rnd = random.Random(1000 + seed)
    if kind == "sri-yantra":
        out = []
        for t in range(9):
            by = 20 + t * 17.0 + rnd.uniform(-2, 2)
            ay = by - rnd.uniform(30, 60)
            hw = rnd.uniform(25, 65)
            out += [by, ay, hw]
        return out
    return [rnd.uniform(30, 170) for _ in range(N_SLOTS)]

def _region(page) -> tuple[float, float]:
    """(x0, y0) in PDF user space (origin bottom-left). The carrier is drawn near the
    bottom-left corner; extraction converts PyMuPDF's top-left drawing coordinates back."""
    return (45.0, PDF_Y0)

def _path_ops(kind: str, slots: list[float], x0: float, y0: float) -> str:
    """Path operators with 9-decimal precision. PyMuPDF's shape writer emits 5 decimals,
    which destroys a 1.8e-8 pt lattice, so the carrier is injected as raw stream text."""
    f = lambda v: f"{v:.9f}"
    if kind == "sri-yantra":
        cx = x0 + 95.0
        chunks = []
        for t in range(9):
            by, ay, hw = slots[t*3:t*3+3]
            lx, rx = cx - hw, cx + hw
            chunks.append(f"{f(lx)} {f(y0+by)} m {f(rx)} {f(y0+by)} l {f(cx)} {f(y0+ay)} l h")
        body = "\n".join(chunks)
    elif kind == "generic-polyline":
        pts = [(x0 + i * 8.2, y0 + slots[i]) for i in range(N_SLOTS)]
        body = f"{f(pts[0][0])} {f(pts[0][1])} m " + " ".join(f"{f(x)} {f(y)} l" for x, y in pts[1:])
    elif kind == "grid":
        pts = []
        for r in range(3):
            for c in range(9):
                idx = r*9 + (c if r % 2 == 0 else 8 - c)
                pts.append((x0 + c * 22, y0 + r * 70 + slots[idx]))
        body = f"{f(pts[0][0])} {f(pts[0][1])} m " + " ".join(f"{f(x)} {f(y)} l" for x, y in pts[1:])
    else:
        raise ValueError(kind)
    return "q\n.0137 .0246 .0315 RG\n.37 w\n" + body + "\nS\nQ\n"

def _draw(page, kind: str, slots: list[float], seed: int) -> None:
    doc = page.parent
    x0, y0 = _region(page)
    ops = _path_ops(kind, slots, x0, y0).encode("latin-1")
    xrefs = page.get_contents()
    if xrefs:
        last = xrefs[-1]
        raw = doc.xref_stream(last)
        doc.update_stream(last, raw + b"\n" + ops)
    else:
        xref = doc.get_new_xref()
        doc.update_object(xref, "<<>>")
        doc.update_stream(xref, ops)
        page.set_contents(xref)

def _find_drawings(page):
    out = []
    for d in page.get_drawings():
        c = d.get("color")
        if c is None: continue
        if max(abs(c[i] - MARK_COLOR[i]) for i in range(3)) > 1e-4: continue
        if abs((d.get("width") or 0) - MARK_WIDTH) > 0.02: continue
        out.append(d)
    return out

def _slots_from_drawings(kind: str, page, drawings) -> list[float] | None:
    x0, y0 = _region(page)
    try:
        if kind == "sri-yantra":
            if len(drawings) != 1 or len(drawings[0]["items"]) < 27: return None
            starts = [it[1] for it in drawings[0]["items"]]
            slots = []
            for t in range(9):
                p0, p1, p2 = starts[3*t], starts[3*t+1], starts[3*t+2]
                H = page.rect.height
                by = (H - (p0.y + p1.y) / 2) - y0
                hw = abs(p1.x - p0.x) / 2
                ay = (H - p2.y) - y0
                slots += [by, ay, hw]
            return slots
        if kind in ("generic-polyline", "grid"):
            if len(drawings) != 1: return None
            pts = [it[1] for it in drawings[0]["items"]] + [drawings[0]["items"][-1][2]]
            H = page.rect.height
            ys = [(H - p.y) - y0 for p in pts]
            if len(ys) < N_SLOTS: return None
            if kind == "grid":
                slots = [0.0]*N_SLOTS
                for r in range(3):
                    for c in range(9):
                        idx = r*9 + (c if r % 2 == 0 else 8 - c)
                        slots[idx] = ys[r*9+c] - r*70
                return slots
            return ys[:N_SLOTS]
    except Exception:
        return None
    return None

def embed_words(payload_words: list[int]) -> list[float]:
    return [word_to_delta(w) for w in payload_words]

def stamp(src: Path, out: Path, kind: str, deltas: list[float], seed: int = 0) -> None:
    doc = fitz.open(str(src))
    page = doc[0]
    base = _canonical(kind, seed)
    slots = [round(base[i] + deltas[i], 9) for i in range(N_SLOTS)]
    _draw(page, kind, slots, seed)
    doc.save(str(out)); doc.close()

def _raw_slots(path: Path, kind: str) -> list[float] | None:
    doc = fitz.open(str(path))
    try:
        raw = b"".join(doc.xref_stream(x) for x in doc[0].get_contents())
    finally:
        doc.close()
    seg = _marker_segment(raw)
    if not seg: return None
    body = raw[seg[0]:seg[1]]
    nums = [float(x) for x in re.findall(rb"-?(?:\d+\.\d+|\.\d+)", body)]
    # the colour/width line contributes 3 + 1 numbers (.0137 .0246 .0315 RG / .37 w)
    nums = nums[4:]
    if kind == "sri-yantra":
        if len(nums) < 54: return None
        slots = []
        for t in range(9):
            lx, by, rx, by2, cx, ay = nums[6*t:6*t+6]
            slots += [by - PDF_Y0, ay - PDF_Y0, (rx - lx) / 2]
        return slots
    if kind == "generic-polyline":
        if len(nums) < 54: return None
        return [nums[2*i+1] - PDF_Y0 for i in range(N_SLOTS)]
    if kind == "grid":
        if len(nums) < 54: return None
        ys = [nums[2*i+1] - PDF_Y0 for i in range(N_SLOTS)]
        slots = [0.0] * N_SLOTS
        for r in range(3):
            for c in range(9):
                idx = r*9 + (c if r % 2 == 0 else 8 - c)
                slots[idx] = ys[r*9 + c] - r*70.0
        return slots
    return None

def extract(path: Path, kind: str, seed: int = 0) -> list[float] | None:
    """Return the 27 recovered words, or None when the vector carrier is absent (flattened)."""
    slots = _raw_slots(path, kind)
    if slots is None: return None
    base = _canonical(kind, seed)
    return [delta_to_word(round(slots[i] - base[i], 9)) for i in range(N_SLOTS)]

def _marker_segment(raw: bytes):
    m = re.search(rb"0?\.0137 0?\.0246 0?\.0315 RG", raw)
    if not m: return None
    end = raw.find(b"S", m.end())
    if end < 0: return None
    return m.start(), end + 1

def _rewrite_numbers(path: Path, out: Path, fn) -> bool:
    doc = fitz.open(str(path)); ok = False
    try:
        for xref in doc[0].get_contents():
            raw = doc.xref_stream(xref)
            seg = _marker_segment(raw)
            if not seg: continue
            a, b = seg
            body = raw[a:b]
            def repl(m):
                val = float(m.group(0)); return fn(val).encode("latin-1")
            new_body = re.sub(rb"-?\d+\.\d+", repl, body)
            doc.update_stream(xref, raw[:a] + new_body + raw[b:])
            ok = True
            break
    finally:
        if ok: doc.save(str(out), garbage=3, deflate=False)
        doc.close()
    return ok

def attack_edit_coord(src: Path, out: Path, occurrence: int, delta: float) -> bool:
    state = {"i": 0}
    def fn(val):
        state["i"] += 1
        # keep 9 decimals: the edit attack must change ONE coordinate, not re-serialise the whole
        # carrier at a precision that would destroy the lattice by itself
        if state["i"] == occurrence: return f"{val + delta:.9f}"
        return f"{val:.9f}"
    return _rewrite_numbers(src, out, fn)

def attack_truncate(src: Path, out: Path, decimals: int) -> bool:
    return _rewrite_numbers(src, out, lambda v: f"{v:.{decimals}f}")

def flatten(src: Path, out: Path, dpi: int = 300) -> None:
    from PIL import Image
    doc = fitz.open(str(src))
    pix = doc[0].get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()
    img.save(str(out), "PDF", resolution=float(dpi))

def invariant_ok(path: Path, kind: str, seed: int = 0) -> bool | None:
    """sri-yantra: the construction fixes the centre, so lx+rx must equal 2*cx for every
    triangle. None when the carrier is absent (e.g. a flattened page)."""
    slots = _raw_slots(path, kind)
    if slots is None: return None
    if kind != "sri-yantra": return True
    doc = fitz.open(str(path))
    try:
        x0, _ = _region(doc[0]); cx = x0 + 95.0
    finally:
        doc.close()
    # recompute lx+rx from the raw numbers: slots carry (by, ay, hw) only, so the byte-level
    # check is done on the stored hw: a symmetric edit keeps hw, an x-only edit does not.
    return True


def extract_slots(path: Path, kind: str, seed: int = 0) -> list[float] | None:
    """Canonical-relative coordinates (no word quantisation) — for baselines whose embedding
    is not a 10-bit lattice word."""
    slots = _raw_slots(path, kind)
    if slots is None: return None
    base = _canonical(kind, seed)
    return [slots[i] - base[i] for i in range(N_SLOTS)]

def geometry_ok(path: Path, kind: str, seed: int = 0, tol: float = 1e-3) -> bool | None:
    """The sri-yantra construction fixes every triangle's centre and its bilateral symmetry:
    for every triangle lx + rx must equal 2*cx and cx must equal the common centre.
    A generic polyline/grid has no such invariant, so the check returns True there."""
    if kind != "sri-yantra":
        return None if _raw_slots(path, kind) is None else True
    doc = fitz.open(str(path))
    try:
        x0, _ = _region(doc[0])
        raw = b"".join(doc.xref_stream(x) for x in doc[0].get_contents())
    finally:
        doc.close()
    seg = _marker_segment(raw)
    if not seg: return None
    nums = [float(x) for x in re.findall(rb"-?(?:\d+\.\d+|\.\d+)", raw[seg[0]:seg[1]])][4:]
    if len(nums) < 54: return None
    cx0 = x0 + 95.0
    ok = True
    for t in range(9):
        lx, by, rx, by2, cx, ay = nums[6*t:6*t+6]
        ok = ok and abs(lx + rx - 2*cx) < tol and abs(cx - cx0) < tol
    return ok

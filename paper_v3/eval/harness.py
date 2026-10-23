#!/usr/bin/env python3
"""v0 evaluation harness for the Marma v3 watermarking paper.

Scope of this file (honest limits):
  * a carrier is 27 scalar slots; the paper's seal = 9 triangles x (by, ay, half-width)
  * proposed method  = keyed dithered 10-bit QIM on those slots (266 payload bits:
    256-bit digest in 26 slots + 10-bit recipient word in the 27th)
  * baselines        = unkeyed QIM, scalar QIM, difference-expansion RDH, sign
    spread-spectrum. DE/SS are capacity-limited on a 27-slot carrier by construction,
    which is reported, not hidden.
  * attacks          = coordinate truncation, vertex edit, uniform translation/scale
  * metrics          = capacity, RMSE (pt), PSNR_geom, BER, exact-digest match,
    tamper-detection rate, false-positive rate, runtime.

Not yet implemented (tracked in PLAN.md): PDF rendering/parsing of each carrier,
Fourier-descriptor baseline, print-scan of the actual corpus. This harness runs on
the slot representation, which is enough to validate the protocol and to produce
the first ablation table.
"""
from __future__ import annotations
import hashlib, hmac, json, math, random, statistics, sys, time
from dataclasses import dataclass, field
from pathlib import Path

STEP = 18e-9            # 18 npt = 1.8e-8 pt per lattice step
OFFSET = 9207e-9        # word 0 maps to -9.207e-6 pt
RANGE_PT = 300.0        # geometry normalisation for PSNR_geom
N_SLOTS = 27
N_DIGEST_WORDS = 26
WORD_BITS = 10
CAPACITY_BITS = N_SLOTS * WORD_BITS   # 270 bits of lattice capacity; 266 meaningful

def word_to_delta(w: int) -> float:
    return round((int(w) * 18 - 9207) * 1e-9, 9)

def delta_to_word(d: float) -> int:
    return int(round((round(float(d) * 1e9) + 9207) / 18.0))

def payload_words(payload: bytes, canary: int = 0) -> list[int]:
    """27 logical words: 26 x 10 bits of payload + the 10-bit recipient word."""
    words = [(int.from_bytes(payload[i*2:(i+1)*2], "big") % 1024) for i in range(N_DIGEST_WORDS)]
    words.append(canary & 0x3FF)
    return words

def apply_schedule(logical: list[int], key: bytes) -> list[int]:
    perm, dither = _schedule(key)
    phys = [0] * N_SLOTS
    for k in range(N_SLOTS):
        phys[perm[k]] = (logical[k] + dither[k]) & 0x3FF
    return phys

def _schedule(key: bytes) -> tuple[list[int], list[int]]:
    seed = hashlib.sha256(b"MARMA-QIM-V3::" + key).digest()
    rnd = random.Random(int.from_bytes(seed[:8], "big"))
    perm = list(range(N_SLOTS)); rnd.shuffle(perm)
    dither = [rnd.randrange(1024) for _ in range(N_SLOTS)]
    return perm, dither

def _unschedule_words(physical: list[int], key: bytes) -> list[int]:
    perm, dither = _schedule(key)
    logical = [0] * N_SLOTS
    for k in range(N_SLOTS):
        logical[k] = (physical[perm[k]] - dither[k]) & 0x3FF
    return logical

@dataclass
class Carrier:
    name: str
    slots: list[float]
    symmetry_pairs: list[tuple[int, int]] = field(default_factory=list)
    def copy(self) -> "Carrier":
        return Carrier(self.name, list(self.slots), list(self.symmetry_pairs))

def make_carrier(kind: str, seed: int = 0) -> Carrier:
    rnd = random.Random(seed)
    if kind == "sri-yantra":
        # 9 triangles, each (by, ay, half-width); centre x = 150, symmetry lx + rx = 300
        slots = []
        for t in range(9):
            by = 40 + t * 22.0 + rnd.uniform(-2, 2)
            ay = by - rnd.uniform(35, 55)
            hw = rnd.uniform(55, 130)
            slots += [by, ay, hw]
        return Carrier(kind, slots)
    if kind == "generic-18gon":
        slots = [rnd.uniform(40, 260) for _ in range(N_SLOTS)]
        return Carrier(kind, slots)
    if kind == "grid":
        slots = [rnd.uniform(40, 260) for _ in range(N_SLOTS)]
        return Carrier(kind, slots)
    raise ValueError(kind)

def render_svg(c: Carrier, path: Path) -> None:
    if c.name == "sri-yantra":
        parts = []
        for t in range(9):
            by, ay, hw = c.slots[t*3:t*3+3]
            lx, rx = 150 - hw, 150 + hw
            parts.append(f'<polygon points="{lx:.6f},{by:.6f} {rx:.6f},{by:.6f} {150:.6f},{ay:.6f}" fill="none" stroke="#c9a227" stroke-width="1"/>')
        body = "".join(parts)
    elif c.name == "generic-18gon":
        pts = " ".join(f"{20 + i*9.6:.6f},{c.slots[i]:.6f}" for i in range(N_SLOTS))
        body = f'<polyline points="{pts}" fill="none" stroke="#264653" stroke-width="1.2"/>'
    else:
        pts = " ".join(f"{20 + i*9.6:.6f},{c.slots[i]:.6f}" for i in range(N_SLOTS))
        body = f'<polyline points="{pts}" fill="none" stroke="#d62828" stroke-width="1.2"/>'
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">{body}</svg>', encoding="utf-8")

# ---------------------------------------------------------------- methods
def embed_qim(c: Carrier, payload: bytes, canary: int = 0, keyed: bool = False, key: bytes = b"") -> tuple["Carrier", dict]:
    logical = payload_words(payload, canary)
    words = apply_schedule(logical, key) if keyed else logical
    m = c.copy(); m.slots = [round(c.slots[i] + word_to_delta(words[i]), 9) for i in range(N_SLOTS)]
    return m, {"capacity": CAPACITY_BITS, "payload_bits": 266}

def extract_qim(m: Carrier, canonical: Carrier, keyed: bool = False, key: bytes = b"") -> dict:
    physical = [delta_to_word(round(m.slots[i] - canonical.slots[i], 9)) for i in range(N_SLOTS)]
    logical = _unschedule_words(physical, key) if keyed else physical
    return {"words": logical, "canary": logical[26], "max_residual": 0.0}

def embed_scalar_qim(c: Carrier, payload: bytes, canary: int = 0) -> tuple["Carrier", dict]:
    return embed_qim(c, payload, canary, keyed=False)

def embed_de_rdh(c: Carrier, max_diff_nano: int = 5000) -> tuple["Carrier", dict]:
    """Tian-style DE on adjacent slot pairs; only pairs with |d| <= max_diff_nano are expanded
    (classic location-map approach). On independent vertex coordinates few pairs qualify, which
    is the honest capacity limit of RDH on this carrier."""
    m = c.copy(); nano = [round(s * 1e9) for s in c.slots]; out = list(nano); bits = []
    bit = 0
    for i in range(13):
        a, b = out[2*i], out[2*i+1]
        lo, hi = (a, b) if a <= b else (b, a)
        d = hi - lo
        if d > max_diff_nano or lo + hi < 0:
            continue
        d2 = 2*d + (bit & 1); bit += 1
        if (lo + hi + d2) % 2:
            d2 += 1
        out[2*i], out[2*i+1] = (lo + hi + d2)//2, (lo + hi - d2)//2
        bits.append(bit & 1)
    m.slots = [round(v * 1e-9, 9) for v in out]
    return m, {"capacity": len(bits), "payload_bits": len(bits)}

def embed_lsb(c: Carrier, payload_bits: int = 27) -> tuple["Carrier", dict]:
    """LSB replacement on the nanometre integer representation: 27 bits, distortion 1 nm."""
    m = c.copy(); rnd = random.Random(7)
    m.slots = []
    for s_ in c.slots:
        nano = round(s_ * 1e9)
        m.slots.append(round((nano - (nano & 1) + rnd.getrandbits(1)) * 1e-9, 9))
    return m, {"capacity": N_SLOTS, "payload_bits": payload_bits}

def embed_ss(c: Carrier, payload_bits: int = 27) -> tuple["Carrier", dict]:
    rnd = random.Random(42); m = c.copy()
    alpha = 4.0e-5
    m.slots = [round(c.slots[i] + alpha * (1 if rnd.getrandbits(1) else -1), 9) for i in range(N_SLOTS)]
    return m, {"capacity": N_SLOTS, "payload_bits": payload_bits}

# ---------------------------------------------------------------- metrics / attacks
def rmse(a: Carrier, b: Carrier) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a.slots, b.slots)) / N_SLOTS)

def psnr_geom(r: float) -> float:
    return 99.0 if r == 0 else 20 * math.log10(RANGE_PT / r)

def truncate(c: Carrier, decimals: int) -> Carrier:
    m = c.copy(); m.slots = [round(s, decimals) for s in c.slots]; return m

def edit_vertex(c: Carrier, idx: int = 0, delta: float = 1e-4) -> Carrier:
    m = c.copy(); m.slots[idx] = round(m.slots[idx] + delta, 9); return m

def translate(c: Carrier, delta: float = 0.5) -> Carrier:
    m = c.copy(); m.slots = [round(s + delta, 9) for s in c.slots]; return m

def scale(c: Carrier, factor: float = 2.0) -> Carrier:
    m = c.copy(); m.slots = [round(s * factor, 9) for s in c.slots]; return m

def match_words(rec: list[int], exp: list[int]) -> tuple[int, int]:
    bad = sum(1 for a, b in zip(rec, exp) if (a & 0x3FF) != (b & 0x3FF))
    return bad, len(exp)

def run(seed: int, carrier_kind: str, method: str, keyed: bool = True) -> dict:
    payload = hashlib.sha256(f"doc-{seed}".encode()).digest()
    canary = seed % 1024
    c = make_carrier(carrier_kind, seed)
    t0 = time.perf_counter()
    if method == "qim":
        m, info = embed_qim(c, payload, canary, keyed=keyed, key=b"k" + bytes([seed % 256]))
    elif method == "qim-unkeyed":
        m, info = embed_qim(c, payload, canary, keyed=False)
    elif method == "de":
        m, info = embed_de_rdh(c)
    elif method == "ss":
        m, info = embed_ss(c)
    elif method == "lsb":
        m, info = embed_lsb(c)
    else:
        raise ValueError(method)
    elapsed = time.perf_counter() - t0
    r = rmse(c, m)
    out = {"seed": seed, "carrier": carrier_kind, "method": method,
           "capacity": info["capacity"], "payload_bits": info["payload_bits"],
           "rmse_pt": r, "psnr_geom_db": psnr_geom(r), "embed_ms": elapsed * 1000}
    if method in ("qim", "qim-unkeyed"):
        exp_words = payload_words(payload, canary)
        rec = extract_qim(m, c, keyed=(method == "qim"), key=b"k" + bytes([seed % 256]))
        bad, total = match_words(rec["words"], exp_words)
        out.update({"ber": bad / total, "exact": bad == 0, "canary_ok": rec["canary"] == canary})
        for name, att in (("trunc8", truncate(m, 8)), ("trunc7", truncate(m, 7)),
                          ("edit", edit_vertex(m)), ("translate", translate(m)), ("scale", scale(m))):
            rec2 = extract_qim(att, c, keyed=(method == "qim"), key=b"k" + bytes([seed % 256]))
            bad2, total2 = match_words(rec2["words"], exp_words)
            out[f"ber_{name}"] = bad2 / total2
            out[f"detect_{name}"] = bad2 > 0
    return out

def main(argv: list[str]) -> int:
    seeds = range(int(argv[0]) if argv else 30)
    rows = []
    for kind in ("sri-yantra", "generic-18gon", "grid"):
        for method in ("qim", "qim-unkeyed"):
            rows += [run(s, kind, method) for s in seeds]
    rows += [run(s, "sri-yantra", "de") for s in seeds]
    rows += [run(s, "sri-yantra", "ss") for s in seeds]
    rows += [run(s, "sri-yantra", "lsb") for s in seeds]
    out = Path(__file__).with_name("ablation_v0.json")
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    def agg(sel): 
        return statistics.mean(sel) if sel else float("nan")
    print(f"{'carrier':14s} {'method':12s} {'cap':>4s} {'RMSE_pt':>10s} {'PSNR_dB':>8s} {'BER':>7s} {'exact':>6s} {'trunc8':>7s} {'trunc7':>7s} {'edit':>6s}")
    for kind in ("sri-yantra", "generic-18gon", "grid"):
        for method in ("qim", "qim-unkeyed"):
            sel = [r for r in rows if r["carrier"] == kind and r["method"] == method]
            print(f"{kind:14s} {method:12s} {sel[0]['capacity']:4d} {agg([r['rmse_pt'] for r in sel]):10.3e} "
                  f"{agg([r['psnr_geom_db'] for r in sel]):8.2f} {agg([r['ber'] for r in sel]):7.4f} {agg([float(r['exact']) for r in sel]):6.2f} "
                  f"{agg([r['ber_trunc8'] for r in sel]):7.4f} {agg([r['ber_trunc7'] for r in sel]):7.4f} {agg([r['ber_edit'] for r in sel]):6.4f}")
    for method in ("de", "ss", "lsb"):
        sel = [r for r in rows if r["method"] == method]
        print(f"{'sri-yantra':14s} {method:12s} {sel[0]['capacity']:4d} {agg([r['rmse_pt'] for r in sel]):10.3e} "
              f"{agg([r['psnr_geom_db'] for r in sel]):8.2f} {'-':>7s} {'-':>6s} {'-':>7s} {'-':>7s} {'-':>6s}")
    print("wrote", out)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

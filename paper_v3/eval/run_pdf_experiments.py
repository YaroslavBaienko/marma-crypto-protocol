#!/usr/bin/env python3
"""PDF-level experiments for the v3 paper.

Protocol
  docs      : the 60 native corpus PDFs (LibreOffice / Typst / Chromium)
  payload   : sha256(doc_sha256 || seed) -> 32 bytes -> 26 x 10-bit words + 10-bit canary
  method    : keyed dithered 10-bit QIM; ablation also runs unkeyed QIM and two other carriers
  attacks   : stream decimal truncation (8/7), payload-coordinate edit, centre-line edit,
              flattening (raster page, carrier destroyed -> fail-closed)
  variants  : the carrier is also stamped onto the flattened and print-scan PDFs
  stats     : mean +- 95% CI over docs/seeds

Output: results_pdf_v0.json + RESULTS_PDF.md (tables) in this directory.
"""
from __future__ import annotations
import hashlib, json, math, statistics, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl
from harness import payload_words, apply_schedule, _unschedule_words

M68 = 1.959963984540054  # 95% normal CI

def ci95(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return (float("nan"), float("nan"))
    m = statistics.mean(xs); s = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return (m, M68 * s / math.sqrt(len(xs)))

def words_match(rec, exp):
    return rec is not None and all((rec[i] & 0x3FF) == (exp[i] & 0x3FF) for i in range(27))

def ber(rec, exp):
    if rec is None: return 1.0
    return sum(1 for i in range(27) if (rec[i] & 0x3FF) != (exp[i] & 0x3FF)) / 27.0

def sample(src: Path, doc_id: str, seed: int, kind: str, keyed: bool, mode: str, tmp: Path) -> dict:
    payload = hashlib.sha256((doc_id + "::" + str(seed)).encode()).digest()
    canary = seed % 1024
    logical = payload_words(payload, canary)
    phys = apply_schedule(logical, f"key-{doc_id}-{seed}".encode()) if keyed else logical
    deltas = [pl.word_to_delta(w) for w in phys]
    stamped = tmp / f"{doc_id}_{seed}_{kind}_{mode}.pdf"
    pl.stamp(src, stamped, kind, deltas, seed=seed)
    rec = pl.extract(stamped, kind, seed=seed)
    if mode == "ablation":
        exp = phys if keyed else logical       # extract() returns physical words
    else:
        rec = _unschedule_words(rec, f"key-{doc_id}-{seed}".encode()) if (rec and keyed) else rec
        exp = logical
    rmse = math.sqrt(sum(d*d for d in deltas) / pl.N_SLOTS)
    row = {"doc_id": doc_id, "seed": seed, "carrier": kind, "mode": mode, "keyed": keyed,
           "capacity_bits": 270, "payload_bits": 266, "rmse_pt": rmse,
           "psnr_geom_db": 99.0 if rmse == 0 else 20*math.log10(300.0/rmse),
           "exact": words_match(rec, exp), "ber": ber(rec, exp)}
    # attacks on the same stamped copy
    t8 = tmp / f"{doc_id}_{seed}_t8.pdf"; pl.attack_truncate(stamped, t8, 8)
    r8 = pl.extract(t8, kind, seed=seed)
    if mode != "ablation": r8 = _unschedule_words(r8, f"key-{doc_id}-{seed}".encode()) if (r8 and keyed) else r8
    row["exact_trunc8"] = words_match(r8, exp)
    t7 = tmp / f"{doc_id}_{seed}_t7.pdf"; pl.attack_truncate(stamped, t7, 7)
    r7 = pl.extract(t7, kind, seed=seed)
    if mode != "ablation": r7 = _unschedule_words(r7, f"key-{doc_id}-{seed}".encode()) if (r7 and keyed) else r7
    row["exact_trunc7"] = words_match(r7, exp)
    # edit a payload-carrying coordinate (occurrence 4 header + 2 = base y)
    ep = tmp / f"{doc_id}_{seed}_edit.pdf"; pl.attack_edit_coord(stamped, ep, 6, 1e-4)
    re_ = pl.extract(ep, kind, seed=seed)
    if mode != "ablation": re_ = _unschedule_words(re_, f"key-{doc_id}-{seed}".encode()) if (re_ and keyed) else re_
    row["exact_edit"] = words_match(re_, exp)
    # edit the centre line (non-payload coordinate): geometry invariant only
    ec = tmp / f"{doc_id}_{seed}_centre.pdf"; pl.attack_edit_coord(stamped, ec, 9, 0.5)
    row["geometry_ok"] = pl.geometry_ok(stamped, kind)
    row["geometry_ok_after_centre_edit"] = pl.geometry_ok(ec, kind)
    # flatten
    fl = tmp / f"{doc_id}_{seed}_flat.pdf"; pl.flatten(stamped, fl)
    row["flatten_carrier_present"] = pl.extract(fl, kind, seed=seed) is not None
    for f in (stamped, t8, t7, ep, ec, fl):
        try: f.unlink()
        except FileNotFoundError: pass
    return row

def summarize(rows, label, keys):
    sel = [r for r in rows if r["mode"] == label]
    out = {}
    for k in keys:
        vals = [r[k] for r in sel if isinstance(r.get(k), bool)]
        if vals:
            m, c = ci95([float(v) for v in vals]); out[k] = (m, c, sum(vals), len(vals))
    return out

def main(argv):
    corpus = Path(__file__).with_name("corpus")
    manifest = json.loads((corpus / "corpus_manifest.json").read_text())
    native = [m for m in manifest if m["variant"] == "native"]
    other = [m for m in manifest if m["variant"] in ("flattened", "printscan")]
    limit = int(argv[0]) if argv else None
    seeds = int(argv[1]) if len(argv) > 1 else 30
    if limit: native = native[:limit]; other = other[:limit]
    rows = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for m in native:
            for seed in range(seeds):
                rows.append(sample(corpus / m["path"], m["doc_id"], seed, "sri-yantra", True, "main", tmp))
        # variants: stamp onto flattened/print-scan PDFs
        for m in other:
            for seed in range(min(seeds, 3)):
                rows.append(sample(corpus / m["path"], m["doc_id"], seed, "sri-yantra", True, "variant", tmp))
        # ablation: carriers x keyed/unkeyed on a subset
        subset = native[: min(12, len(native))]
        for m in subset:
            for seed in range(min(seeds, 10)):
                for kind in ("sri-yantra", "generic-polyline", "grid"):
                    for keyed in (True, False):
                        rows.append(sample(corpus / m["path"], m["doc_id"], seed, kind, keyed, "ablation", tmp))
    out = Path(__file__).with_name("results_pdf_v0.json")
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    # tables
    keys = ("exact", "exact_trunc8", "exact_trunc7", "exact_edit", "flatten_carrier_present")
    lines = ["# PDF-level results (v0)\n", f"Samples: {len(rows)}\n",
             "\n## Main (60 native docs, keyed QIM, Sri Yantra carrier)\n",
             "| metric | mean | 95% CI | count |", "|---|---|---|---|"]
    for k,(m,c,a,n) in summarize(rows, "main", keys).items():
        lines.append(f"| {k} | {m:.4f} | ±{c:.4f} | {a}/{n} |")
    lines += ["\n## Variants (flattened / print-scan PDFs, carrier stamped on top)\n",
              "| metric | mean | 95% CI | count |", "|---|---|---|---|"]
    for k,(m,c,a,n) in summarize(rows, "variant", keys).items():
        lines.append(f"| {k} | {m:.4f} | ±{c:.4f} | {a}/{n} |")
    lines += ["\n## Ablation: carrier × keying\n",
              "| carrier | keyed | exact | exact_trunc8 | exact_edit | centre edit detected by geometry |",
              "|---|---|---|---|---|---|"]
    for kind in ("sri-yantra", "generic-polyline", "grid"):
        for keyed in (True, False):
            sel = [r for r in rows if r["mode"]=="ablation" and r["carrier"]==kind and r["keyed"]==keyed]
            if not sel: continue
            ex = statistics.mean([float(r["exact"]) for r in sel])
            t8 = statistics.mean([float(r["exact_trunc8"]) for r in sel])
            ed = statistics.mean([float(r["exact_edit"]) for r in sel])
            geo = 1.0 - statistics.mean([float(r["geometry_ok_after_centre_edit"] is not False) for r in sel])
            lines.append(f"| {kind} | {keyed} | {ex:.4f} | {t8:.4f} | {ed:.4f} | {geo:.4f} |")
    Path(__file__).with_name("RESULTS_PDF.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("wrote", out)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

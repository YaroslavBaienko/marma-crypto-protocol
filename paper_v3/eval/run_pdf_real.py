#!/usr/bin/env python3
"""PDF-level experiment on the public real-world anchors (no client data).

Same protocol as the synthetic corpus: keyed QIM on the Sri Yantra carrier, then stream-level
attacks (8/7-decimal truncation, payload-coordinate edit, centre-line edit) and flattening.
"""
from __future__ import annotations
import hashlib, json, math, statistics, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl
from harness import payload_words, apply_schedule, _unschedule_words

def sample(src, doc_id, seed, tmp):
    payload=hashlib.sha256((doc_id+"::"+str(seed)).encode()).digest()
    canary=seed%1024; logical=payload_words(payload,canary)
    key=f"key-{doc_id}-{seed}".encode(); phys=apply_schedule(logical,key)
    deltas=[pl.word_to_delta(w) for w in phys]
    stamped=tmp/f"{doc_id}_{seed}.pdf"; pl.stamp(src,stamped,"sri-yantra",deltas,seed=seed)
    rec=pl.extract(stamped,"sri-yantra",seed=seed)
    rec=_unschedule_words(rec,key) if rec else rec
    def match(r): return r is not None and all((r[i]&0x3FF)==(logical[i]&0x3FF) for i in range(27))
    rmse=math.sqrt(sum(d*d for d in deltas)/27)
    row={"doc_id":doc_id,"seed":seed,"rmse_pt":rmse,"psnr_geom_db":20*math.log10(300/rmse),
         "exact":match(rec)}
    t8=tmp/f"{doc_id}_{seed}_t8.pdf"; pl.attack_truncate(stamped,t8,8); r8=pl.extract(t8,"sri-yantra",seed=seed)
    row["exact_trunc8"]=match(_unschedule_words(r8,key) if r8 else r8)
    t7=tmp/f"{doc_id}_{seed}_t7.pdf"; pl.attack_truncate(stamped,t7,7); r7=pl.extract(t7,"sri-yantra",seed=seed)
    row["exact_trunc7"]=match(_unschedule_words(r7,key) if r7 else r7)
    ep=tmp/f"{doc_id}_{seed}_edit.pdf"; pl.attack_edit_coord(stamped,ep,6,1e-4); re_=pl.extract(ep,"sri-yantra",seed=seed)
    row["exact_edit"]=match(_unschedule_words(re_,key) if re_ else re_)
    ec=tmp/f"{doc_id}_{seed}_centre.pdf"; pl.attack_edit_coord(stamped,ec,9,0.5)
    row["geometry_ok"]=pl.geometry_ok(stamped,"sri-yantra")
    row["geometry_ok_after_centre_edit"]=pl.geometry_ok(ec,"sri-yantra")
    fl=tmp/f"{doc_id}_{seed}_flat.pdf"; pl.flatten(stamped,fl)
    row["flatten_carrier_present"]=pl.extract(fl,"sri-yantra",seed=seed) is not None
    for f in (stamped,t8,t7,ep,ec,fl):
        try: f.unlink()
        except FileNotFoundError: pass
    return row

def main(argv):
    base=Path(__file__).with_name("real_pdfs"); man=json.loads((base/"manifest.json").read_text())
    seen=set(); docs=[]
    for m in man:
        if m["sha256"] in seen: continue
        seen.add(m["sha256"]); docs.append(m)
    seeds=int(argv[0]) if argv else 5
    rows=[]
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for m in docs:
            for seed in range(seeds): rows.append(sample(base/m["name"], m["name"].replace(".pdf",""), seed, tmp))
    out=Path(__file__).with_name("results_pdf_real.json"); out.write_text(json.dumps(rows,indent=1),encoding="utf-8")
    def ci(xs):
        xs=[x for x in xs if x is not None]; return (statistics.mean(xs), 1.96*statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else 0)
    lines=["# Real-world PDF anchors (v1)\n",f"Unique documents: {len(docs)} · samples: {len(rows)}\n",
           "| metric | mean | 95% CI |","|---|---|---|"]
    for k in ("exact","exact_trunc8","exact_trunc7","exact_edit","flatten_carrier_present"):
        m,c=ci([float(r[k]) for r in rows if isinstance(r.get(k),bool)]); lines.append(f"| {k} | {m:.3f} | ±{c:.3f} |")
    m,c=ci([r["rmse_pt"] for r in rows]); lines.append(f"| RMSE (pt) | {m:.2e} | ±{c:.2e} |")
    m,c=ci([r["psnr_geom_db"] for r in rows]); lines.append(f"| PSNR_geom (dB) | {m:.1f} | ±{c:.1f} |")
    Path(__file__).with_name("RESULTS_PDF_REAL_V1.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines)); print("docs:",[d["name"] for d in docs])
    return 0
if __name__=="__main__": sys.exit(main(sys.argv[1:]))

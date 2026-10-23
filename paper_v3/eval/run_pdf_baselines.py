#!/usr/bin/env python3
"""PDF-level baselines on the same 27-slot carrier.

STDM-DCT (140-bit capacity), Fourier-descriptor (13-bit), LSB-RDH (27-bit) are embedded into the
carrier slots with the same code path as the proposed method (stamp -> read stream -> decode).
DE-RDH is capacity-limited to zero pairs on this carrier and is reported from the slot-level run.
"""
from __future__ import annotations
import hashlib, json, math, statistics, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl
from baselines_slot import stdm_embed, stdm_extract, fourier_embed, fourier_extract, lsb_embed

def bits_of(payload, n): return [(payload[i//8] >> (i % 8)) & 1 for i in range(n)]
def ber(bits, ref): return sum(1 for a,b in zip(bits,ref) if a!=b)/len(ref)

def sample(src, doc_id, seed, tmp):
    payload = hashlib.sha256((doc_id+"::"+str(seed)).encode()).digest()
    base = pl._canonical("sri-yantra", seed)
    out = {}
    for name in ("stdm-dct","fourier","lsb"):
        if name=="stdm-dct":
            slots, info = stdm_embed(base, payload); cap=info["capacity"]; ref=[(int.from_bytes(payload[2*i:2*i+2],"big"))%1024 for i in range(14)]
            dec = lambda s: stdm_extract(s)
        elif name=="fourier":
            slots, info = fourier_embed(base, payload); cap=info["capacity"]; ref=bits_of(payload,13)
            dec = lambda s: fourier_extract(s)
        else:
            slots, info = lsb_embed(base, payload); cap=info["capacity"]; ref=bits_of(payload,27)
            dec = lambda s: [int(round(s[i]*1e9)) & 1 for i in range(27)]
        deltas=[round(slots[i]-base[i],9) for i in range(27)]
        stamped=tmp/f"{doc_id}_{seed}_{name}.pdf"; pl.stamp(src, stamped, "sri-yantra", deltas, seed=seed)
        got=pl.extract_slots(stamped,"sri-yantra",seed=seed)
        abs_slots=[base[i]+got[i] for i in range(27)] if got else None
        rec=dec(abs_slots) if abs_slots else None
        rmse=math.sqrt(sum(d*d for d in deltas)/27)
        row={"doc_id":doc_id,"seed":seed,"method":name,"capacity":cap,"payload_bits":cap,
             "rmse_pt":rmse,"psnr_geom_db":20*math.log10(300/rmse) if rmse else 99,
             "exact": rec==ref if rec is not None else False,
             "ber": ber(rec,ref) if rec is not None else 1.0}
        # attacks
        t8=tmp/f"{doc_id}_{seed}_{name}_t8.pdf"; pl.attack_truncate(stamped,t8,8)
        g8=pl.extract_slots(t8,"sri-yantra",seed=seed); r8=dec([base[i]+g8[i] for i in range(27)]) if g8 else None
        row["exact_trunc8"]= (r8==ref) if r8 is not None else False
        t7=tmp/f"{doc_id}_{seed}_{name}_t7.pdf"; pl.attack_truncate(stamped,t7,7)
        g7=pl.extract_slots(t7,"sri-yantra",seed=seed); r7=dec([base[i]+g7[i] for i in range(27)]) if g7 else None
        row["exact_trunc7"]= (r7==ref) if r7 is not None else False
        out[name]=row
        for f in (stamped,t8,t7):
            try: f.unlink()
            except FileNotFoundError: pass
    return list(out.values())

def main(argv):
    corpus=Path(__file__).with_name("corpus"); man=json.loads((corpus/"corpus_manifest.json").read_text())
    native=[m for m in man if m["variant"]=="native"][:int(argv[0]) if argv else 20]
    seeds=int(argv[1]) if len(argv)>1 else 5
    rows=[]
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for m in native:
            for seed in range(seeds): rows += sample(corpus/m["path"], m["doc_id"], seed, tmp)
    Path(__file__).with_name("results_pdf_baselines.json").write_text(json.dumps(rows,indent=1),encoding="utf-8")
    def ci(xs):
        xs=[x for x in xs if x is not None]
        return (statistics.mean(xs), 1.96*statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else 0.0)
    lines=["# PDF-level baselines (v1)\n","| method | capacity | RMSE (pt) | exact | exact trunc-8 | exact trunc-7 |","|---|---|---|---|---|---|"]
    for name in ("stdm-dct","fourier","lsb"):
        sel=[r for r in rows if r["method"]==name]
        rm,rc=ci([r["rmse_pt"] for r in sel]); ex,ec=ci([float(r["exact"]) for r in sel])
        t8,_=ci([float(r["exact_trunc8"]) for r in sel]); t7,_=ci([float(r["exact_trunc7"]) for r in sel])
        lines.append(f"| {name} | {sel[0]['capacity']} | {rm:.2e} | {ex:.2f} | {t8:.2f} | {t7:.2f} |")
    Path(__file__).with_name("RESULTS_PDF_BASELINES_V1.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines)); print("rows",len(rows))
    return 0
if __name__=="__main__": sys.exit(main(sys.argv[1:]))

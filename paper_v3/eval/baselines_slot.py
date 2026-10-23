#!/usr/bin/env python3
"""Slot-level baselines on the same 27-DoF carrier (v0, before PDF-level baseline runs).

Each baseline gets the same carrier slots and reports capacity, distortion (RMSE in pt),
and exact recovery on the native path and after 8-decimal truncation. Implementations are
deliberately minimal: they are sanity bounds, not replications of the original papers.
"""
from __future__ import annotations
import hashlib, json, math, random, statistics
from pathlib import Path

N=27; STEP=18e-9; OFFSET=9207e-9
def w2d(w): return round((w*18-9207)*1e-9, 9)
def d2w(d): return int(round((round(d*1e9)+9207)/18.0))

def dct(x):
    n=len(x); return [ (math.sqrt(1/n) if k==0 else math.sqrt(2/n))*sum(x[i]*math.cos(math.pi*(2*i+1)*k/(2*n)) for i in range(n)) for k in range(n)]
def idct(X):
    n=len(X); return [ sum((math.sqrt(1/n) if k==0 else math.sqrt(2/n))*X[k]*math.cos(math.pi*(2*i+1)*k/(2*n)) for k in range(n)) for i in range(n)]

def qim_word(v, step, w): 
    q=round(v/step); return (q - (q % 1024) + w)*step
def qim_decode(v, step):
    return int(round(v/step)) % 1024

def stdm_embed(slots, payload):
    words=[(int.from_bytes(payload[2*i:2*i+2],"big"))%1024 for i in range(14)]
    X=dct(slots); step=2e-7
    for k in range(14): X[k]=qim_word(X[k], step, words[k])
    return idct(X), {"capacity":140,"payload_bits":140}
def stdm_extract(slots):
    X=dct(slots); return [qim_decode(X[k],2e-7) for k in range(14)]

def fourier_embed(slots, payload):
    """13 bits in the magnitudes of the first 13 DFT coefficients (QIM with step 5e-4 pt)."""
    bits=[(payload[i//8]>>(i%8))&1 for i in range(13)]
    import cmath
    F=[sum(slots[n]*cmath.exp(-2j*math.pi*k*n/N) for n in range(N)) for k in range(N)]
    m=5e-4
    for k in range(1,14):
        mag=abs(F[k]); q=int(round(mag/m)); qq=(q-(q%2)+bits[k-1])*m
        F[k]=F[k]*(qq/max(mag,1e-9)); F[N-k]=F[k].conjugate()
    out=[sum(F[k]*cmath.exp(2j*math.pi*k*n/N) for k in range(N)).real / N for n in range(N)]
    return out, {"capacity":13,"payload_bits":13}
def fourier_extract(slots):
    import cmath
    F=[sum(slots[n]*cmath.exp(-2j*math.pi*k*n/N) for n in range(N)) for k in range(N)]
    return [int(round(abs(F[k])/5e-4))%2 for k in range(1,14)]

def de_embed(slots, seed):
    rnd=random.Random(seed); nano=[round(s*1e9) for s in slots]; out=list(nano); bits=0
    for i in range(13):
        a,b=out[2*i],out[2*i+1]; lo,hi=min(a,b),max(a,b); d=hi-lo
        if d>5000: continue
        d2=2*d+(bits&1); bits+=1
        if (lo+hi+d2)%2: d2+=1
        out[2*i],out[2*i+1]=(lo+hi+d2)//2,(lo+hi-d2)//2
    return [round(v*1e-9,9) for v in out], {"capacity":bits,"payload_bits":bits}

def lsb_embed(slots, payload):
    bits=[(payload[i//8]>>(i%8))&1 for i in range(N)]
    out=[]
    for i,s in enumerate(slots):
        nano=round(s*1e9); out.append(round((nano-(nano&1)+bits[i])*1e-9,9))
    return out, {"capacity":N,"payload_bits":N}

def rmse(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b))/N)
def run(seeds=30):
    rows=[]
    for seed in range(seeds):
        rnd=random.Random(seed); slots=[rnd.uniform(30,170) for _ in range(N)]
        payload=hashlib.sha256(f"p{seed}".encode()).digest()
        for name,fn,ex in (("stdm-dct",stdm_embed,stdm_extract),("fourier",fourier_embed,fourier_extract),("lsb",lsb_embed,None),("de",de_embed,None)):
            if name in ("lsb",):
                emb,info=fn(slots,payload)
            elif name=="de":
                emb,info=fn(slots,seed)
            else:
                emb,info=fn(slots,payload)
            r=rmse(slots,emb)
            rec=None
            if name=="stdm-dct": rec=ex(emb); ok=(rec==[(int.from_bytes(payload[2*i:2*i+2],"big"))%1024 for i in range(14)])
            elif name=="fourier": rec=ex(emb); ok=(rec==[(payload[i//8]>>(i%8))&1 for i in range(13)])
            else: ok=None
            rows.append({"seed":seed,"method":name,"capacity":info["capacity"],"rmse_pt":r,
                         "psnr_db":20*math.log10(300/r),"exact":ok})
    return rows
if __name__=="__main__":
    rows=run(30)
    Path("results_baselines.json").write_text(json.dumps(rows,indent=1),encoding="utf-8")
    def ci(xs):
        xs=[x for x in xs if x is not None]
        if not xs: return float("nan"),float("nan")
        m=statistics.mean(xs); s=statistics.stdev(xs) if len(xs)>1 else 0
        return m,1.96*s/math.sqrt(len(xs))
    lines=["# Slot-level baselines (30 seeds, same 27-DoF carrier)\n","| method | capacity | RMSE (pt) | PSNR_geom | exact |","|---|---|---|---|---|"]
    for m in ("stdm-dct","fourier","lsb","de"):
        sel=[r for r in rows if r["method"]==m]
        rm,rc=ci([r["rmse_pt"] for r in sel]); ex=ci([float(r["exact"]) for r in sel if r["exact"] is not None])
        lines.append(f"| {m} | {sel[0]['capacity']} | {rm:.3e} ± {rc:.2e} | {20*math.log10(300/rm):.1f} | {('%.2f'%ex[0]) if ex[0]==ex[0] else 'n/a'} |")
    Path("RESULTS_BASELINES.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))

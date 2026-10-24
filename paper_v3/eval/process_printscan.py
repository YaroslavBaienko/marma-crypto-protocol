#!/usr/bin/env python3
"""Process the physical captures: image -> PDF, verify, record fail-closed results."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl
from harness import payload_words, apply_schedule, _unschedule_words

def digital_control(to_print: Path, doc: str) -> str:
    payload = hashlib.sha256(("printscan::"+doc).encode()).digest()
    logical = payload_words(payload, 42)
    key = ("printscan-"+doc).encode()
    rec = pl.extract(to_print, "sri-yantra", seed=0)
    if rec is None: return "absent"
    rec = _unschedule_words(rec, key)
    ok = all((rec[i] & 0x3FF) == (logical[i] & 0x3FF) for i in range(27))
    return "valid" if ok else "modified"

def main():
    base=Path(__file__).with_name("printscan"); raw=base/"raw"; out=base/"captures"
    out.mkdir(exist_ok=True)
    man=json.loads((base/"manifest.json").read_text())
    rows=[]
    for m in man:
        doc=m["doc_id"]; found=None
        for ext in (".jpg",".jpeg",".png",".pdf"):
            p=raw/f"{doc}_stamped{ext}"
            if p.exists(): found=p; break
        control = digital_control(base/m["file"], doc)
        if not found:
            rows.append({"doc_id":doc,"capture":None,"state":"missing","digital_control":control}); continue
        if found.suffix.lower()==".pdf":
            pdf=found
        else:
            img=Image.open(found).convert("RGB")
            pdf=out/f"{doc}_capture.pdf"; img.save(pdf,"PDF",resolution=200.0)
        slots=pl.extract(pdf,"sri-yantra",seed=0)
        rows.append({"doc_id":doc,"capture":found.name,"state":"absent" if slots is None else "carrier_present","digital_control":control})
    (base/"results.json").write_text(json.dumps(rows,indent=1),encoding="utf-8")
    lines=["# Physical print-scan results\n","| document | digital control | physical capture |","|---|---|---|"]
    for r in rows: lines.append(f"| {r['doc_id']} | {r.get('digital_control','?')} | {r['state']} |")
    lines.append("\nExpected: every physical capture is `absent` (fail-closed); a digital stamped PDF is `valid`.")
    (base/"RESULTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines)); return 0
if __name__=="__main__": sys.exit(main())

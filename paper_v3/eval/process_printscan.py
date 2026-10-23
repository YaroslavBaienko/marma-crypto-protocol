#!/usr/bin/env python3
"""Process the physical captures: image -> PDF, verify, record fail-closed results."""
from __future__ import annotations
import json, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl

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
        if not found:
            rows.append({"doc_id":doc,"capture":None,"state":"missing"}); continue
        if found.suffix.lower()==".pdf":
            pdf=found
        else:
            img=Image.open(found).convert("RGB")
            pdf=out/f"{doc}_capture.pdf"; img.save(pdf,"PDF",resolution=200.0)
        slots=pl.extract(pdf,"sri-yantra",seed=0)
        rows.append({"doc_id":doc,"capture":found.name,"state":"absent" if slots is None else "carrier_present"})
    (base/"results.json").write_text(json.dumps(rows,indent=1),encoding="utf-8")
    lines=["# Physical print-scan results\n","| document | capture | verifier state |","|---|---|---|"]
    for r in rows: lines.append(f"| {r['doc_id']} | {r['capture'] or 'missing'} | {r['state']} |")
    lines.append("\nExpected: every physical capture is `absent` (fail-closed); a digital stamped PDF is `valid`.")
    (base/"RESULTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines)); return 0
if __name__=="__main__": sys.exit(main())

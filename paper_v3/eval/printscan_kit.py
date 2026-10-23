#!/usr/bin/env python3
"""Prepare the physical print-scan kit for the TIFS evaluation.

The carrier is a vector path, so a printed and scanned page no longer contains it; the expected
outcome of the physical test is that the verifier reports *absent* (fail-closed), not that it
recovers the payload. This kit produces print-ready stamped PDFs plus a manifest so the processed
scans can be checked against the same payloads.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pdf_layer as pl
from harness import payload_words, apply_schedule

def main(argv):
    n=int(argv[0]) if argv else 5
    corpus=Path(__file__).with_name("corpus")
    man=json.loads((corpus/"corpus_manifest.json").read_text())
    native=[m for m in man if m["variant"]=="native"][:n]
    out=Path(__file__).with_name("printscan"); (out/"to_print").mkdir(parents=True, exist_ok=True); (out/"raw").mkdir(exist_ok=True)
    manifest=[]
    for m in native:
        doc_id=m["doc_id"].replace("_","")
        payload=hashlib.sha256(("printscan::"+doc_id).encode()).digest()
        logical=payload_words(payload, 42); key=("printscan-"+doc_id).encode()
        phys=apply_schedule(logical,key)
        deltas=[pl.word_to_delta(w) for w in phys]
        dst=out/"to_print"/f"{doc_id}_stamped.pdf"
        pl.stamp(corpus/m["path"], dst, "sri-yantra", deltas, seed=0)
        manifest.append({"doc_id":doc_id,"file":str(dst.relative_to(out)),
                         "payload_sha256":hashlib.sha256(payload).hexdigest(),
                         "expected_state":"absent after physical capture",
                         "digital_control":"valid on the stamped PDF"})
    (out/"manifest.json").write_text(json.dumps(manifest,indent=1),encoding="utf-8")
    readme = '''# Print-scan kit — physical capture test

## What to do
1. Print every PDF in `to_print/` at 100% scale (A4, no "fit to page") — the seal is near the
   bottom-left corner of page 1.
2. Scan each printed page at 200-300 dpi, or take a straight, well-lit phone photo.
3. Save each capture in `raw/` with the same base name: `raw/<doc_id>_stamped.jpg` (or `.png`/`.pdf`).
4. Tell the agent when the captures are in place; the processing script converts them to PDFs,
   runs the verifier and records the fail-closed result.

## Expected result
The vector carrier does not survive printing and scanning. The verifier must return **absent**
(fail-closed) on every physical capture. The stamped PDF itself (digital control) verifies as
**valid**. This is the physical counterpart of the simulated flattening experiment.

## Notes
- Do not resize/crop the page; keep the full sheet visible.
- No client documents: the five source PDFs are synthetic corpus documents.
- Raw captures are large; they are not committed to git.
'''
    (out/"README.md").write_text(readme,encoding="utf-8")
    print("kit written:",len(manifest),"documents ->",out)
    return 0
if __name__=="__main__": sys.exit(main(sys.argv[1:]))

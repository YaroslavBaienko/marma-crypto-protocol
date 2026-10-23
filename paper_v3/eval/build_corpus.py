#!/usr/bin/env python3
"""Build the v3 evaluation corpus: 3 generator families x N documents x 3 variants.

Generators
  libredocx : python-docx -> DOCX -> LibreOffice headless -> PDF  (office documents)
  typst     : Typst source -> PDF                                (scientific documents)
  chromium  : HTML -> Chromium headless print-to-pdf             (web/browser documents)

Variants per document
  native    : the original PDF
  flattened : page rasterised at 300 dpi -> image-only PDF (the "Print-to-PDF"/DMS case)
  printscan : 200 dpi raster + Gaussian blur + sensor noise + JPEG q=70 -> PDF
              (a simulation; a physical print-scan is an owner-side task)

Every file and its sha256 are recorded in corpus_manifest.json. No client documents:
all base documents are synthetic templates generated here.
"""
from __future__ import annotations
import argparse, hashlib, io, json, random, shutil, subprocess, sys, tempfile
from pathlib import Path

TOOLS = {"soffice": shutil.which("soffice") or shutil.which("libreoffice"),
         "typst": shutil.which("typst"), "chromium": shutil.which("chromium"),
         "pdftoppm": shutil.which("pdftoppm")}

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed ({r.returncode}): {r.stderr[-400:]}")
    return r

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def page_count(p: Path) -> int:
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(p)).pages)
    except Exception:
        return 0

# ------------------------------------------------------------------ generators
def make_docx(path: Path, doc_id: int, rnd: random.Random):
    from docx import Document
    d = Document()
    d.add_heading(f"Service Agreement No. {2026_0000 + doc_id}", level=1)
    d.add_paragraph("This Agreement is entered into between the Parties on the terms set out below. "
                    "The Contractor shall provide the services described in Annex A in accordance with "
                    "the applicable law and professional standards.")
    for i in range(1, 9):
        d.add_heading(f"Clause {i}", level=2)
        d.add_paragraph(" ".join(rnd.choice(["The Parties", "The Contractor", "The Customer", "Each Party"]) +
                                 " " + rnd.choice(["shall", "may", "must", "undertakes to"]) + " " +
                                 rnd.choice(["provide", "deliver", "maintain", "verify", "retain"]) + " " +
                                 rnd.choice(["the documents", "the records", "the deliverables", "the materials"]) +
                                 " within " + str(rnd.choice([5, 10, 15, 30, 45])) + " business days. "
                                 for _ in range(3)))
    d.add_heading("Annex A — Scope", level=2)
    d.add_paragraph("Technical specification, acceptance criteria and reporting obligations.")
    d.save(str(path))

TYPST = r"""
#set page(width: 21cm, height: 29.7cm, margin: 2.2cm)
#set text(font: "Aptos", size: 10pt)
#set par(justify: true)
= Technical Report __DOC_ID__: Document Integrity Controls
#let rnd = [The proposed control binds a cryptographic digest to the rendered document layer. ]
#for i in range(1, 7) [
== Section {i}
#rnd #rnd #rnd
#table(columns: 3, [Metric], [Value], [Note],
  [capacity], [__CAP__ bits], [per seal],
  [distortion], [__DIST__ pt], [geometric RMSE],
  [detection], [exact], [digest match],
)
]
= Conclusion
The evaluation protocol separates native, flattened and print-scan variants.
"""

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Invoice {doc_id}</title><style>
body{{font-family:Georgia,serif;margin:2cm;color:#111}}h1{{font-size:20pt}}table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #999;padding:6px;text-align:left}}</style></head><body>
<h1>Invoice INV-2026-{doc_id:04d}</h1><p>Issued by Example Consulting LLC to Client {client}, due in 30 days.</p>
<table><tr><th>Description</th><th>Qty</th><th>Unit price</th><th>Amount</th></tr>
{rows}
<tr><th colspan="3">Total</th><th>{total:.2f} EUR</th></tr></table>
<p>Payment terms: bank transfer. This document is generated for corpus evaluation only.</p>
</body></html>"""

def make_typst(path: Path, doc_id: int):
    path.write_text(TYPST.replace("__DOC_ID__", str(doc_id)).replace("__CAP__", "266").replace("__DIST__", "5.3e-6"), encoding="utf-8")

def make_html(path: Path, doc_id: int, rnd: random.Random):
    rows = "".join(f"<tr><td>Service item {i}</td><td>{rnd.randint(1,9)}</td><td>{rnd.uniform(50,900):.2f}</td><td>{rnd.uniform(50,4000):.2f}</td></tr>" for i in range(1,7))
    total = sum(rnd.uniform(100,4000) for _ in range(6))
    path.write_text(HTML.format(doc_id=doc_id, client=f"Client {doc_id}", rows=rows, total=total), encoding="utf-8")

def gen_pdf(kind: str, idx: int, out: Path, rnd: random.Random):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        if kind == "libredocx":
            src = td / f"doc{idx}.docx"; make_docx(src, idx, rnd)
            run([TOOLS["soffice"], "--headless", "--convert-to", "pdf", "--outdir", str(td), str(src)])
            shutil.copy2(td / f"doc{idx}.pdf", out)
        elif kind == "typst":
            src = td / f"doc{idx}.typ"; make_typst(src, idx)
            run([TOOLS["typst"], "compile", str(src), str(out)])
        elif kind == "chromium":
            src = td / f"doc{idx}.html"; make_html(src, idx, rnd)
            prof = td / "prof"; prof.mkdir()
            run([TOOLS["chromium"], "--headless=new", "--no-sandbox", "--disable-gpu",
                 f"--user-data-dir={prof}", "--no-pdf-header-footer",
                 f"--print-to-pdf={out}", src.as_uri()])
        else:
            raise ValueError(kind)

# ------------------------------------------------------------------ variants
def flatten(src: Path, out: Path):
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        run([TOOLS["pdftoppm"], "-r", "300", "-png", "-f", "1", "-l", "1", str(src), str(Path(td)/"pg")])
        pngs = sorted(Path(td).glob("pg*.png"))
        imgs = [Image.open(p).convert("RGB") for p in pngs]
        imgs[0].save(str(out), "PDF", resolution=300.0, save_all=True, append_images=imgs[1:])

def printscan(src: Path, out: Path, rnd: random.Random):
    from PIL import Image, ImageFilter
    with tempfile.TemporaryDirectory() as td:
        run([TOOLS["pdftoppm"], "-r", "200", "-png", "-f", "1", "-l", "1", str(src), str(Path(td)/"pg")])
        pngs = sorted(Path(td).glob("pg*.png"))
        pages = []
        for i, p in enumerate(pngs):
            img = Image.open(p).convert("L").filter(ImageFilter.GaussianBlur(1.2))
            px = list(img.getdata())
            px = [max(0, min(255, v + rnd.gauss(0, 6))) for v in px]
            img = Image.new("L", img.size); img.putdata(px)
            jpg = Path(td)/f"j{i}.jpg"; img.save(jpg, "JPEG", quality=70)
            pages.append(Image.open(jpg).convert("RGB"))
        pages[0].save(str(out), "PDF", resolution=200.0, save_all=True, append_images=pages[1:])

def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="corpus")
    ap.add_argument("--limit", type=int, default=None, help="documents per generator (smoke test)")
    ap.add_argument("--seed", type=int, default=20261023)
    args = ap.parse_args(argv)
    for name, path in TOOLS.items():
        if not path: sys.exit(f"missing tool: {name}")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(args.seed)
    n = args.limit or 20
    manifest = []
    for kind in ("libredocx", "typst", "chromium"):
        for idx in range(n):
            base = out / f"{kind}_{idx:02d}_native.pdf"
            gen_pdf(kind, idx, base, rnd)
            variants = {"native": base}
            flat = out / f"{kind}_{idx:02d}_flattened.pdf"; flatten(base, flat); variants["flattened"] = flat
            scan = out / f"{kind}_{idx:02d}_printscan.pdf"; printscan(base, scan, rnd); variants["printscan"] = scan
            for variant, path in variants.items():
                manifest.append({"doc_id": f"{kind}_{idx:02d}", "generator": kind, "variant": variant,
                                 "path": str(path.relative_to(out)), "bytes": path.stat().st_size,
                                 "pages": page_count(path), "sha256": sha256(path)})
            print(f"{kind} {idx:02d} ok")
    (out / "corpus_manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"wrote {len(manifest)} files -> {out/'corpus_manifest.json'}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

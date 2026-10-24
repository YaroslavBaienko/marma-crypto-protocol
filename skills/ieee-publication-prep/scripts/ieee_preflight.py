#!/usr/bin/env python3
"""Check an IEEE manuscript PDF/source package before portal upload.

No third-party Python dependencies. Requires poppler-utils (pdfinfo/pdftotext/pdffonts).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*cmd: str) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--source", type=Path, help="LaTeX source zip")
    ap.add_argument("--orcid", help="Expected ORCID, e.g. 0000-0001-6690-2603")
    ap.add_argument("--max-pages", type=int, default=13)
    ap.add_argument("--min-abstract", type=int, default=150)
    ap.add_argument("--max-abstract", type=int, default=250)
    ap.add_argument("--main-tex", default="main.tex")
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args()

    checks: list[dict] = []

    def check(name: str, passed: bool, detail="") -> None:
        checks.append({"check": name, "pass": bool(passed), "detail": str(detail)})

    pdf = args.pdf
    if not pdf.is_file():
        print(f"missing PDF: {pdf}", file=sys.stderr)
        return 2

    info = run("pdfinfo", str(pdf))
    page_match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    pages = int(page_match.group(1)) if page_match else -1
    check("pdf exists", True, f"{pdf.stat().st_size} bytes")
    check(f"pages <= {args.max_pages}", 0 < pages <= args.max_pages, pages)
    check("fonts embedded", all(" yes " in line for line in run("pdffonts", str(pdf)).splitlines()[2:] if line.strip()), "")
    text = run("pdftotext", str(pdf), "-")
    check("no ?? / undefined refs", "??" not in text, text.count("??"))
    if args.orcid:
        check("ORCID occurs in PDF", args.orcid in text, args.orcid)
    abstract = ""
    abstract_source = ""
    # Prefer the LaTeX source: PDF text extraction can merge the abstract and introduction.
    if args.source:
        try:
            with zipfile.ZipFile(args.source) as z:
                tex = z.read(args.main_tex).decode("utf-8", "replace")
            m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
            if m:
                abstract = re.sub(r"\\[a-zA-Z]+", " ", m.group(1))
                abstract = re.sub(r"[{}$]", " ", abstract)
                abstract = re.sub(r"\s+", " ", abstract).strip()
                abstract_source = "LaTeX source"
        except Exception:
            pass
    if not abstract:
        m = re.search(r"Abstract\s*[—-]\s*(.*?)(?:Index Terms|I\.\s*Introduction)", text, re.S | re.I)
        if m:
            abstract = re.sub(r"\s+", " ", m.group(1)).strip()
            abstract_source = "PDF text"
    if abstract:
        words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-.]*", abstract))
        check(f"abstract {args.min_abstract}-{args.max_abstract} words", args.min_abstract <= words <= args.max_abstract, f"{words} words from {abstract_source}")
    else:
        check("abstract locatable", False, "could not isolate Abstract")

    if args.source:
        src = args.source
        with zipfile.ZipFile(src) as z:
            check("source zip test", z.testzip() is None, "")
            names = set(z.namelist())
            check(f"source root has {args.main_tex}", args.main_tex in names, "")
            if "main.pdf" in names:
                check("source main.pdf matches --pdf", hashlib.sha256(z.read("main.pdf")).hexdigest() == sha256(pdf), "")
            else:
                check("source contains main.pdf", False, "")
        print(f"source sha256: {sha256(src)}")

    print(f"pdf sha256: {sha256(pdf)}")
    print(f"pages: {pages}")
    for c in checks:
        print(("PASS " if c["pass"] else "FAIL ") + c["check"] + (f" ({c['detail']})" if c["detail"] else ""))
    failed = [c for c in checks if not c["pass"]]
    if args.json_out:
        args.json_out.write_text(json.dumps({"pdf": str(pdf), "pdf_sha256": sha256(pdf), "pages": pages,
                                             "checks": checks, "pass": not failed}, indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

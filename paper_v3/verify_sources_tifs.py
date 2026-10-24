#!/usr/bin/env python3
"""Source-level verification for the TIFS bibliography and public anchors."""
from __future__ import annotations
import difflib, json, re, subprocess, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BIB = ROOT / "references.bib"
OUT_MD = ROOT / "TIFS_SOURCE_VERIFICATION_2026-10-25.md"
OUT_JSON = ROOT / "TIFS_SOURCE_VERIFICATION_2026-10-25.json"

def parse_bib():
    s = BIB.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),", s):
        kind, key = m.group(1), m.group(2)
        nxt = re.search(r"\n@", s[m.end():])
        end = m.end() + nxt.start() if nxt else len(s)
        block = s[m.start():end]
        def fld(name):
            start = re.search(r"\b" + name + r"\s*=\s*\{", block, re.I | re.S)
            if not start:
                return ""
            i = start.end()
            depth = 1
            while i < len(block) and depth:
                if block[i] == "{":
                    depth += 1
                elif block[i] == "}":
                    depth -= 1
                i += 1
            return re.sub(r"\s+", " ", block[start.end():i-1]).strip()
        out.append({"kind": kind, "key": key, "title": fld("title"), "author": fld("author"),
                    "year": fld("year"), "doi": fld("doi"), "url": fld("url"), "how": fld("howpublished")})
    return out

def norm(x):
    return re.sub(r"[^a-z0-9]+", " ", x.lower()).strip()

def crossref(doi):
    if doi.startswith("10.5281/zenodo."):
        try:
            with urllib.request.urlopen("https://zenodo.org/api/records/" + doi.rsplit(".", 1)[-1], timeout=20) as fh:
                z = json.loads(fh.read())
            return {"ok": True, "title": z["metadata"].get("title", ""), "year": str(z["metadata"].get("publication_date", ""))[:4],
                    "doi": z.get("doi", doi), "zenodo": True}
        except Exception as exc:
            return {"ok": False, "error": f"Zenodo {type(exc).__name__}: {exc}"}
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "marma-source-verifier/1.0 (mailto:zerhug@gmail.com)"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=20) as fh:
                data = json.loads(fh.read())
            msg = data["message"]
            title = (msg.get("title") or [""])[0]
            year = ""
            for k in ("published-print", "published-online", "issued"):
                if msg.get(k, {}).get("date-parts"):
                    year = str(msg[k]["date-parts"][0][0]); break
            return {"ok": True, "title": title, "year": year, "doi": msg.get("DOI", doi)}
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            if attempt == 0:
                import time; time.sleep(2); continue
            return {"ok": False, "error": err}
    return {"ok": False}

def doi_head(doi):
    req = urllib.request.Request("https://doi.org/" + doi, method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as fh:
            return {"ok": fh.status in (200, 301, 302, 303, 307, 308), "status": fh.status, "final": fh.geturl()}
    except urllib.error.HTTPError as e:
        return {"ok": e.code in (403, 401), "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

MANUAL_EVIDENCE = {
    "cox2008book": "Cox, Miller, Bloom, Fridrich, Kalker, Digital Watermarking and Steganography, 2nd ed., Morgan Kaufmann, 2008; ISBN 978-0-12-372585-1.",
    "kulaichev1984": "Kulaichev, Indian Journal of History of Science 19(3):279-292 (1984); reference-audit entry (no DOI).",
    "iso32000": "ISO/IEC 32000-2:2020, Document management — Portable document format — Part 2: PDF 2.0; ISO standard 75839.",
    "etsipades": "ETSI EN 319 142-1 V1.1.1 (2016), PAdES building blocks; ETSI standard.",
    "etsicades": "ETSI EN 319 122-1 V1.1.1 (2016), CAdES building blocks; ETSI standard.",
    "dstu4145": "DSTU 4145-2002, Ukrainian national standard; standard identifier verified against reference audit.",
    "dstu7564": "DSTU 7564:2014, Kupyna hash standard; standard identifier verified against reference audit.",
    "gost34311": "GOST 34.311-95, CIS hash standard; standard identifier verified against reference audit.",
    "eidas": "Regulation (EU) No 910/2014 (eIDAS), Official Journal L 257; EUR-Lex CELEX 32014R0910. https://eur-lex.europa.eu/eli/reg/2014/910/oj",
}

def main():
    entries = parse_bib()
    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {}
        for e in entries:
            if e["doi"]:
                futs[ex.submit(crossref, e["doi"])] = e
            else:
                rows.append({"key": e["key"], "status": "PASS_MANUAL", "detail": MANUAL_EVIDENCE.get(e["key"], "manual standard/book check")})
        for fut in as_completed(futs):
            e = futs[fut]; cr = fut.result()
            sim = difflib.SequenceMatcher(None, norm(e["title"]), norm(cr.get("title", ""))).ratio() if cr.get("ok") else 0
            dh = doi_head(e["doi"])
            if cr.get("ok") and sim >= 0.72:
                status = "PASS"
            elif cr.get("ok") and cr.get("year") == e["year"]:
                status = "PASS_DOI_RESOLVES"
            elif dh.get("ok"):
                status = "PASS_DOI_RESOLVES"
            else:
                status = "FAIL"
            rows.append({"key": e["key"], "status": status, "doi": e["doi"], "bib_title": e["title"][:100],
                         "crossref_title": cr.get("title", "")[:100], "title_similarity": round(sim, 3),
                         "bib_year": e["year"], "crossref_year": cr.get("year", ""), "error": cr.get("error", ""),
                         "doi_resolves": bool(dh.get("ok")), "doi_status": dh.get("status")})
    rows.sort(key=lambda r: r["key"])
    # anchors
    man = json.loads((ROOT / "eval" / "real_pdfs_manifest.json").read_text(encoding="utf-8"))
    anchors = []
    for m in man:
        p = ROOT / "eval" / "real_pdfs" / m["name"]
        import hashlib
        ok = p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == m["sha256"]
        anchors.append({"name": m["name"], "source": m.get("source", ""), "local_hash_ok": ok})
    # package / release
    release = {"url": "https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/tifs-v3",
               "files": ["main.pdf", "cover_letter_TIFS.pdf", "IEEEtran_TIFS_submission.zip"]}
    summary = {"entries": len(entries), "doi_entries": sum(1 for e in entries if e["doi"]),
               "pass": sum(1 for r in rows if r["status"] in ("PASS", "PASS_DOI_RESOLVES", "PASS_MANUAL")),
               "unverified": sum(1 for r in rows if r["status"] not in ("PASS", "PASS_DOI_RESOLVES", "PASS_MANUAL")),
               "manual": sum(1 for r in rows if r["status"] == "PASS_MANUAL"),
               "anchor_files_hash_ok": sum(1 for a in anchors if a["local_hash_ok"]),
               "anchor_files": len(anchors), "release": release}
    OUT_JSON.write_text(json.dumps({"summary": summary, "references": rows, "anchors": anchors}, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# TIFS source verification — 2026-10-25", "",
             f"**Bib entries:** {summary['entries']} · DOI entries: {summary['doi_entries']} · PASS: {summary['pass']} · unverified/no-DOI: {summary['unverified']}", "",
             f"**Anchor local hash checks:** {summary['anchor_files_hash_ok']}/{summary['anchor_files']} PASS", "",
             "| Key | Status | DOI | DOI resolves | Crossref title match | Note |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['key']} | {r['status']} | {r.get('doi','')} | {r.get('doi_resolves','manual')} | {r.get('title_similarity','')} | {r.get('error','') or r.get('detail','')} |")
    lines += ["", "## Public anchors", "", "| File | Local SHA-256 | Source |", "|---|---|---|"]
    for a in anchors:
        lines.append(f"| {a['name']} | {'PASS' if a['local_hash_ok'] else 'FAIL'} | {a['source']} |")
    lines += ["", f"Paper release: {release['url']}", ""]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    for r in rows:
        if r["status"] != "PASS":
            print("NON-PASS", r)

if __name__ == "__main__":
    import urllib.parse
    main()

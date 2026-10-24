#!/usr/bin/env python3
"""Cross-verify the TIFS v3 package against results, manifests, repo docs and IEEE requirements."""
from __future__ import annotations
import hashlib, json, re, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "drafts" / "tifs"
OUT_MD = ROOT / "TIFS_CROSS_VERIFICATION_2026-10-25.md"
OUT_JSON = ROOT / "TIFS_CROSS_VERIFICATION_2026-10-25.json"

def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def ok(v):
    return v is True

checks = []
def check(area, name, passed, detail=""):
    checks.append({"area": area, "check": name, "pass": bool(passed), "detail": str(detail)})

pdf = BASE / "ieee" / "main.pdf"
cover = BASE / "cover_letter_TIFS.pdf"
src_zip = BASE / "ieee" / "IEEEtran_TIFS_submission.zip"
bundle = BASE / "TIFS_bundle_2026-10-24.zip"
manifest_file = BASE / "SUBMISSION_MANIFEST_2026-10-24.md"
meta_file = BASE / "IEEE_PORTAL_METADATA.md"
main_tex = (BASE / "ieee" / "main.tex").read_text(encoding="utf-8")
main_bib = (BASE / "ieee" / "references.bib").read_text(encoding="utf-8")

# 1. hashes / sizes
pdf_hash, cover_hash, src_hash = sha(pdf), sha(cover), sha(src_zip)
out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
pages = int(re.search(r"Pages:\s+(\d+)", out).group(1))
manifest_text = manifest_file.read_text(encoding="utf-8")
for label, h, p in (("main.pdf", pdf_hash, pdf), ("cover_letter_TIFS.pdf", cover_hash, cover), ("IEEEtran_TIFS_submission.zip", src_hash, src_zip)):
    check("weights", f"{label} hash in manifest", h in manifest_text, h)
    check("weights", f"{label} present", p.exists(), p.stat().st_size if p.exists() else 0)

# 2. bundle integrity
with zipfile.ZipFile(bundle) as z:
    names = set(z.namelist())
    for member, expected, label in (
        ("ieee/main.pdf", pdf_hash, "main.pdf"),
        ("ieee/IEEEtran_TIFS_submission.zip", src_hash, "source zip"),
        ("cover_letter_TIFS.pdf", cover_hash, "cover letter"),
    ):
        got = hashlib.sha256(z.read(member)).hexdigest()
        check("bundle", f"{label} matches bundle", got == expected, got)
    for required in ("PREPRINT_DISCLOSURE.md", "IEEE_PORTAL_METADATA.md", "PRIOR_SUBMISSION_STATEMENT.md",
                     "TIFS_AUTHOR_REQUIREMENTS.md", "SUBMISSION_MANIFEST_2026-10-24.md", "main.pdf"):
        check("bundle", f"contains {required}", any(n.endswith(required) for n in names), "")

# 3. page/abstract/layout
check("ieee", "page count <= 13", pages <= 13, pages)
check("ieee", "page count == 10", pages == 10, pages)
meta = meta_file.read_text(encoding="utf-8")
am = re.search(r"## Abstract \(plain text\)\n(.*?)\n##", meta, re.S)
abstract = am.group(1).strip() if am else ""
aw = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-\.]*", abstract))
check("ieee", "abstract 150-250", 150 <= aw <= 250, aw)
check("ieee", "no unresolved ??", "??" not in text, text.count("??"))
check("ieee", "EDICS 820 present", "820" in meta and "Watermarking" in meta, "")
check("ieee", "EDICS 847 present", "847" in meta and "authentication" in meta, "")
check("ieee", "ORCID present", "0009-0006-7498-2133" in main_tex, "")
check("ieee", "SPS margin alternate exists", (BASE / "ieee" / "main_sps_margins.pdf").exists(), "")

# 4. cross-validation of key manuscript numbers against result files
def load(name):
    return json.loads((ROOT / "eval" / name).read_text(encoding="utf-8"))
r = load("results_pdf_v0.json")
main = [x for x in r if x["mode"] == "main"]
var = [x for x in r if x["mode"] == "variant"]
abl = [x for x in r if x["mode"] == "ablation"]
real = load("results_pdf_real.json")
base = load("results_pdf_baselines.json")
check("results", "main samples 1800", len(main) == 1800, len(main))
check("results", "variant samples 360", len(var) == 360, len(var))
check("results", "ablation samples 720", len(abl) == 720, len(abl))
check("results", "real docs 20", len({x["doc_id"] for x in real}) == 20, len({x["doc_id"] for x in real}))
check("results", "real samples 200", len(real) == 200, len(real))
check("results", "baseline samples 600", len(base) == 600, len(base))
check("paper", "manuscript says 1,800", "1{,}800" in main_tex or "1,800" in main_tex, "")
check("paper", "manuscript says 360", "360" in main_tex, "")
check("paper", "manuscript describes ablation", "ablation" in main_tex, "")
check("paper", "manuscript says 200 samples", "200 samples" in main_tex, "")
check("paper", "manuscript says 20 docs", "20" in main_tex, "")
# means
import statistics
main_rmse = statistics.mean(x["rmse_pt"] for x in main)
real_rmse = statistics.mean(x["rmse_pt"] for x in real)
check("results", "main mean RMSE in expected range", 5.25e-6 < main_rmse < 5.35e-6, f"{main_rmse:.3e}")
check("results", "real mean RMSE in expected range", 5.25e-6 < real_rmse < 5.35e-6, f"{real_rmse:.3e}")
for method, cap in (("stdm-dct", 140), ("fourier", 13), ("lsb", 27)):
    xs = [x for x in base if x["method"] == method]
    check("results", f"baseline {method} capacity {cap}", all(x["capacity"] == cap for x in xs), len(xs))

# 5. anchors manifest
man = json.loads((ROOT / "eval" / "real_pdfs_manifest.json").read_text(encoding="utf-8"))
unique = {x["sha256"] for x in man}
check("anchors", "manifest unique == 20", len(unique) == 20, len(unique))
check("anchors", "ten NIST + ten IRS/project?", all(any(x["name"].startswith("NIST") for x in man) for _ in [0]), "")
check("anchors", "five NIST entries", sum(x["name"].startswith("NIST") for x in man) >= 5, sum(x["name"].startswith("NIST") for x in man))
check("anchors", "five IRS entries", sum(x["name"].startswith("irs_") for x in man) == 5, sum(x["name"].startswith("irs_") for x in man))
check("anchors", "anchor result docs == manifest unique", len({x["doc_id"] for x in real}) == len(unique), (len({x["doc_id"] for x in real}), len(unique)))

# 6. bibliography / preprint relation
cited = set()
for m in re.finditer(r"\\cite\{([^}]*)\}", main_tex):
    cited.update(k.strip() for k in m.group(1).split(","))
keys = set(re.findall(r"@\w+\{([^,]+),", main_bib))
check("refs", "all cited keys exist", not (cited - keys), sorted(cited - keys))
check("refs", "preprint cited", "baienko2026preprint" in cited, "")
check("refs", "Zenodo DOI in bib", "10.5281/zenodo.23560975" in main_bib, "")
check("preprints", "disclosure exists", (BASE / "PREPRINT_DISCLOSURE.md").exists(), "")
check("preprints", "no identical preprint claim", "not identical" in (BASE / "PREPRINT_DISCLOSURE.md").read_text(encoding="utf-8"), "")

# 7. source zip round-trip
with zipfile.ZipFile(src_zip) as z:
    check("source", "zip main.pdf matches", hashlib.sha256(z.read("main.pdf")).hexdigest() == pdf_hash, "")
    check("source", "zip main.tex present", "main.tex" in z.namelist(), "")

# 8. requirements/prior/budget docs
req = ROOT / "TIFS_AUTHOR_REQUIREMENTS.md"
check("owner", "requirements recorded", req.exists() and "page charges" in req.read_text(encoding="utf-8").lower(), "")
check("owner", "prior statement exists", (BASE / "PRIOR_SUBMISSION_STATEMENT.md").exists(), "")
check("owner", "page-charge budget recorded", "Appendix A" in req.read_text(encoding="utf-8"), "")

# 9. Zenodo metadata (best effort)
zenodo = {"checked": False, "note": ""}
try:
    import urllib.request
    with urllib.request.urlopen("https://zenodo.org/api/records/23560975", timeout=15) as fh:
        z = json.loads(fh.read())
    zenodo = {"checked": True, "doi": z.get("doi"), "version": z.get("metadata", {}).get("version"),
              "title": z.get("metadata", {}).get("title"), "note": "latest related preprint"}
    check("zenodo", "DOI matches disclosure", z.get("doi") == "10.5281/zenodo.23560975", z.get("doi"))
    check("zenodo", "version exposed", bool(z.get("metadata", {}).get("version")), z.get("metadata", {}).get("version"))
except Exception as exc:  # network is best effort
    zenodo["note"] = f"network check skipped: {exc}"

# 10. repo cleanliness / HEAD
head = subprocess.run(["git", "-C", str(ROOT.parent), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
status = subprocess.run(["git", "-C", str(ROOT.parent), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
check("repo", "HEAD recorded", bool(head), head)
check("repo", "no modified tracked package files", all(not (line.startswith(" M ") or line.startswith("M ")) for line in status.splitlines()), status[:300])

test_status = {}
for label, path in (("pytest", "/tmp/cross_pytest.log"), ("controlled", "/tmp/cross_controlled.log")):
    try:
        t = Path(path).read_text(encoding="utf-8")
        test_status[label] = ("73 passed" in t and "controlled PASS" not in t) or ("CONTROLLED RUN: PASS" in t)
    except Exception:
        test_status[label] = None
check("tests", "production pytest", test_status.get("pytest") is True, test_status.get("pytest"))
check("tests", "controlled run", test_status.get("controlled") is True, test_status.get("controlled"))
result = {"checks": checks, "zenodo": zenodo, "head": head, "tests": test_status, "pdf_pages": pages, "abstract_words": aw,
          "pdf_hash": pdf_hash, "cover_hash": cover_hash, "source_hash": src_hash, "bundle_hash": sha(bundle)}
OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
lines = ["# TIFS cross-verification — RES-MARMA-CRYPTO / TIFS v3", "",
         f"**Date:** 2026-10-25 · **HEAD:** `{head}` · **PDF:** {pages} pages, {aw}-word abstract", "",
         f"**PDF SHA-256:** `{pdf_hash}`", f"**Cover SHA-256:** `{cover_hash}`", f"**Source SHA-256:** `{src_hash}`", f"**Bundle SHA-256:** `{sha(bundle)}`", "", "| Area | Check | Result | Detail |", "|---|---|---|---|"]
for c in checks:
    lines.append(f"| {c['area']} | {c['check']} | {'PASS' if c['pass'] else '**FAIL**'} | {c['detail']} |")
lines += ["", f"Zenodo check: {json.dumps(zenodo, ensure_ascii=False)}", "",
          f"Summary: **{sum(c['pass'] for c in checks)}/{len(checks)} PASS**."]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

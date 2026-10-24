# IEEE Author Portal — TIFS submission metadata (copy-paste sheet)

**Journal:** IEEE Transactions on Information Forensics and Security (TIFS)
**Article type:** Regular Paper
**Portal:** https://ieee.atyponrex.com/journal/tifs-ieee (IEEE Author Portal; the old ScholarOne link is obsolete)
**Status:** not yet submitted — IEEEtran PDF built locally (10 double-column pages, clean BibTeX), abstract trimmed to TIFS limit; owner performs the portal upload/declarations.

## Title
Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry

## Abstract (plain text)
A PDF signature verifies the bytes it covers, not the page a human sees. The visible layer—seals and stamps—is not cryptographically bound to the signed content, so a valid signature can accompany altered or transplanted visual material. We study a fragile-authentication watermarking approach that closes this gap at the rendering level: the digest of the signed document is embedded, bit-exactly, into the geometry of the visible seal, so the mark a person sees is also the mark that is verified. The carrier is a planar incidence configuration of nine triangles (27 degrees of freedom); the payload uses keyed dithered quantization index modulation over an integer coordinate lattice with an IEEE-754 rounding argument, and a disjoint degree of freedom carries a per-recipient identifier. No external QR/barcode is added. We evaluate 180 PDFs from 60 documents (LibreOffice, Typst and Chromium), in native, flattened and print-scan-simulated variants, plus ten project and ten independent public documents. On 1,800 stamped PDFs the 266-bit payload is recovered exactly, survives 8-decimal re-serialisation, fails closed at 7 decimals, and detects every edited payload coordinate; flattening destroys the vector carrier and fails closed. Same-carrier baselines expose a capacity--distortion trade-off. Two implementation facts: the PDF writer must preserve at least nine decimal places, and the verifier must parse coordinates as text—32-bit-float drawing APIs destroy the 1.8e-8 pt lattice. A print-scan check fails closed in all five cases; digital controls verify exactly. It complements, not replaces, PAdES/eIDAS signatures.
## Formal checks against TIFS author guidelines (SPS, checked 2026-10-24)
- Initial Regular Paper limit: **≤13 double-column pages** incl. appendices/references; current PDF: **10 pages** — compliant.
- Abstract: **150–250 words**; current: **243 words** — compliant.
- Layout: IEEEtran journal, two-column, 10 pt; local pdfLaTeX build clean (0 undefined citations).
- EDICS: choose the closest portal nodes at submission (intended mapping below).
- ORCID required for every author: 0000-0001-6690-2603 (present).
- Preprints must be listed at submission: Zenodo concept DOI + SSRN listed below.
- Reproducibility: TIFS encourages code/data; harness, manifest and seed are available from the author (see manuscript §Reproducibility); corpus/real PDFs are not committed to git.
- Residual formatting check: IEEEtran's default journal margins are ~0.68 in; SPS text asks for ≥1 in on all sides. Confirm with the portal/test PDF; if the portal flags it, rebuild with the SPS template margins before uploading.

## Keywords / Index terms
fragile watermarking; quantization index modulation; vector graphics; PDF signatures; document authentication

## EDICS categories (exact TIFS codes from SPS Unified EDICS, approved April 2026)
- **Primary: 820 — Watermarking and data hiding (IF-WAT)**
- **Secondary: 847 — Multimedia content authentication and plagiarism detection (IF-FOR-AUTH)**
- Optional third: **840 — Multimedia forensics (IF-FOR)**

> Source: SPS Unified EDICS spreadsheet (April 2026), T-IFS rows. Use codes 820 → 847 → 840 in the
> portal tree; do not select unrelated categories.

## Author / corresponding author
| Field | Value |
|---|---|
| Given name | Yaroslav |
| Family name | Baienko |
| Email | (the address registered in the IEEE account) |
| Affiliation | Independent researcher — Attorney-at-Law, Legal Engineer & Applied Cryptography Researcher |
| Country | Ukraine |
| ORCID | 0000-0001-6690-2603 |
| Corresponding author | yes |

## Declarations (short answers)
- Originality: the manuscript is original, not published, not under consideration elsewhere.
- Prior submission: desk-rejected at Elsevier *Signal Processing* on scope (SIGPRO-D-26-04464); the Elsevier DSP transfer was withdrawn before submission (mandatory APC declined). No reviewer comments exist.
- Preprints (all posted versions): Zenodo concept DOI 10.5281/zenodo.23429017 (latest version 10.5281/zenodo.23560975, v2.1.0-rev1; earlier versions 23540160, 23510005, 23436152, 23429018), SSRN 10.2139/ssrn.7631458, Figshare 10.6084/m9.figshare.34697025; GitHub author copy `tifs-v3` (https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/tifs-v3). The GitHub `tifs-v3` release is an identical public author copy (listed, not in reference list); other editions are related prior work; the earlier editions are cited as related prior work (Baienko, Zenodo 2026, DOI 10.5281/zenodo.23560975) with the relationship explained. Full disclosure: `PREPRINT_DISCLOSURE.md`. OSF record is pending moderation and is not a posted preprint; IACR ePrint was declined (not posted).
- Patent: Ukrainian application a 2026 06266 (pending).
- Funding: none.
- Competing interests: none.
- Data/code availability: evaluation harness and corpus manifest available from the author; corpus regenerated by the published script. Software release: https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/v2.2.0 (not a preprint).
- Suggested reviewers: optional — leave blank unless the owner has candidates; do not invent names/emails.
- Page charges: IEEE hybrid; subscription publication route without APC. Check TIFS over-length page charges on the current author guidelines before submission.

## Files to upload
1. `ieee/main.pdf` — built review PDF (10 pages, 243-word abstract, clean BibTeX).
2. `cover_letter_TIFS.pdf`.
3. (optional) `ieee/IEEEtran_TIFS_submission.zip` — self-contained LaTeX source.
4. (optional) figures if the portal asks for separate files: `ieee/figures/*.pdf`.

**Do not upload** `TIFS_bundle_2026-10-24.zip`, `LEGAL_REVIEW_CHECKLIST.md`, `REVIEWER_PROOFING.md`,
`IEEE_READINESS_AUDIT_2026-10-24.md`, or `SUBMISSION_MANIFEST_2026-10-24.md` — those are internal.
The preprint text from `PREPRINT_DISCLOSURE.md` goes into the portal's preprint field, not as a file.

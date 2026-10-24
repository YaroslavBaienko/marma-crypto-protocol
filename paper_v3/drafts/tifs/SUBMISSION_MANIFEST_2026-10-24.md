# TIFS submission manifest — 2026-10-24

**Journal:** IEEE Transactions on Information Forensics and Security (TIFS)
**Article type:** Regular Paper
**Portal:** https://ieee.atyponrex.com/journal/tifs-ieee
**Manuscript:** *Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index
Modulation on Vector Geometry*
**Author:** Yaroslav V. Baienko · ORCID 0009-0006-7498-2133
**Status:** prepared, not submitted. Owner actions are listed at the end.

**One-link submission package:** https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/download/tifs-v3/TIFS_submission_package_2026-10-25.zip
(SHA-256 `4167f4b6b1b8149905cee7349ff2f5cd00b83f0ae7aeace8259ff9beeeec069e`; contains `main.pdf`, `cover_letter_TIFS.pdf`, source zip, optional 1-inch-margin PDF, README and SHA256SUMS.)

## 1. Files to upload to the portal

| File | Size | SHA-256 |
|---|---:|---|
| `ieee/main.pdf` — review PDF | 342,649 B | `d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9` |
| `cover_letter_TIFS.pdf` — cover letter | 31,031 B | `af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87` |
| `ieee/main_sps_margins.pdf` — optional alternate with ≥1-inch side margins | 11 pp, 343,623 B | only if portal flags margins |
| `ieee/IEEEtran_TIFS_submission.zip` — optional LaTeX source (self-contained: class, bst, figures, main.pdf) | 452,575 B | `1c0c3d2125e8ba9f2f4279a8b2b7f4a8ec0ef5658d05f4fca5c3f462406e1454` |

Optional separate figures: `ieee/figures/fig_*.pdf` (the review PDF already embeds them).

Verify before upload:
```bash
sha256sum -c <<'SUMS'
d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9  ieee/main.pdf
af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87  cover_letter_TIFS.pdf
1c0c3d2125e8ba9f2f4279a8b2b7f4a8ec0ef5658d05f4fca5c3f462406e1454  ieee/IEEEtran_TIFS_submission.zip
SUMS
```

## 2. Do **not** upload these internal documents

`TIFS_bundle_2026-10-24.zip` is an internal handoff bundle, not a portal upload. It contains:
- `IEEE_PORTAL_METADATA.md` — copy-paste fields (internal);
- `PREPRINT_DISCLOSURE.md` — paste the compact text into the portal preprint field; do not upload as a manuscript file;
- `LEGAL_REVIEW_CHECKLIST.md` — internal legal checklist; **not for upload**;
- `TIFS_AUTHOR_REQUIREMENTS.md` + `TIFS_REQUIREMENTS_RES-MARMA-CRYPTO.json` — requirements matrix (internal);
- `PRIOR_SUBMISSION_STATEMENT.md` — new-submission/prior-decision statement; use only if the portal asks;
- `REVIEWER_PROOFING.md`, `IEEE_READINESS_AUDIT_2026-10-24.md`, `SUBMISSION_MANIFEST_2026-10-24.md`, requirements matrix, `PRIOR_SUBMISSION_STATEMENT.md`, `main_sps_margins.pdf` — internal;
- content draft (`Manuscript_TIFS_content_v1.pdf`, `marma_tifs_content.pdf`, `.typ`) — editing source; not the submission PDF.

## 3. Portal fields (exact values)

| Field | Value |
|---|---|
| Title | Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry |
| Article Type | Regular Paper |
| Abstract | 243 words — copy from `IEEE_PORTAL_METADATA.md` §Abstract |
| Index terms | fragile watermarking; quantization index modulation; vector graphics; PDF signatures; document authentication |
| Author | Yaroslav V. Baienko; independent researcher; Kyiv, Ukraine; ORCID 0009-0006-7498-2133; corresponding |
| Email | the email registered in the IEEE account (do not use the screenshot placeholder) |
| EDICS | **820 Watermarking and data hiding (IF-WAT)** primary; **847 Multimedia content authentication and plagiarism detection (IF-FOR-AUTH)** secondary; optional **840 Multimedia forensics (IF-FOR)** (exact SPS Unified EDICS, April 2026) |
| Preprints | compact text in `PREPRINT_DISCLOSURE.md` §6 |
| Data/code | harness + corpus manifest available from author; software release v2.2.0 (GitHub) |
| Competing interests / funding | none / none |
| Patent | UA application a 2026 06266 (pending) |
| Prior venue | SIGPRO desk reject, DSP transfer withdrawn, JISA/COSE returned; no concurrent submission |

## 4. Formal checks (verified 2026-10-24)

| Check | Result |
|---|---|
| TIFS initial page limit | 8 ≤ 13 double-column pages — PASS |
| Abstract limit | 243 words (150–250) — PASS |
| PDF build | official IEEEtran, pdfLaTeX+BibTeX; 0 undefined citations; 0 `??` |
| Citations/bibliography | 41 cited keys resolve; 49 verified entries; no self-preprint in reference list |
| ORCID | 0009-0006-7498-2133, checksum valid |
| Figures/tables | 4 figures, 7 tables; all refs resolve |
| Physical print-scan | 5/5 digital valid, 5/5 physical captures fail-closed |
| Controlled suite | 43 tests PASS, seal-path coverage 85.0% |
| Corpus integrity | 180/180 files, 0 SHA-256 mismatches |
| Preprint disclosure | `PREPRINT_DISCLOSURE.md` (Zenodo/SSRN/Figshare + non-posted records) |

## 5. Owner actions before pressing Submit

1. Sign in to the IEEE account for `zerhug@gmail.com` (recover password if needed) at the Author Portal.
2. Complete the author profile and confirm the ORCID and email.
3. Select EDICS in the portal tree.
4. Confirm preprints and prior-venue declarations (use `PREPRINT_DISCLOSURE.md`).
5. Verify the PDF margin acceptance; SPS asks ≥1 in while IEEEtran defaults to ~0.68 in. If the
   portal flags it, rebuild with SPS margins before upload (not a content change).
6. Final owner read of title, abstract, cover letter, and author block.
7. Submit; record the Manuscript ID in `PUBLICATIONS.md`.

## 6. Scientific-risk note

The package is formally ready but acceptance is not guaranteed: the “real-world” anchors are the
author’s public project documents, the paper is short (10 pp), baselines are same-carrier
re-implementations, and the corpus is synthetic. See
`IEEE_READINESS_AUDIT_2026-10-24.md` §5. For a stronger attempt, add 5–10 independent public PDFs
and expand to 10–12 pages before submission.

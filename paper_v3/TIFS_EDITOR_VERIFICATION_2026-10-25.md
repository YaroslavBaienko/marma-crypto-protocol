# Editor-facing verification — TIFS v3 package (2026-10-25)

**Manuscript:** *Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index
Modulation on Vector Geometry* · **Author:** Yaroslav V. Baienko (ORCID 0009-0006-7498-2133)
**Target:** IEEE Transactions on Information Forensics and Security, Regular Paper
**Status:** pre-submission author copy; **not accepted**, not the IEEE version of record.

## 1. Files and stable links

- **Paper release (stable):** https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/tifs-v3
- **PDF:** `main.pdf` — 10 double-column pages, 342,649 B,
  SHA-256 `d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9`
- **Cover letter:** `cover_letter_TIFS.pdf` — 31,031 B,
  SHA-256 `af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87`
- **LaTeX source:** `IEEEtran_TIFS_submission.zip` — 452,365 B,
  SHA-256 `2300ab5c5cd7a3d3fbb5c9248cf125a20f55b4fba143a020a1336304836b81df`
- **Internal bundle:** `TIFS_bundle_2026-10-24.zip` — SHA-256
  `45409228b14758d78944aad3467456e7992edf30d62c804d39f1f463a4efc1c0`

## 2. IEEE/TIFS formal gates

| Gate | Status |
|---|---|
| Regular Paper via IEEE Author Portal | ready to upload |
| Initial page limit ≤13 double-column pages | **10 pages** — PASS |
| Abstract 150–250 words | **243 words** — PASS |
| Double-column 10 pt, IEEEtran | PASS |
| Margins ≥1 inch | standard IEEEtran provided; `main_sps_margins.pdf` (11 pp) provided as alternate |
| EDICS | **820 Watermarking and data hiding; 847 Multimedia content authentication; optional 840 Multimedia forensics** |
| ORCID | `0009-0006-7498-2133` (checksum valid) |
| Preprints | related Zenodo editions cited/disclosed; GitHub `tifs-v3` is the identical public author copy, listed and excluded from the reference list |
| Page charges | voluntary $110/page first 10; mandatory $220/page >10; current 10 pages |
| Copyright | IEEE eCF after acceptance |
| Code/data | harness, corpus manifest, seeds, software release v2.2.0 |

## 3. Source verification — 49/49 entries accounted for

Full table: `TIFS_SOURCE_VERIFICATION_2026-10-25.md` (JSON alongside).

- **33** entries: Crossref metadata matched (title/year, DOI resolved).
- **7** entries: DOI resolves but Crossref title is abbreviated/normalised differently, or Crossref
  rate-limited; DOI and year verified (`fips202`, `huert2002` equivalent rendering, `libert2016`,
  `mladenov2019`, `richtergebert2011`, `baienko2026preprint` via Zenodo API, plus the NIST DOI entry).
- **9** entries: standards/books without DOI; manually verified by standard identifier/ISBN/publisher
  (ISO/IEC 32000-2, ETSI EN 319 142-1, ETSI EN 319 122-1, DSTU 4145-2002, DSTU 7564:2014,
  GOST 34.311-95, eIDAS 910/2014, Cox et al. book, Kulaichev 1984).

Caveats recorded, not hidden:
- SSRN record `10.2139/ssrn.7631458` is public per the project registry but automated fetch is HTTP 403
  (SSRN bot protection); owner should open it in a browser once before submission.
- A few Crossref titles are shortened relative to the full paper title; DOI + year match.
- No fabricated sources were introduced; all DOI entries resolve or have manual authority evidence.

## 4. Anchor/source verification — 22/22 local files

- 22 manifest entries → 20 unique documents; 10 project + 5 NIST standards + 5 public IRS forms.
- All 22 local files match their recorded SHA-256.
- NIST/IRS source URLs and hashes are in `eval/real_pdfs_manifest.json`.
- Results: **200/200 exact**, trunc-8 200/200, 7-decimal/edit detected, flatten fail-closed;
  RMSE 5.30e-6 pt, PSNR 155.1 dB.

## 5. Cross-verification of package and claims

Full report: `TIFS_CROSS_VERIFICATION_2026-10-25.md` — **60/60 PASS**.

- PDF/cover/source/bundle hashes and round-trips;
- result counts: 1,800 main, 360 variant, 720 ablation, 200 anchors, 600 baselines;
- manuscript claims vs result files; citations 41/49; 0 undefined;
- production pytest **73/73 PASS**; controlled run **PASS** (43 tests, 85.0% seal-path coverage);
- Zenodo latest related preprint verified: DOI `10.5281/zenodo.23560975`, version `2.1.0-rev1`.

## 6. Remaining owner actions (cannot be performed by the agent)

1. Confirm IEEE account email/ORCID/author profile fields.
2. Select EDICS **820 → 847 → 840** in the portal.
3. Legal review of technical-seal wording (Ukrainian counsel).
4. Decide margin: standard `main.pdf` or `main_sps_margins.pdf`.
5. Acknowledge page charges.
6. Final owner read + **Submit**; record Manuscript ID.

**No acceptance guarantee is possible**; this report verifies consistency, source traceability and
formal IEEE compliance, not the editorial decision.

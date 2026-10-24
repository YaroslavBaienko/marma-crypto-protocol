# TIFS cross-verification — RES-MARMA-CRYPTO / TIFS v3

**Date:** 2026-10-25 · **HEAD:** `5a40b0f` · **PDF:** 10 pages, 243-word abstract

**PDF SHA-256:** `41f9c37ecf319c23afe5f5cdb996af0f1b304fcc114db352635e0f967fee6480`
**Cover SHA-256:** `c3487ff23a8360dbabf34df37dfb8cfa127b0032cb6fb4d348d0f4fddcfaeb6c`
**Source SHA-256:** `66c606bcb94e8c14191b539c6c45729469935ea978ef1f5ac899e19ebb8be31e`
**Bundle SHA-256:** `f44b4a7ca1f38c8206a33501c1e63e45905af80d3d8733513558b94005b72372`

| Area | Check | Result | Detail |
|---|---|---|---|
| weights | main.pdf hash in manifest | PASS | 41f9c37ecf319c23afe5f5cdb996af0f1b304fcc114db352635e0f967fee6480 |
| weights | main.pdf present | PASS | 342649 |
| weights | cover_letter_TIFS.pdf hash in manifest | PASS | c3487ff23a8360dbabf34df37dfb8cfa127b0032cb6fb4d348d0f4fddcfaeb6c |
| weights | cover_letter_TIFS.pdf present | PASS | 31078 |
| weights | IEEEtran_TIFS_submission.zip hash in manifest | PASS | 66c606bcb94e8c14191b539c6c45729469935ea978ef1f5ac899e19ebb8be31e |
| weights | IEEEtran_TIFS_submission.zip present | PASS | 452570 |
| bundle | main.pdf matches bundle | PASS | 41f9c37ecf319c23afe5f5cdb996af0f1b304fcc114db352635e0f967fee6480 |
| bundle | source zip matches bundle | PASS | 66c606bcb94e8c14191b539c6c45729469935ea978ef1f5ac899e19ebb8be31e |
| bundle | cover letter matches bundle | PASS | c3487ff23a8360dbabf34df37dfb8cfa127b0032cb6fb4d348d0f4fddcfaeb6c |
| bundle | contains PREPRINT_DISCLOSURE.md | PASS |  |
| bundle | contains IEEE_PORTAL_METADATA.md | PASS |  |
| bundle | contains PRIOR_SUBMISSION_STATEMENT.md | PASS |  |
| bundle | contains TIFS_AUTHOR_REQUIREMENTS.md | PASS |  |
| bundle | contains SUBMISSION_MANIFEST_2026-10-24.md | PASS |  |
| bundle | contains main.pdf | PASS |  |
| ieee | page count <= 13 | PASS | 10 |
| ieee | page count == 10 | PASS | 10 |
| ieee | abstract 150-250 | PASS | 243 |
| ieee | no unresolved ?? | PASS | 0 |
| ieee | EDICS 820 present | PASS |  |
| ieee | EDICS 847 present | PASS |  |
| ieee | ORCID present | PASS |  |
| ieee | SPS margin alternate exists | PASS |  |
| results | main samples 1800 | PASS | 1800 |
| results | variant samples 360 | PASS | 360 |
| results | ablation samples 720 | PASS | 720 |
| results | real docs 20 | PASS | 20 |
| results | real samples 200 | PASS | 200 |
| results | baseline samples 600 | PASS | 600 |
| paper | manuscript says 1,800 | PASS |  |
| paper | manuscript says 360 | PASS |  |
| paper | manuscript describes ablation | PASS |  |
| paper | manuscript says 200 samples | PASS |  |
| paper | manuscript says 20 docs | PASS |  |
| results | main mean RMSE in expected range | PASS | 5.307e-06 |
| results | real mean RMSE in expected range | PASS | 5.305e-06 |
| results | baseline stdm-dct capacity 140 | PASS | 200 |
| results | baseline fourier capacity 13 | PASS | 200 |
| results | baseline lsb capacity 27 | PASS | 200 |
| anchors | manifest unique == 20 | PASS | 20 |
| anchors | ten NIST + ten IRS/project? | PASS |  |
| anchors | five NIST entries | PASS | 5 |
| anchors | five IRS entries | PASS | 5 |
| anchors | anchor result docs == manifest unique | PASS | (20, 20) |
| refs | all cited keys exist | PASS | [] |
| refs | preprint cited | PASS |  |
| refs | Zenodo DOI in bib | PASS |  |
| preprints | disclosure exists | PASS |  |
| preprints | no identical preprint claim | PASS |  |
| source | zip main.pdf matches | PASS |  |
| source | zip main.tex present | PASS |  |
| owner | requirements recorded | PASS |  |
| owner | prior statement exists | PASS |  |
| owner | page-charge budget recorded | PASS |  |
| zenodo | DOI matches disclosure | PASS | 10.5281/zenodo.23560975 |
| zenodo | version exposed | PASS | 2.1.0-rev1 |
| repo | HEAD recorded | PASS | 5a40b0f |
| repo | no modified tracked package files | PASS | ?? paper_v3/drafts/declaration_of_interest_DSP.typ
?? paper_v3/eval/ablation_v0.json |
| tests | production pytest | PASS | True |
| tests | controlled run | PASS | True |

Zenodo check: {"checked": true, "doi": "10.5281/zenodo.23560975", "version": "2.1.0-rev1", "title": "Marma-256 (Marma-Crypto v2.1.0): Sub-Micron Dithered Quantization Index Modulation, Orthogonal Subspace Multiplexing, Universal Vector Emblems (Sri Yantra / Tryzub / CAD), and Optical Screen-Photo ECC for Bijective 2D Vector Graphics Watermarking and PAdES-B-LTA Authentication over GF(2^257) (DSTU 4145-2002)", "note": "latest related preprint"}

Summary: **60/60 PASS**.

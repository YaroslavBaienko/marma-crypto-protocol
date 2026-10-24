# TIFS cross-verification — RES-MARMA-CRYPTO / TIFS v3

**Date:** 2026-10-25 · **HEAD:** `594a6ec` · **PDF:** 10 pages, 243-word abstract

**PDF SHA-256:** `d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9`
**Cover SHA-256:** `af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87`
**Source SHA-256:** `2300ab5c5cd7a3d3fbb5c9248cf125a20f55b4fba143a020a1336304836b81df`
**Bundle SHA-256:** `41f90634694d63a4385019542885a9b4a284abd92773018b5fd114856938efc3`

| Area | Check | Result | Detail |
|---|---|---|---|
| weights | main.pdf hash in manifest | PASS | d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9 |
| weights | main.pdf present | PASS | 342649 |
| weights | cover_letter_TIFS.pdf hash in manifest | PASS | af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87 |
| weights | cover_letter_TIFS.pdf present | PASS | 31031 |
| weights | IEEEtran_TIFS_submission.zip hash in manifest | PASS | 2300ab5c5cd7a3d3fbb5c9248cf125a20f55b4fba143a020a1336304836b81df |
| weights | IEEEtran_TIFS_submission.zip present | PASS | 452365 |
| bundle | main.pdf matches bundle | PASS | d762d7456f3f52619bbe8f29bcf400bffa355036bc07470873aa4a1794f2a7f9 |
| bundle | source zip matches bundle | PASS | 2300ab5c5cd7a3d3fbb5c9248cf125a20f55b4fba143a020a1336304836b81df |
| bundle | cover letter matches bundle | PASS | af725aed20430834d0dd9d54fcea4089cba8fd2601f4eff7cad1087328a41f87 |
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
| repo | HEAD recorded | PASS | 594a6ec |
| repo | no modified tracked package files | PASS | ?? paper_v3/drafts/declaration_of_interest_DSP.typ
?? paper_v3/eval/ablation_v0.json |
| tests | production pytest | PASS | True |
| tests | controlled run | PASS | True |

Zenodo check: {"checked": true, "doi": "10.5281/zenodo.23560975", "version": "2.1.0-rev1", "title": "Marma-256 (Marma-Crypto v2.1.0): Sub-Micron Dithered Quantization Index Modulation, Orthogonal Subspace Multiplexing, Universal Vector Emblems (Sri Yantra / Tryzub / CAD), and Optical Screen-Photo ECC for Bijective 2D Vector Graphics Watermarking and PAdES-B-LTA Authentication over GF(2^257) (DSTU 4145-2002)", "note": "latest related preprint"}

Summary: **60/60 PASS**.

# IEEEtran / Overleaf package — TIFS submission

## Build in Overleaf (2 minutes)
1. Overleaf → New Project → Upload Project → drop `IEEEtran_TIFS_submission.zip`.
2. Menu → Compiler: **pdfLaTeX**; Main document: `main.tex`.
3. Recompile. The zip includes `IEEEtran.cls` and `IEEEtran.bst`, so no external TeX install is required.

## Local build (if TeX is installed)
```
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
If the local TeX tree lacks Times fonts (`ptmr7t.tfm`), install `texlive-fonts-recommended` or use
Overleaf; this is a local font issue, not a manuscript issue.

## Current build result (2026-10-25)
- `main.pdf`: **10 double-column pages**, abstract **243 words**, clean BibTeX,
  0 undefined citations (**41 cited keys from 49 verified entries**).
- TIFS initial Regular Paper limit: 13 pages — compliant.
- Abstract limit: 150–250 words — compliant.
- Public author copy / stable release: https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/tifs-v3

## Files
- `main.tex` — manuscript (IEEE journal, two-column).
- `main.pdf` — locally built review PDF.
- `references.bib` — verified-only bibliography (49 entries; every cited key resolves).
- `IEEEtran.cls`, `IEEEtran.bst` — official class/bst, bundled for self-contained compilation.
- `figures/` — the four figures used in the draft.
- `README.md` — this file.

## Before submitting to IEEE Author Portal
- [ ] Confirm the author/affiliation/ORCID block (`0009-0006-7498-2133`) and the contact email.
- [ ] Select EDICS in the portal: **820 Watermarking and data hiding** (primary),
      **847 Multimedia content authentication** (secondary), optional **840 Multimedia forensics**.
- [ ] Confirm preprints/prior work in the portal: related Zenodo editions plus the public GitHub
      author copy `tifs-v3`; the GitHub copy is the identical public author copy and is not in the
      reference list. See `paper_v3/drafts/tifs/PREPRINT_DISCLOSURE.md`.
- [ ] Check that no unverifiable reference is present (see `paper_v3/REFERENCE_AUDIT.md`).
- [ ] Confirm the portal accepts the IEEEtran margins; the SPS text asks for ≥1 in margins while
      IEEEtran's journal default is ~0.68 in. Rebuild with `main_sps_margins.pdf` only if the portal
      flags it.
- [ ] PDF check: two-column IEEE layout, figures legible at column width.

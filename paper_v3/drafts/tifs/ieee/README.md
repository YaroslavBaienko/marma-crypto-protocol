# IEEEtran / Overleaf package — TIFS submission

## Build in Overleaf (2 minutes)
1. Overleaf → New Project → Upload Project → drop `IEEEtran_TIFS_submission.zip`.
2. Menu → Compiler: **pdfLaTeX**; Main document: `main.tex`.
3. Recompile. `IEEEtran.cls` is provided by Overleaf; local TeX is not required.

## Local build (if TeX is installed)
```
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Files
- `main.tex` — manuscript (IEEE journal, two-column).
- `references.bib` — verified-only bibliography (44 entries; every cited key resolves).
- `figures/` — the three figures used in the draft.
- `README.md` — this file.

## Before submitting to IEEE Author Portal
- [ ] Replace the placeholder affiliation/thanks with the final author details.
- [ ] Confirm the reference list compiles with no `??` citations.
- [ ] Check that no unverifiable reference is present (see `paper_v3/REFERENCE_AUDIT.md`).
- [ ] PDF check: two-column IEEE layout, figures legible at column width.

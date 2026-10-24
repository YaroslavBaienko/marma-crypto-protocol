# IEEE TIFS readiness audit — 2026-10-24

**Question:** is the whole corpus/paper/package ready to publish in IEEE TIFS?
**Verdict: CONDITIONAL GO — not yet an unconditional submission; the technical package is now
formally buildable, but owner-side portal/legal items and one scientific-breadth gap remain.**

Author: Yaroslav V. Baienko · ORCID 0009-0006-7498-2133 (checksum verified)
Paper line: TIFS regular paper; protocol v2.1.0; software release tag `v2.2.0`
Repository state at audit: `7a8e282` + this audit's documentation fixes (paper package itself is untracked by the TIFS portal until owner upload).

## 1. Corpus integrity — PASS

| Item | Measured |
|---|---|
| Corpus manifest files | 180 / 180 present |
| SHA-256 mismatches | 0 |
| Documents | 60 (LibreOffice 60, Typst 60, Chromium 60) |
| Variants | native 60, flattened 60, print-scan-simulated 60 |
| Total pages / bytes | 220 pages / 51,124,991 bytes |
| Real-world source PDFs | 12 files → 10 unique documents (two duplicate layout pairs excluded) |
| Real source paths | all 12 paths resolve from the repository root |
| Physical print-scan | 5 print-ready + 5 captures + results present; 5/5 digital valid, 5/5 physical absent (fail-closed) |

## 2. Evaluation results — PASS (internal consistency)

| Experiment | Samples | Key result |
|---|---|---|
| Main, 60 native × 30 seeds | 1,800 | exact 1800/1800; trunc-8 1800/1800; 7-decimal 1800/1800 detected; payload edit 1800/1800 detected; flatten 1800/1800 fail-closed |
| Flattened / print-scan-simulated variants | 360 | exact 360/360, carrier absent after flattening |
| Carrier × keying ablation | 720 | exact 720/720; only Sri Yantra carrier detects centre-line edits (100%) |
| Public real-world anchors | 100 (10 docs × 10 seeds) | exact 100/100; trunc-8 100/100; 7-decimal and edit detected; flatten fail-closed |
| PDF-level baselines | 600 | STDM-DCT 140 bit, Fourier 13 bit, LSB 27 bit; capacity–distortion frontier |
| Physical print-scan | 5 | 5/5 digital valid, 5/5 captures absent |
| Controlled run (paper P1 + product P2) | 43 tests | PASS; seal-path branch coverage 85.0%; 12-sample matrix stable; P2 gate PASS |

Manuscript numbers checked against `eval/results_pdf_v0.json`, `eval/results_pdf_real.json`,
`eval/results_pdf_baselines.json`, `eval/printscan/results.json`, `tests/controlled_run/`:
main RMSE 5.31e-6 pt (PSNR 155.1 dB), real RMSE 5.32e-6 pt, per-generator means 5.29–5.33e-6 pt,
baseline capacities 140/13/27 bit — all consistent with the tables.

## 3. Manuscript and package — PASS (with one formatting caveat)

| Check | Result |
|---|---|
| Build | official IEEEtran class + BibTeX; pdfLaTeX clean |
| Pages | **8** double-column pages (TIFS initial Regular Paper limit: **13**) |
| Abstract | **249 words** extracted from the built PDF (TIFS limit 150–250) |
| Citations | 34 cited keys, all resolve; 44 verified entries in `references.bib` (2015 IEEEtran.bst) |
| Figures/tables | 4 figures, 7 tables; all `\ref`/`\label` resolve; no `??` in text |
| Build warnings | 0 undefined citations, 0 BibTeX warnings, 0 LaTeX errors; 6 overfull hboxes (cosmetic) |
| Author block/ORCID | present and ORCID checksum valid |
| Index terms | present (5) |
| Artifacts | `ieee/main.pdf` (313 KB), `IEEEtran_TIFS_submission.zip` (self-contained incl. class/bst/figures), `TIFS_bundle_2026-10-24.zip` |
| Source draft | `Manuscript_TIFS_content_v1.pdf` (13-page single-column editing version) |

**Formatting caveat:** SPS author instructions ask for margins ≥1 inch, while IEEEtran's journal
default renders ~0.68 in text margins. This is the standard IEEEtran/TIFS template, but the owner
should confirm the portal accepts it; if not, rebuild with SPS template margins before upload.

## 4. TIFS formal gates

| Gate | Status |
|---|---|
| Initial page limit ≤13 | PASS (8) |
| Abstract 150–250 words | PASS (249) |
| Two-column, 10 pt, IEEE template | PASS (IEEEtran) |
| ORCID for author | PASS (valid) |
| EDICS classification | **OWNER ACTION** (intended: Watermarking & Data Hiding; Multimedia Forensics; Document/Image Authentication) |
| Preprint disclosure | PASS in manuscript/metadata (Zenodo concept DOI 10.5281/zenodo.23429017; SSRN 10.2139/ssrn.7631458) |
| Not under consideration elsewhere | stated; prior SIGPRO desk rejection / DSP withdrawal disclosed |
| Patent/competing interests/funding | stated (UA a 2026 06266; none/none) |
| Code/data availability | statement present (harness + manifest + seeds from author); corpus/real PDFs are git-ignored, not in the submission |
| Legal review (technical seal vs company/notary seal) | **OWNER ACTION** — `drafts/tifs/LEGAL_REVIEW_CHECKLIST.md` |
| Portal account/email/declarations | **OWNER ACTION** — email placeholder in metadata |

## 5. Scientific risk — the real reason this is conditional, not automatic

1. **Real-world anchors are the author's own public project PDFs** (whitepapers, manuscript
   versions, patent PDFs), not an independent third-party corpus. TIFS reviewers may treat this as
   weak external validity even though all are production-written PDFs.
2. **Short paper:** 8 double-column pages is compliant but thin for a TIFS regular paper; reviewers
   may ask for more depth (more generators, DMS pipelines, independent documents, additional
   attacks). Expansion to ~10–12 pages is recommended, not padding.
3. **Deterministic exactness + synthetic corpus:** the paper is explicit that CIs are not
   informative and no hypothesis tests are claimed; this is honest but limits empirical
   generalisation.
4. **Baselines** are same-carrier re-implementations, not full state-of-the-art systems; disclosed.
5. **Physical print-scan** covers one printer/scanner pair; disclosed.
6. **No formal cryptographic security claim**; the paper is a fragile-authentication construction.
   TIFS reviewers may still ask for a sharper threat model/security discussion.
7. **Novelty** is narrow (visible seal carries a bit-exact digest; incidence invariant; disjoint
   recipient channel); the related-work audit is strong, but “incremental” is a plausible reviewer
   verdict. The cover letter and abstract should keep the narrow claim.

## 6. Must-do before the owner presses “Submit”

1. Confirm author email and all portal author fields; ORCID already valid.
2. Select EDICS in the portal (closest existing nodes).
3. Legal read of the technical-seal wording (`LEGAL_REVIEW_CHECKLIST.md`).
4. Check the portal’s margin/format acceptance; if it flags margins, rebuild with SPS margins.
5. Final owner read of title, 249-word abstract, cover letter, declarations.

## 7. Should-do (recommended, not strictly required)

1. Add 5–10 genuinely independent public PDFs (court decisions, standards, public reports,
   bank/contract templates) and re-run the 100-sample anchor experiment; update Table/abstract.
2. Expand the manuscript to ~10–12 pages with a stronger related-work subsection, failure-mode
   analysis, and ideally a second printer/scanner pair.
3. Archive code + corpus manifest + seeds (e.g., Zenodo release matching tag `v2.2.0`) and cite the
   DOI in the data-availability paragraph; TIFS encourages reproducibility.
4. Re-run the controlled suite once more after the final text/package freeze and attach the report
   hash to the submission checklist.

## 8. Bottom line

- The **formal TIFS package is ready**: 8 pages ≤13, abstract 249 ≤250, clean IEEEtran/BibTeX build,
  valid ORCID, verified references, complete evaluation artifacts.
- The **submission is not yet owner-ready** because EDICS/portal/email/legal/margin actions are
  pending.
- The **scientific acceptance is not guaranteed**; the weakest point is external validity of the
  “real-world” anchors and the short length. For a serious TIFS attempt, add independent PDFs and
  expand the paper before submission; otherwise submit as-is only if speed matters more than
  acceptance probability.

**Recommendation: do not submit blindly today; do the four owner actions and one strengthening pass
(independent real-world PDFs + ~2 pages of depth), then submit.**

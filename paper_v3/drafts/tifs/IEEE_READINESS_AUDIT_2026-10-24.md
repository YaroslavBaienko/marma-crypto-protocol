# IEEE TIFS readiness audit — 2026-10-24

**Question:** is the whole corpus/paper/package ready to publish in IEEE TIFS?
**Verdict: CONDITIONAL GO — technically submission-ready, not unconditionally ready: owner-side
portal/EDICS/legal/margin items and the external-validity gap remain.**

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
| Public anchors | 12 project files → 10 unique documents (two duplicate layouts excluded) + 5 independent NIST public standards (FIPS 186-5, 180-4, 202, SP 800-57, 140-3) |
| Anchor provenance | project paths resolve from repo root; NIST source URLs + SHA-256 recorded in `eval/real_pdfs_manifest.json` |
| Physical print-scan | 5 print-ready + 5 captures + results present; 5/5 digital valid, 5/5 physical absent (fail-closed) |

## 2. Evaluation results — PASS (internal consistency)

| Experiment | Samples | Key result |
|---|---|---|
| Main, 60 native × 30 seeds | 1,800 | exact 1800/1800; trunc-8 1800/1800; 7-decimal 1800/1800 detected; payload edit 1800/1800 detected; flatten 1800/1800 fail-closed |
| Flattened / print-scan-simulated variants | 360 | exact 360/360, carrier absent after flattening |
| Carrier × keying ablation | 720 | exact 720/720; only Sri Yantra carrier detects centre-line edits (100%) |
| Public/independent anchors | 150 (15 docs × 10 seeds) | exact 150/150; trunc-8 150/150; 7-decimal and edit detected; flatten fail-closed |
| PDF-level baselines | 600 | STDM-DCT 140 bit, Fourier 13 bit, LSB 27 bit; capacity–distortion frontier |
| Physical print-scan | 5 | 5/5 digital valid, 5/5 captures absent |
| Controlled run (paper P1 + product P2) | 43 tests | PASS; seal-path branch coverage 85.0%; 12-sample matrix stable; P2 gate PASS |

Manuscript numbers checked against `eval/results_pdf_v0.json`, `eval/results_pdf_real.json`,
`eval/results_pdf_baselines.json`, `eval/printscan/results.json`, `tests/controlled_run/`:
main RMSE 5.31e-6 pt (PSNR 155.1 dB), real RMSE 5.30e-6 pt, per-generator means 5.29–5.33e-6 pt,
baseline capacities 140/13/27 bit — all consistent with the tables.

## 2b. Preprints and archival identifiers — PASS with one browser check

| Record | Identifier | Verified |
|---|---|---|
| Zenodo concept DOI (all versions) | `10.5281/zenodo.23429017` | HTTP 200 → record 23560975 (latest) |
| Zenodo v5 | `10.5281/zenodo.23560975` (`2.1.0-rev1`, 22 pp, 2026-10-22) | HTTP 200; metadata matches |
| Zenodo v4/v3/v2/v1 | `23540160`, `23510005`, `23436152`, `23429018` | HTTP 200 each; metadata matches |
| SSRN | `10.2139/ssrn.7631458` | public record per PUBLICATIONS; automated fetch 403 (SSRN bot block) — owner should open in a browser and confirm the title/status |
| Figshare | `10.6084/m9.figshare.34697025` | DOI resolves to article 34697025 (v1, 2026-10-19) |
| OSF / Law Archive | `osf.io/preprints/lawarchive/a8q5x_v1` | **pending moderation**, not a posted preprint; excluded from disclosure |
| IACR ePrint | submission 112662 | **declined**, not posted; excluded |
| Software Heritage | `swh:1:snp:dcae02ea…` (web URL) and `swh:1:rev:9101009d…` | both browse URLs return 200; historical snapshot covers the v1.3.0-era tree, not v2.2.0 |
| GitHub software release | `v2.2.0` + `.deb` | present; software, not a preprint |

The TIFS manuscript has **no self-preprint/Zenodo/SSRN entry in its reference list** (verified);
the concept DOI is mentioned only in the author footnote/reproducibility paragraph as disclosure.
The complete paste-ready list is `drafts/tifs/PREPRINT_DISCLOSURE.md`; the cover letter and portal
metadata include it.

## 3. Manuscript and package — PASS (with one formatting caveat)

| Check | Result |
|---|---|
| Build | official IEEEtran class + BibTeX; pdfLaTeX clean |
| Pages | **8** double-column pages (TIFS initial Regular Paper limit: **13**) |
| Abstract | **243 words** extracted from the built PDF (TIFS limit 150–250) |
| Citations | 34 cited keys, all resolve; 44 verified entries in `references.bib` (2015 IEEEtran.bst) |
| Figures/tables | 4 figures, 7 tables; all `\ref`/`\label` resolve; no `??` in text |
| Build warnings | 0 undefined citations, 0 BibTeX warnings, 0 LaTeX errors; 5 overfull hboxes (cosmetic, <8 pt) |
| Author block/ORCID | present and ORCID checksum valid |
| Index terms | present (5) |
| Artifacts | `ieee/main.pdf` (8 pp, 321,683 B, SHA-256 `fc6384cf…`), `IEEEtran_TIFS_submission.zip` (429,513 B, SHA-256 `c7c598a8…`), `ieee/main_sps_margins.pdf` (9 pp alternate), internal `TIFS_bundle_2026-10-24.zip` (hash reported after final bundle build); upload manifest in `drafts/tifs/SUBMISSION_MANIFEST_2026-10-24.md` |
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
| EDICS classification | **OWNER ACTION** — exact SPS Unified EDICS: **820 Watermarking and data hiding (IF-WAT)** primary; **847 Multimedia content authentication and plagiarism detection (IF-FOR-AUTH)** secondary; optional **840 Multimedia forensics (IF-FOR)** |
| Preprint disclosure | PASS in manuscript/metadata (Zenodo concept DOI 10.5281/zenodo.23429017; SSRN 10.2139/ssrn.7631458) |
| Not under consideration elsewhere | stated; prior SIGPRO desk rejection / DSP withdrawal disclosed |
| Patent/competing interests/funding | stated (UA a 2026 06266; none/none) |
| Code/data availability | statement present (harness + manifest + seeds from author); corpus/real PDFs are git-ignored, not in the submission |
| Legal review (technical seal vs company/notary seal) | **OWNER ACTION** — `drafts/tifs/LEGAL_REVIEW_CHECKLIST.md` |
| Portal account/email/declarations | **OWNER ACTION** — email placeholder in metadata |

## 5. Scientific risk — the real reason this is conditional, not automatic

1. **External anchors:** the ten project PDFs are the author's own public documents, but five
   independent NIST public standards (FIPS 186-5, 180-4, 202, SP 800-57, 140-3) have now been added,
   giving 150 samples with the same exact/fail-closed behaviour. This reduces — but does not fully
   remove — the external-validity concern; enterprise DMS pipelines remain future work.
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
5. Final owner read of title, 243-word abstract, cover letter, declarations.

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

- The **formal TIFS package is ready**: 8 pages ≤13, abstract 243 ≤250, clean IEEEtran/BibTeX build,
  valid ORCID, verified references, complete evaluation artifacts.
- The **submission is not yet owner-ready** because EDICS/portal/email/legal/margin actions are
  pending.
- The **scientific acceptance is not guaranteed**; the weakest point is external validity of the
  “real-world” anchors and the short length. For a serious TIFS attempt, add independent PDFs and
  expand the paper before submission; otherwise submit as-is only if speed matters more than
  acceptance probability.

**Recommendation: do not submit blindly today; do the four owner actions and one strengthening pass
(independent real-world PDFs + ~2 pages of depth), then submit.**

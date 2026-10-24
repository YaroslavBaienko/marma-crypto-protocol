# IEEE TIFS submission plan (primary target after the DSP withdrawal)

**Date:** 2026-10-23 · **Status (2026-10-24):** pre-submission — locally buildable IEEEtran PDF (10 double-column pages, 243-word abstract), evaluation complete, package/bundle rebuilt; no portal submission yet.
**Why TIFS:** the best topical fit for fragile watermarking/forensics; IEEE hybrid model lets the
author publish under the subscription route **without an APC** (open access remains optional).
**Portal:** IEEE Author Portal — https://ieee.atyponrex.com/journal/tifs-ieee (old ScholarOne link is obsolete)
**Format:** IEEE Transactions two-column; manuscript type "Regular Paper"; TIFS initial limit **13 double-column pages** including appendices and references (revised limit 16; over-length charges apply). Current PDF: 10 pages.

## Gate before submission

- [x] IEEE two-column manuscript built locally with official IEEEtran (10 pages incl. appendices + references; clean BibTeX).
- [x] Title/abstract finalised (watermarking-first; abstract trimmed to 243 words, TIFS limit 150–250).
- [x] Verified bibliography only (`references.bib`, 45 entries); audit passes and local build has no undefined citations/BibTeX warnings.
- [x] Evaluation lifted: 10 project PDFs + 10 independent public PDFs (200 samples) + PDF-level baselines (STDM, Fourier, LSB, 600 samples).
- [x] Physical print-scan set: 5 A4 pages (Canon MF3010, 300 dpi scan), 5/5 digital controls valid, 5/5 captures fail-closed.
- [x] TIFS cover letter prepared (`cover_letter_TIFS.pdf`); owner confirms final details at upload.
- [x] Author declarations prepared in `IEEE_PORTAL_METADATA.md`: no competing interests; pending UA patent a 2026 06266; preprint DOIs; no concurrent submission; data/code availability. Owner clicks the portal confirmations.

## Changes vs the DSP-v3 draft

1. IEEE formatting (two-column, IEEE reference style, index terms).
2. Real-world PDF anchors: contracts/bank statements/court-style PDFs from the project corpora
   (public documents only; no client data), stamped and attacked.
3. PDF-level baselines: STDM-DCT and Fourier-descriptor embedding on the same carrier, attacked in
   the stream, so the comparison is not slot-level only.
4. Per-generator breakdown and a table of failure modes (writer precision, flattening, truncation).
5. Reproducibility appendix pointer (harness, corpus manifest, seeds).

## Risk

TIFS reviewers are demanding on evaluation breadth and on security claims. The paper must keep the
"fragile, not robust" framing, avoid cryptographic-security claims, and report the capacity-limited
baselines honestly. If TIFS rejects, fallbacks are the Elsevier hybrid journals and MTAP; conference
(IH&MMSec/WIFS) remains a parallel option.

## Status 2026-10-23

- [x] Content draft expanded to 12 pages (single-column editing version).
- [x] Real-world anchors: 10 project PDFs + 10 independent public PDFs, 200 samples, results match the synthetic corpus.
- [x] PDF-level baselines: STDM-DCT, Fourier, LSB (600 samples).
- [x] Precision study: 9/8 decimals exact, 7/6 fail; writer-precision table.
- [x] IEEEtran/Overleaf package: `drafts/tifs/ieee/IEEEtran_TIFS_submission.zip`
      (main.tex, references.bib, figures, README; all 41 cited keys resolve against 49 verified entries).
- [x] Print-scan kit: `eval/printscan_kit.py` → five print-ready stamped PDFs + `printscan/README.md`;
      `eval/process_printscan.py` converts captures and records the expected fail-closed result.
- [x] Physical print-scan: five A4 pages printed on Canon MF3010 (600 dpi mono), scanned at 300 dpi grayscale; **5/5 digital controls valid, 5/5 physical captures absent (fail-closed)** — see `eval/printscan/RESULTS.md`.
- [x] Controlled verification run: 43 tests OK, seal-path branch coverage 85.0% (pdf_layer 72.3%, profiles 93.7%, harness 80.5%), cross-runtime JS ↔ Python 1024/1024, production signer ↔ eval 1024/1024, 12-sample matrix stable across two runs; report in `paper_v3/tests/controlled_run/` (current run: 43 tests, git `7a8e282`).
- [x] Production profile P2: additive wrapper `src/marma_seal_profiles.py` (42 mm round branded stamp, canonical carrier geometry unchanged, `data-profile` persisted in SVG metadata, verifier fails closed on unknown/mismatched profile and tampered geometry; legacy v1 untouched). Controlled run has 43 tests and a production-P2 gate: PASS.
- [x] CLI: production `--profile v2-round42` flag implemented and tested (sign/verify SVG; wrong profile exits 2; legacy v1 default unchanged); controlled suite now 43 tests.
- [ ] Legal review (owner + Ukrainian counsel): checklist at `drafts/tifs/LEGAL_REVIEW_CHECKLIST.md`; not legal advice.
- [x] Product integration: Nautilus action for the 42 mm seal + CLI `--profile` auto-detect on verify; release candidate `v2.2.0-1` built and package-tested (`bash build.sh --test` PASS). System install/tag/manual GUI are owner actions (see `RELEASE_NOTES_v2.2.0.md`).
- [x] PAdES whitepaper gate: root cause was test-environment PyMuPDF shadowing (1.25.4 vs 1.28.2), not data/code corruption; full production suite is **40/40 PASS** in the correct environment (`tests/README.md`, `requirements-dev.txt`). Residual product risk: pin PyMuPDF >= 1.28.2 or re-seal whitepapers with a version-stable canonicalisation.
- [x] Seal-only visual contract: removed human-visible captions under the seal in PDF/DOCX/universal-API signing; cryptographic metadata retained; 45/45 production tests incl. `tests/test_seal_visual_contract.py`; package RC `2.2.0-2` rebuilt and package-tested. Manual Nautilus re-check remains owner-side.
- [x] Nautilus selection bug fixed (URIs/paths/split-view resolver; 0 fallback chooser calls in the 15-scenario headless matrix); error dialogs and `MARMA_HEADLESS` added; production Suite 51/51; package RC `2.2.0-3` built/package-tested.
- [x] Real Nautilus GUI action exercised (Wayland, keyboard automation) → valid signed PDF, `seal_pages=last`, no visible caption; evidence in `docs/manual_test/2026-10-24/GUI_EVIDENCE.md`. Per-item manual walkthrough still optional.
- [x] Seal placement policy: `--seal-pages last|first|first-last|all` (default last), verified visible-seal presence on declared pages (PDF/universal/DOCX; SVG metadata); 65/65 production tests; package RC `2.2.0-4` built/package-tested; policy comparison + screenshots in `docs/visual_contract/` and `docs/manual_test/`.
- [x] Nautilus seal-placement dialog: settings action + per-action `ask` mode, config `~/.config/marma-crypto/config.json`, env override; 73/73 tests; package RC `2.2.0-5` built/package-tested.
- [x] IEEEtran package builds locally (pdfLaTeX+BibTeX, 0 undefined citations); Overleaf/portal re-build is a final owner confirmation.
- [ ] Owner: print/scan/photograph the five kit PDFs into `eval/printscan/raw/`; then run
      `python3 eval/process_printscan.py`.
- [ ] Owner: upload to IEEE Author Portal, select EDICS, confirm declarations/ORCID, submit. Final formatting polish + counsel review of the technical-seal wording remain.


## Readiness audit 2026-10-24 (authoritative; full report: `IEEE_READINESS_AUDIT_2026-10-24.md`; preprints: `drafts/tifs/PREPRINT_DISCLOSURE.md`; author requirements: `TIFS_AUTHOR_REQUIREMENTS.md`)

**Verdict: scientifically close, formally not yet submitted-ready.**

### Verified
- IEEEtran PDF: **10 pages**, two-column, 10 pt, clean BibTeX, 0 undefined citations, 41 cited keys from 49 verified entries; `main.pdf` built with official IEEEtran class.
- TIFS formal checks: initial Regular Paper **≤13 pages** (10 ok); abstract **243 words** (150–250 ok); ORCID present; keywords present; preprint relation/patent/funding/competing-interest statements present.
- Evaluation reproducible locally: 60 documents × 3 generators × 3 variants = 180 PDFs (manifest hashes PASS); 1,800 main + 360 variant + 720 ablation samples; 200 public/independent samples (10 project + 10 independent public); 600 PDF-level baseline samples; 5/5 physical fail-closed.
- Controlled run: PASS (43 tests, seal-path branch coverage 85.0%, 12-sample matrix stable, P2 gate PASS).
- Corpus/manifest and real-world source paths present; print-scan raw/captures present (not committed to git by policy).

### Formal blockers/owner steps before upload
1. **EDICS selection** in the portal tree (exact SPS Unified EDICS codes: 820 Watermarking and data hiding (IF-WAT); 847 Multimedia content authentication and plagiarism detection (IF-FOR-AUTH); optional 840 Multimedia forensics (IF-FOR)).
2. **Portal account/author details**: ORCID 0000-0001-6690-2603 and email are present in the manuscript/metadata; owner must confirm the account email and all author details.
3. **Margins check**: SPS text says ≥1 in margins; IEEEtran's default journal margins are ~0.68 in. Confirm the portal accepts the template PDF; otherwise rebuild with SPS template margins before upload.
4. **Legal review** of “technical seal vs company/notary seal” wording by Ukrainian counsel (`LEGAL_REVIEW_CHECKLIST.md`) — publication safety, not IEEE formatting.
5. **Owner final read** of title/abstract/cover letter; no suggested reviewers invented.

### Scientific risk (not a formal blocker, but reviewer-facing)
- 10 pages is inside the 13-page limit; the independent NIST anchors and expanded appendices address the earlier depth concern.
- Deterministic exactness on a synthetic corpus + 10 public documents; no hypothesis tests (explicitly stated). The paper already limits claims to fragile authentication and reports a capacity–distortion frontier, but TIFS reviewers may demand stronger deployment breadth.
- Baselines are same-carrier re-implementations, not state-of-the-art full systems; acknowledged in threats-to-validity.
- Single printer/scanner pair; acknowledged as a limitation.

**Recommendation:** after owner legal read + EDICS/portal declarations, submit as a Regular Paper; the formal package is ready. Do not claim cryptographic security or robust watermarking beyond the stated scope.

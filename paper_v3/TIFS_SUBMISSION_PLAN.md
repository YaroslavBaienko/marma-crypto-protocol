# IEEE TIFS submission plan (primary target after the DSP withdrawal)

**Date:** 2026-10-23 · **Status:** pre-submission work.
**Why TIFS:** the best topical fit for fragile watermarking/forensics; IEEE hybrid model lets the
author publish under the subscription route **without an APC** (open access remains optional).
**Portal:** IEEE Author Portal (ScholarOne) — https://mc.manuscriptcentral.com/tifs-ieee
**Format:** IEEE Transactions two-column; manuscript type "Regular Paper"; no strict page limit
(over-length charges apply beyond the free pages — check the current TIFS author guidelines).

## Gate before submission

- [ ] v3 manuscript in IEEE two-column layout (Typst approximation for review; IEEEtran/Word for the
      accepted version — LaTeX is not installed on this machine).
- [ ] Title/abstract unchanged from the DSP-v3 framing (already watermarking-first).
- [ ] Verified bibliography only (`references.bib`, 44 entries); audit passes.
- [ ] Evaluation lifted: 10–20 real-world PDFs + PDF-level baselines (STDM, Fourier, LSB, DE).
- [ ] Physical or phone-camera print-scan set, or an explicit limitation statement.
- [ ] TIFS cover letter (no transfer context needed; state novelty and relation to the preprint).
- [ ] Author declarations: no competing interests; pending UA patent a 2026 06266; preprint DOIs;
      no concurrent submission; data/code availability.

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
- [x] Real-world anchors: 10 public PDFs, 100 samples, results match the synthetic corpus.
- [x] PDF-level baselines: STDM-DCT, Fourier, LSB (600 samples).
- [x] Precision study: 9/8 decimals exact, 7/6 fail; writer-precision table.
- [x] IEEEtran/Overleaf package: `drafts/tifs/ieee/IEEEtran_TIFS_submission.zip`
      (main.tex, references.bib, figures, README; all 30 cited keys resolve against 44 verified entries).
- [x] Print-scan kit: `eval/printscan_kit.py` → five print-ready stamped PDFs + `printscan/README.md`;
      `eval/process_printscan.py` converts captures and records the expected fail-closed result.
- [x] Physical print-scan: five A4 pages printed on Canon MF3010 (600 dpi mono), scanned at 300 dpi grayscale; **5/5 digital controls valid, 5/5 physical captures absent (fail-closed)** — see `eval/printscan/RESULTS.md`.
- [x] Controlled verification run: 30 tests OK, seal-path branch coverage 85.0% (pdf_layer 72.3%, profiles 93.7%, harness 80.5%), cross-runtime JS ↔ Python 1024/1024, production signer ↔ eval 1024/1024, 12-sample matrix stable across two runs; report in `paper_v3/tests/controlled_run/`.
- [x] Production profile P2: additive wrapper `src/marma_seal_profiles.py` (42 mm round branded stamp, canonical carrier geometry unchanged, `data-profile` persisted in SVG metadata, verifier fails closed on unknown/mismatched profile and tampered geometry; legacy v1 untouched). Controlled run now has 35 tests and a production-P2 gate: PASS.
- [x] CLI: production `--profile v2-round42` flag implemented and tested (sign/verify SVG; wrong profile exits 2; legacy v1 default unchanged); controlled suite now 39 tests.
- [ ] Legal review (owner + Ukrainian counsel): checklist at `drafts/tifs/LEGAL_REVIEW_CHECKLIST.md`; not legal advice.
- [x] Product integration: Nautilus action for the 42 mm seal + CLI `--profile` auto-detect on verify; release candidate `v2.2.0-1` built and package-tested (`bash build.sh --test` PASS). System install/tag/manual GUI are owner actions (see `RELEASE_NOTES_v2.2.0.md`).
- [x] PAdES whitepaper gate: root cause was test-environment PyMuPDF shadowing (1.25.4 vs 1.28.2), not data/code corruption; full production suite is **40/40 PASS** in the correct environment (`tests/README.md`, `requirements-dev.txt`). Residual product risk: pin PyMuPDF >= 1.28.2 or re-seal whitepapers with a version-stable canonicalisation.
- [x] Seal-only visual contract: removed human-visible captions under the seal in PDF/DOCX/universal-API signing; cryptographic metadata retained; 45/45 production tests incl. `tests/test_seal_visual_contract.py`; package RC `2.2.0-2` rebuilt and package-tested. Manual Nautilus re-check remains owner-side.
- [x] Nautilus selection bug fixed (URIs/paths/split-view resolver; 0 fallback chooser calls in the 15-scenario headless matrix); error dialogs and `MARMA_HEADLESS` added; production Suite 51/51; package RC `2.2.0-3` built/package-tested.
- [ ] Owner: real mouse click-through in Nautilus after installing the RC (Wayland input automation unavailable to this agent).
- [x] Seal placement policy: `--seal-pages last|first|first-last|all` (default last), verified visible-seal presence on declared pages (PDF/universal/DOCX; SVG metadata); 65/65 production tests; package RC `2.2.0-4` built/package-tested; policy comparison + screenshots in `docs/visual_contract/` and `docs/manual_test/`.
- [x] Nautilus seal-placement dialog: settings action + per-action `ask` mode, config `~/.config/marma-crypto/config.json`, env override; 73/73 tests; package RC `2.2.0-5` built/package-tested.
- [ ] Owner: build the zip in Overleaf (pdfLaTeX + BibTeX) and confirm it compiles with no `??`.
- [ ] Owner: print/scan/photograph the five kit PDFs into `eval/printscan/raw/`; then run
      `python3 eval/process_printscan.py`.
- [ ] Final IEEE formatting polish and submission via IEEE Author Portal.

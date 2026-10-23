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

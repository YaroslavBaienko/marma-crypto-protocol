**STATUS: CLOSED — the DSP submission was removed on 2026-10-23 (mandatory Gold-OA APC $2,900 declined); this file is kept as the record of the transfer flow. See PUBLICATIONS.md §5.2b and TIFS_SUBMISSION_PLAN.md.**

# DSP transfer — completion plan (transfer confirmed 2026-10-23)

**Status:** transfer confirmed by Elsevier; submission at *Digital Signal Processing* (IF 3.4,
CiteScore 6.9, Gold OA APC $2,900) is **in progress and not completed**. The portal lets us
revise before completing, so the transferred v2.0 files are a placeholder, not the submission.

## Non-negotiables

1. **Never complete the submission with v2.0.** Its bibliography contains 8 unverifiable entries
   and wrong DOIs/venues (see `REFERENCE_AUDIT.md`). Submit only the v3 text with
   `references.bib` (verified-only) and the audit gate passing.
2. **Do not pay the APC before acceptance.** Before accepting, ask Elsevier about waivers or
   discounts applicable to Ukrainian authors; the APC is due on acceptance, not on submission.
3. **Check the completion deadline** in the "complete your submission" email / transfer portal
   (Elsevier transfer invitations typically expire; if the window is too short, ask the DSP
   editorial office to extend it — the transfer is already recorded, and they can re-issue the link).

## Minimum viable v3 for DSP (what must be true at completion)

| Item | Current state | Needed |
|---|---|---|
| Title / abstract | re-framed draft exists (`REFRAME_ABSTRACT.md`) | final DPX-ready wording |
| Bibliography | 44 verified entries (`references.bib`) | every citation resolves; audit script green |
| Related work | rebuilt outline | written from verified sources only |
| Evaluation | PDF-level results (1,800 samples), carrier ablation, same-carrier baselines (slot level) | lift baselines to PDF level (stretch); report honestly |
| Corpus | 180 PDFs, 3 generators, 3 variants | add 10 real-world PDFs if time permits |
| Physical print-scan | simulation only | optional for DSP; state it as simulated |
| Scope framing | watermarking-first | remove crypto/legal bulk; keep one deployment subsection |
| Companion material | optical/universal/API | removed from this paper |
| Length | draft-1 is 5 pp | 12–16 pp (DSP typical) |

## Suggested timeline (adjust to the actual deadline)

- **Day 1–2:** finalise title/abstract/intro/contributions; freeze bibliography gate script.
- **Day 3–5:** write Related Work from verified sources; write Method section with the exactness
  argument and the PDF-writer precision requirement.
- **Day 6–8:** write Evaluation with the measured tables/figures; add PDF-level baselines if
  feasible; state limitations explicitly.
- **Day 9–10:** DSP cover letter + portal upload; request APC waiver/discount; internal read-through.
- **Optional stretch:** real print-scan (phone photo) and 10 real PDFs, only if they fit before the
  deadline; otherwise reported as future work.

## Cover-letter points (DSP)

- Transfer context: SIGPRO-D-26-04464 desk-rejected on scope, transferred at Elsevier's suggestion.
- What changed on transfer: new title/abstract framing for DSP, verified references, new PDF-level
  evaluation and carrier ablation; optical/API material moved to a companion paper.
- Fit: fragile watermarking / QIM / document authentication are core DSP topics; the paper reports
  capacity–distortion trade-offs on the same carrier.
- Honesty: baselines that are capacity-limited are reported as such; no claim of cryptographic
  security from the watermarking argument; not a replacement for PAdES/eIDAS.

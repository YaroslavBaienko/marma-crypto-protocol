# Marma v3 — plan for a watermarking/forensics paper (14–16 pp)

**Status:** planning + bibliography audit done (2026-10-23). No submission before the reference
audit gate and the evaluation matrix below pass.

## Target venues (decide after the evaluation)

| Venue | Fit | Draft length | Notes |
|---|---|---|---|
| IEEE TIFS | best topical fit | 14–16 pp | needs real corpus + re-implemented baselines |
| ACM TOMM | good | 16–18 pp | multimedia evaluation expected |
| EURASIP J. Information Security | good (applied) | 14–16 pp | OA APC |
| Multimedia Tools and Applications | broad, faster | 12–14 pp | fallback for a sound-but-narrow result |
| IEEE Access | fast, soundness-based | 12–14 pp | last-resort speed, APC |
| ACM IH&MMSec / IEEE WIFS | conference first | 8–10 pp | deadline-driven; good peer-reviewed line |

Pre-submission check: 5 recent papers per venue; reference overlap ≥30% with our verified list;
scope sentence matched to the venue's aims.

## Structure and page budget

1. **Introduction** (1.5 pp) — signature-valid / page-not-valid problem; one running example; contributions.
2. **Related work** (2 pp) — QIM & dither (Chen–Wornell, Eggers, Pérez-González); spread-spectrum/security (Cox, Cayre); RDH (Tian, Ni, Thodi); 2D vector graphics/maps (Wang 2014, Peng 2019, Doncel 2007, Li–Xu 2003, Hou 2014, Mouhamed 2012, Ohbuchi); PDF watermarking (Hatoum); PDF signature attacks (Mladenov 2019, Mainka 2021, Rohlmann 2021); standards in one paragraph.
3. **Threat model & requirements** (1.25 pp) — what "valid signature, different page" means; attacker capabilities; fragile vs robust; success criteria.
4. **Method** (3.5 pp) — geometry carrier; exact lattice & rounding bound; digest binding; keyed dither; recipient channel; verification algorithm.
5. **Evaluation** (4 pp) — corpus, baselines, attacks, metrics, results, ablation.
6. **Security discussion** (1.25 pp) — what is and is not proven; relation to PAdES certification; failure modes.
7. **Limitations & conclusion** (1 pp).

Appendix/supplement: geometry theorem; implementation details; full tables.

## Evaluation protocol (the missing evidence)

**Corpus (`paper_v3/eval/build_corpus.py`, to be implemented):**
* 60 documents × 3 generator families:
  * 20 produced by **LibreOffice** (DOCX → PDF; contracts/memos),
  * 20 produced by **Typst** (reports/whitepapers),
  * 20 produced by **browser print** (Chromium headless; invoices/letters),
* each document in three variants: native PDF, **flattened** (raster 300 dpi → image-only PDF),
  **print-scan simulated** (raster 200 dpi + blur + sensor noise + JPEG q=70 → PDF).
* 10 real-world PDFs from the project's existing corpora as sanity anchors (no client data).
* Manifest: `corpus_manifest.json` with generator, variant, pages, bytes, sha256.

**Carriers:** `sri-yantra` (26+1 DoF), `generic-18-gon`, `grid` — equal visible area (±2%) and
equal payload (266 bits) so the ablation is fair.

**Baselines re-implemented on the same carrier (never quoted from papers):**
1. scalar QIM (Chen–Wornell, Δ tuned to equal RMSE);
2. spread-transform dither modulation (equal distortion);
3. difference-expansion RDH (Tian-style, capacity-matched);
4. prediction-error expansion (Thodi-style) where applicable;
5. Fourier-descriptor watermarking (Doncel-style, 2D vector graphics);
6. control: no embedding + geometry-only perturbation.

**Attacks:** vertex edit (+1e-4 pt), coordinate truncation (`%.8f`, `%.7f`, `%.6f`), page rescale,
translation (CTM), flattening, print-scan simulation, cropping/partial seal, QR-detachment analogue.

**Metrics:** capacity (bits), geometric RMSE (pt) and PSNR_geom, BER after each attack, tamper
detection rate and false-positive rate, runtime (ms/verify), payload-to-area ratio (bits/cm²).

**Statistics:** 30 seeds × corpus; mean ±95% CI; paired Wilcoxon for ablation/baselines; report
effect sizes, not only p-values.

**Ablation:** carrier type (sri-yantra vs 18-gon vs grid); keyed vs unkeyed dither; recipient channel
present vs absent; digest length 128/256/512 bits.

## Split plan

| Artifact | Where |
|---|---|
| v3.0 watermarking paper (this plan) | TIFS/TOMM/EURASIP JIS |
| Marma-Optical + Universal emblems + API | companion paper (IH&MMSec/WIFS first, then journal) |
| Geometry theorem | appendix of v3 or a short note |
| Deployment (PAdES/DSTU, GOST/Kupyna) | one subsection + supplement |

## Task checklist

- [x] Reference audit; verified-only `references.bib` (44 entries).
- [x] Title/abstract/contribution re-framing.
- [ ] `build_corpus.py` + `corpus_manifest.json` (60 PDFs, variants).
- [ ] Carrier module + metric module (`eval/carriers.py`, `eval/metrics.py`).
- [ ] Baseline implementations (same carrier, equal distortion).
- [ ] Attack harness + results tables/figures.
- [ ] Ablation (geometry / dither / recipient channel).
- [ ] v3 manuscript in Typst, 14–16 pp, figures from the harness only.
- [ ] Venue pre-check (5 papers/venue, ≥30% reference overlap) before submission.

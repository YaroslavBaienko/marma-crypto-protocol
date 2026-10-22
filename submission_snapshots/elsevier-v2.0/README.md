# Frozen submission snapshot — v2.0 (Elsevier JISA + SIGPRO)

Immutable record of the manuscript version that was actually submitted to Elsevier.
Frozen on 2026-10-22 from the author's local `submission_elsevier_jisa/` working folder,
so that the repository can reproduce the submitted state without publishing the rest of
the per-journal working folder.

## What was submitted

| Journal | Manuscript No. | Submitted | Outcome |
|---|---|---|---|
| Journal of Information Security and Applications (JISA) | `JISAS-D-26-07950` | 2026-10-19 | Rejected 2026-10-20 (EiC A. T. S. Ho: scope fit confirmed, novelty/depth insufficient) |
| Signal Processing (EURASIP) | `SIGPRO-D-26-04464` | 2026-10-21 13:51 EEST | Under review |
| Computers & Security (COSE) | `COSE-D-26-06638` | 2026-10-20 | Returned without review (scope policy) |

JISA and SIGPRO received byte-identical manuscript PDFs (`01_Manuscript_*.pdf`).

## Files

- `Marma_Crypto_Elsevier_JISA_Edition.typ` — Typst source of the submitted 21-page manuscript (v2.0).
- `01_Manuscript_Marma_Crypto_JISA.pdf`, `01_Manuscript_Marma_Signal_Processing.pdf` — submitted PDFs.
- `03_Highlights_JISA.txt`, `03_Highlights_Signal_Processing.docx` — highlights as sent.
- `figures/*.svg` — the five vector figures referenced by the manuscript.
- `SHA256SUMS` — integrity manifest.

## Withheld correspondence (not published)

The cover letters contain the author's e-mail address and per-journal declarations, so they
are deliberately **not** committed to the public repository. They remain in the author's
local `submission_elsevier_jisa/` folder. Their SHA-256 digests, recorded at freeze time,
are kept here for accountability:

| Withheld file | SHA-256 |
|---|---|
| `02_Cover_Letter_JISA.txt` | `5a382d97fea45c5693a75e89402ed60728bfa3302ef05f30ce1cd0fca8eadd24` |
| `02_Cover_Letter_Elsevier_Signal_Processing.txt` | `0651700a07ad1287c057f8f3f6d70e5647d6546dabed8b9eb21fc187415ebc89` |

## Rules

1. **Do not edit anything in this directory.** It is a frozen evidence artifact.
   `tests/test_manuscript_v2_cross_verification.py` verifies every hash in `SHA256SUMS`.
2. The rest of the live working folder `submission_elsevier_jisa/` stays gitignored;
   only this frozen snapshot is in git.
3. The current archival edition is `whitepaper/Marma_Crypto_IACR_LNCS_Edition.typ`
   (v2.1.0). It must **supersede**, never equal, this snapshot — a later manuscript
   update must not rewrite what the journals received.

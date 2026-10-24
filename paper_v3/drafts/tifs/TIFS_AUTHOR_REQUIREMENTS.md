# TIFS author requirements — fixed for RES-MARMA-CRYPTO

**Source:** IEEE Signal Processing Society, *Information for Authors* —
https://signalprocessingsociety.org/publications-resources/information-authors
**Fetched / fixed:** 2026-10-24 (page is the current SPS Transactions & Journals policy; TIFS-specific
scope/reproducibility page: https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security)
**Article:** *Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on
Vector Geometry* — IEEE TIFS Regular Paper
**Author:** Yaroslav V. Baienko (ORCID 0009-0006-7498-2133)

## 0. Tenant pass (RES-MARMA-CRYPTO)

- Tenant: **`RES-MARMA-CRYPTO`** (PUBLIC), Qdrant collection **`RES_MARMA_CRYPTO_bge`**.
- `project_facts` returned 6 PUBLIC facts (release registry, patent strategy, v1.3.0 release,
  cryptographic bridge, Theorem 1, attack classes I–III); **no TIFS-author-guidelines fact**.
- Qdrant semantic search for TIFS/author-guideline requirements returned prior submission/preprint
  documents and PUBLICATIONS.md, **not the current SPS policy page**.
- Therefore this file records the authoritative external requirements for this article; it is the
  canonical repo-side requirements matrix. The MCP surface available in this session is read-only,
  so nothing was written to Supabase/Qdrant; if a HOT fact is wanted, it must go through the declared
  `knowledge_os` ingestion/writer path.

## 1. Venue and article type

- Submit to **IEEE Transactions on Information Forensics and Security (TIFS)** via **IEEE Author
  Portal**: https://ieee.atyponrex.com/journal/tifs-ieee (the old ScholarOne site is obsolete).
- Article type: **Regular Paper** (complete disclosure of a technical premise). Not Comment
  Correspondence, Overview Article, or Rebuttal.
- Review is **single-anonymized**: reviewers know author identities; author identities are not
  hidden. Minimum **two independent reviewers**; plagiarism screening before acceptance.
- Scope: information forensics/security, including watermarking/data hiding, multimedia content
  authentication and document security. The paper’s fragile-AI/PDF-seal topic fits; EDICS below.

## 2. Mandatory author/manuscript assertions

1. Not under consideration elsewhere and not previously published.
2. All listed authors agree on authorship/order; figures, tables and results accurately reflect the
   experimental work.
3. All authors accept all applicable APCs, overlength page charges and OA fees; charges are
   non-negotiable. The corresponding author obtains co-author/sponsor consent.
4. Scope/novelty: the manuscript must state (a) the problem and contribution, (b) why it is
   significant, (c) the closest published literature, and (d) what is distinctive/new relative to
   that literature.
5. **Immediate-rejection triggers:** lack of novelty; insufficient experimental data; improper
   English; too many typographical/grammatical errors; insufficient citations.
6. **Author misconduct:** plagiarism, self-plagiarism (uncited reuse/duplicate submission/
   substantial overlap) and research misconduct are prohibited; inappropriate language is an
   immediate-rejection trigger.

## 3. Manuscript format and page limits

- PDF, **double-column, single-spaced, 10-point font, margin ≥1 inch on all sides**; IEEE style
  files (LaTeX/Word Template Selector).
- **Initial Regular Paper limit: ≤13 double-column pages**, including title, authors’ complete
  contact information, abstract, text, all figures/tables, appendices/proofs and references.
  Supplemental/graphical abstract pages are not counted.
- **Revised Regular Paper limit: ≤16 pages**, including title/authors/abstract/text/figures/tables/
  references; appendices/proofs become Supplemental Materials and do not count.
- Resubmissions are treated as new submissions and must be **≤13 pages**.
- Abstract: **150–250 words**, self-contained, no abbreviations/footnotes/display equations/
  references; include a few keywords/phrases.
- Index terms/keywords required; graphical abstract optional.
- Native-language author names are allowed alongside English names.
- At each revision stage upload a **“Formatted (Double Column) Main File – PDF Document Only”** that
  is publication-ready; remove colored annotations/acknowledgments except final ones. After
  acceptance IEEE/SPS does not permit manuscript changes.
- **Color graphics are free** (online-only journals).

## 4. Submission package

1. Author Portal account; **ORCID required for every author**; all author names/affiliations must
   match manuscript and portal.
2. Electronic manuscript PDF (formatted as above).
3. **EDICS classification** (choose most appropriate; failure may delay review).
4. PDFs of all reference-list items that are **not publicly available** (e.g. unpublished
   manuscripts), with short space-free filenames.
5. Graphical abstract and supplemental materials intended for the final paper must be uploaded at
   initial submission; each upload needs a description.
6. Cover letter and declarations (originality, prior/preprint disclosure, patent, conflicts,
   funding, data/code availability).
7. Copyright: IEEE eCF after acceptance (electronic Copyright Form in Author Portal).

## 5. Supplemental materials / reproducibility

- Optional supplemental material may include multimedia, datasets, code/software, extra proofs,
  simulations. Equations/theorems/tables/figures must be numbered consecutively with the main paper.
- Recommended supplemental limit: **≤6 double-column pages** without explicit EiC approval; longer
  needs EiC approval.
- TIFS **encourages reproducibility**: authors are encouraged to make code/data that recreate the
  figures available; TIFS journal page specifically encourages publishing code/data online or as
  supplemental material. Not a hard gate, but reviewers value it.

## 6. Preprints — TIFS two-track rule (critical for this article)

- **Preprints identical to the submitted manuscript** (minor differences only): may be posted;
  at submission provide a complete list including URLs; **do not put them in the reference list**.
- **Other posted preprints** (not identical to the submitted manuscript): considered prior work;
  cite them in the manuscript when relevant.
- If the manuscript is **based on** other posted preprints, explain in detail how they relate and
  why they are not prior work; related preprints must be properly cited in the manuscript.
- This article: TIFS v3 is **not identical** to any posted preprint. The latest Zenodo edition is
  now cited as `baienko2026preprint` (DOI 10.5281/zenodo.23560975; concept 10.5281/zenodo.23429017)
  with the relation explained. Full list: `drafts/tifs/PREPRINT_DISCLOSURE.md`.

## 7. Resubmission of previously rejected manuscripts

At submission the portal may ask whether the manuscript is new or a resubmission of an earlier
rejected manuscript from any journal/conference. If it is a resubmission, a supporting document with
**verbatim quotations of all relevant previous review reports** and how they were addressed is
required; if rejected for scope, provide motivation why it is in scope.

For this article:
- The TIFS v3 manuscript itself is a **new submission**; it has not been submitted to TIFS or any
  other journal.
- Earlier versions/research line had editorial decisions: JISA rejection (EiC: insufficient
  novelty/depth), SIGPRO desk rejection (out of scope), COSE return-without-review (scope policy),
  DSP transfer withdrawn before submission; no peer-review reports were issued for those desk
  decisions. `PUBLICATIONS.md` §2/§5 preserves the exact record.
- If asked, answer “new submission”; provide the prior-decision statement rather than claiming no
  prior versions existed. Do not submit two overlapping manuscripts elsewhere.

## 8. Journal requirements mapped to this article

| ID | Requirement | This article / package | Status |
|---|---|---|---|
| T01 | Regular Paper via IEEE Author Portal | `ieee/main.pdf`; portal not yet submitted | READY |
| T02 | Single-anonymized review, ≥2 reviewers | Policy noted; no action | N/A |
| T03 | No concurrent/previously published | No active other submission; prior venues disclosed | READY |
| T04 | Clear problem/contribution/significance/novelty | Introduction + abstract; narrow claim | READY, reviewer risk |
| T05 | Sufficient experimental data | 180 corpus PDFs (hashes PASS), 1,800 main + 360 variant + 720 ablation, 200 anchors (10 project + 10 independent public), 600 baselines, 5/5 physical | READY, reduced external-validity risk (10 independent public anchors) |
| T06 | Proper English / no typo flood | IEEEtran build clean; owner final proofread | PARTIAL (owner) |
| T07 | Sufficient citations/related work | 49 verified entries, 41 cited keys; no missing citations | READY |
| T08 | ORCID + accurate author info | ORCID valid; email/profile owner | PARTIAL (owner) |
| T09 | Double-column 10 pt PDF | IEEEtran; 10 pages | READY |
| T10 | Margins ≥1 inch | IEEEtran default ~0.68 in; `main_sps_margins.pdf` (11 pp with 1-inch side margins) is provided as the alternate if the portal requires it | **GAP/CHECK** |
| T11 | Initial ≤13 pages | 10 pages | READY |
| T12 | Abstract 150–250 words, self-contained | 243 words; no refs/equations; standard acronyms PDF/PAdES/eIDAS used | READY (minor acronym note) |
| T13 | Keywords/index terms | 5 terms | READY |
| T14 | EDICS classification | 820 IF-WAT primary; 847 IF-FOR-AUTH secondary; 840 IF-FOR optional | READY |
| T15 | Non-public reference PDFs uploaded | All 45 refs are public standards/papers; no confidential refs known | READY/N/A |
| T16 | Supplemental material ≤6 pages (if used) | No supplemental upload; code/data statement + GitHub release | N/A/READY |
| T17 | Reproducibility/code/data encouraged | Harness, manifest, seeds; software release v2.2.0; corpus/real PDFs not committed | PARTIAL (optional) |
| T18 | Preprint two-track rule | Related Zenodo cited/explained; full list in disclosure; no identical preprint | READY |
| T19 | Resubmission/prior-rejection statement | New submission; prior decisions documented, no review reports | READY/PREPARE IF ASKED |
| T20 | Cover letter and declarations | `cover_letter_TIFS.pdf`, `PREPRINT_DISCLOSURE.md`, metadata | READY |
| T21 | Page charges acknowledged | $110/page voluntary first 10; $220/page mandatory >10; current 10 pages | ACKNOWLEDGE |
| T22 | OA/hybrid choice | Subscription route, no APC; OA optional | READY |
| T23 | Copyright eCF | After acceptance | POST-ACCEPT |
| T24 | Final “Formatted (Double Column) Main File” | Current `main.pdf`; final after revision | READY |
| T25 | Publication-ready no post-accept changes | Keep source/PDF under version control | PROCESS |
| T26 | Scope fit | TIFS information forensics/security; watermarking/document security | READY |

Legend: READY = satisfied in package; PARTIAL = owner/format check; GAP = action needed.

## 9. Must-fix before Submit

1. **Margin check**: SPS requires ≥1 in; IEEEtran gives ~0.68 in. Either confirm the portal accepts
   the official IEEEtran PDF or rebuild with SPS 1-inch margins before upload.
2. **Owner final proofread** of title/abstract/cover letter and English; T03/T06/T08/T19/T21/T23.
3. **Portal author profile**: existing IEEE account, email, ORCID, affiliation.
4. **EDICS**: 820 primary, 847 secondary, optional 840.
5. **Preprints**: paste the disclosure text; cite relation already fixed.
6. **Prior venues**: if portal asks, use the prepared new-submission/prior-decision statement.
7. **Page-charge budget**: current 10 pages; if accepted/typeset >10 pages, mandatory $220/page for
   pages 11+; voluntary $110/page for first 10.
8. **Scientific decision**: current external anchors are the author’s own public project documents;
   for a stronger TIFS attempt add 5–10 independent public PDFs and expand to ~10–12 pages. This is
   not a formal gate but is the main acceptance risk.

## 10. After acceptance

- Sign IEEE eCF in Author Portal.
- Submit final IEEE style files (“Formatted (Double Column) Main File – PDF Document Only”) and any
  supplemental material.
- Author biographies/photos and final metadata as requested by the production system.
- Pay applicable page charges/OA if chosen; mandatory overlength charges cannot be waived.
- Review proofs; no substantive changes after acceptance.

## 11. Sources

- SPS Information for Authors: https://signalprocessingsociety.org/publications-resources/information-authors
- TIFS journal scope/reproducibility: https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security
- IEEE Author Portal: https://ieee.atyponrex.com/journal/tifs-ieee
- SPS Unified EDICS (April 2026): https://signalprocessingsociety.org/publications-resources/unified-edics
- This repo: `IEEE_READINESS_AUDIT_2026-10-24.md`, `drafts/tifs/PREPRINT_DISCLOSURE.md`,
  `drafts/tifs/SUBMISSION_MANIFEST_2026-10-24.md`, `drafts/tifs/IEEE_PORTAL_METADATA.md`.

## Appendix A — page-charge budget for this article

TIFS page charges are based on the **published/typeset** Regular Paper, not on the submitted PDF.
Voluntary charges apply to the first ten pages; mandatory charges apply above ten.

| Published pages | Voluntary $110/page (first 10) | Mandatory $220/page (>10) | Total if voluntary charges are accepted |
|---:|---:|---:|---:|
| 8 | $880 | $0 | $880 |
| 10 | $1,100 | $0 | $1,100 |
| 12 | $1,100 | $440 | $1,540 |
| 14 | $1,100 | $880 | $1,980 |
| 16 | $1,100 | $1,320 | $2,420 |

Current submission PDF: 10 pages. A revision/typeset expansion above 10 pages creates mandatory
charges; plan a conservative budget of ~$1,540 for a 12-page accepted paper. OA (optional) is
additional; subscription/hybrid route has no APC.

# IEEE submission playbook — TIFS v3 (2026-10-25)

**Purpose:** capture the full IEEE/TIFS preparation, cross-verification, portal flow and post-submission
state so the same process is repeatable and auditable. The reusable agent skill is
`skills/ieee-publication-prep/SKILL.md` (installed at `~/.agents/skills/ieee-publication-prep`).

**Current state:** **SUBMITTED** to IEEE TIFS 2026-10-25. Portal UUID
`0e4ee084-bfb8-4eaf-afbf-b1707e9d1194`; **Manuscript ID `T-IFS-29736-2026`** assigned via IEEE SPS follow-up email (2026-10-25 02:16 EET).
Frozen record: [`paper_v3/drafts/tifs/SUBMISSION_CONFIRMATION_2026-10-25.md`](drafts/tifs/SUBMISSION_CONFIRMATION_2026-10-25.md).

---

## 1. Venue and requirements (TIFS)

| Item | Requirement / decision |
|---|---|
| Journal | IEEE Transactions on Information Forensics and Security |
| Article type | Regular Paper |
| Initial page limit | **≤13 double-column pages** incl. appendices/references |
| Revised page limit | ≤16 pages |
| Abstract | **150–250 words**; current: 243 metadata words (242 source) |
| Layout | IEEEtran two-column, 10 pt; official class |
| Margins | SPS guidance ≥1 inch; standard IEEEtran narrower — compliant alternate `main_sps_margins.pdf` (11 pp) exists; submitted standard IEEEtran |
| ORCID | `0000-0001-6690-2603` (verified against ORCID API; matches portal/manuscript/cover) |
| EDICS | `IF-WAT-MODL` Theoretical models; `IF-FOR-AUTH` Multimedia content authentication and plagiarism detection |
| Subject categories | Watermarking and Data Hiding; Multimedia Forensics |
| Page charges | voluntary $110/page first 10; mandatory $220/page above 10 |
| Preprints | identical copy listed, not in reference list; related non-identical preprints cited as prior art |
| Code | public GitHub release `v2.2.0`; Code Ocean optional |
| Data | no IEEE DataPort deposit (answer `No`); corpus/code availability stated in manuscript/repo |
| COI/funding | none / no funding |
| Copyright | IEEE eCF after acceptance |

## 2. Artifact freeze

| File | Bytes | SHA-256 |
|---|---|---|
| `drafts/tifs/ieee/main.pdf` | 342,649 | `41f9c37ecf319c23afe5f5cdb996af0f1b304fcc114db352635e0f967fee6480` |
| `drafts/tifs/ieee/IEEEtran_TIFS_submission.zip` | 452,570 | `66c606bcb94e8c14191b539c6c45729469935ea978ef1f5ac899e19ebb8be31e` |
| `drafts/tifs/cover_letter_TIFS.pdf` | 37,639 | `f97624c33028d7c5c907f91c6637f3323301cd560daeb800759457e09619252b` |
| Atypon Reviewer PDF (downloaded) | 2,477,047 | `9cf8f732206035119f565ab7bb911007f4394a984865dd633fc46af527f29666` |
| Internal bundle | — | `f44b4a7ca1f38c8206a33501c1e63e45905af80d3d8733513558b94005b72372` |
| Paper release | — | https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/tifs-v3 |

**Reviewer PDF:** 40 pages = portal metadata (1–2) + blank Atypon separator (3) + 10-page manuscript
(4–13) + 3-page preprint disclosure + 22-page prior Zenodo v5 + 2-page prior-submission statement.
The cover letter is not shown to reviewers.

## 3. Portal flow completed

1. Article type → **Regular Paper**.
2. Upload Manuscript:
   - Main Document - LaTeX: `IEEEtran_TIFS_submission.zip` (root `main.tex`);
   - Main Document - PDF: `main.pdf`;
   - conflict-of-interest checkbox: none;
   - optional fields left empty except cover letter; supporting docs prior statement.
3. Title → exact manuscript title.
4. Abstract → 243-word TIFS abstract.
5. Authors / Affiliations / Author Details:
   - Yaroslav V. Baienko, `zerhug@gmail.com`, Ukraine, corresponding/submitting author;
   - no affiliation (independent researcher);
   - CRediT: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation,
     Visualization, Project administration, Resources, Writing – original draft/review & editing;
   - ORCID `0000-0001-6690-2603`.
6. Match Organizations → no affiliation.
7. Additional Information:
   - EDICS and subject categories as above;
   - previously submitted to this journal: **No**;
   - human/animal subjects: **No/No**;
   - previously published: **Yes** (public preprints/author copy; files uploaded);
   - code: **Yes**; data: **No** (no DataPort);
   - rejected/related: **Yes** with JISAS-D-26-07950, SIGPRO-D-26-04464, COSE-D-26-06638;
   - conference extension: **No**; other unpublished/accepted/under-review papers: **No**;
   - identical preprint: **Yes** — GitHub `tifs-v3`, not in reference list;
   - other preprints not prior art: **No**;
   - scope/significance/three related papers/distinctiveness filled.
8. Reviewer PDF built by Atypon and downloaded for audit.
9. Complete my submission → **submitted 2026-10-25 02:03 EET**.
10. Acknowledgement email from TIFS Editorial Staff; Manuscript ID `T-IFS-29736-2026` assigned via IEEE SPS follow-up email.

## 4. Cross-verification evidence

- `paper_v3/TIFS_CROSS_VERIFICATION_2026-10-25.md` — 60/60 checks PASS (hashes, page/abstract,
  ORCID, result counts, anchors, citations, zip round-trip, Zenodo relation, pytest 73/73, controlled run).
- `paper_v3/TIFS_SOURCE_VERIFICATION_2026-10-25.md` — 49/49 bibliography entries accounted for
  (Crossref/DOI/manual standards); anchor files 22/22 hashes.
- `paper_v3/TIFS_EDITOR_VERIFICATION_2026-10-25.md` — editor-facing summary.
- `paper_v3/FINAL_SUBMISSION_CHECKS_2026-10-24.json` — machine-readable final checks.

## 5. Reusable skill

`skills/ieee-publication-prep/`:

```text
SKILL.md
references/tifs-author-requirements.md
references/portal-answer-matrix.md
references/submission-freeze.md
references/lessons-from-tifs-v3.md
scripts/ieee_preflight.py
evals/evals.json
```

Install/refresh:

```bash
mkdir -p ~/.agents/skills/ieee-publication-prep
cp -a skills/ieee-publication-prep/. ~/.agents/skills/ieee-publication-prep/
```

Use the preflight checker:

```bash
python3 skills/ieee-publication-prep/scripts/ieee_preflight.py \
  --pdf paper_v3/drafts/tifs/ieee/main.pdf \
  --source paper_v3/drafts/tifs/ieee/IEEEtran_TIFS_submission.zip \
  --orcid 0000-0001-6690-2603 --max-pages 13 \
  --json-out /tmp/ieee_preflight.json
```

Expected current result: 9/9 PASS (except the script prints PASS for all checks after the abstract
extraction fix; abstract 242 words from LaTeX source).

## 6. Post-submission control checklist

- [x] Recorded Manuscript ID `T-IFS-29736-2026` (email 2026-10-25 02:16 EET; Date header 24-Oct-2026).
- [x] Cover letter version **verified by owner as correct** (corrected 36.8 KB build; no editorial correction needed).
- [ ] Verify submitted `main.pdf` (334.6 KB) and source zip (442 KB).
- [ ] No concurrent submission elsewhere.
- [ ] Log the first editor decision in `PUBLICATIONS.md` and the frozen record.
- [ ] For revisions, create a new frozen directory; never overwrite the submitted artifacts.

## 7. Known residual risks

- Standard IEEEtran margins vs SPS ≥1-inch wording; portal accepted standard build.
- Prior Zenodo v5 file contains historical ORCID/affiliation (old data); current manuscript is correct.
- Reviewer PDF contains a blank Atypon separator page and a 22-page prior preprint; not a manuscript
  defect, but it increases reviewer reading load.
- Acceptance is not guaranteed; this playbook records process quality, not an editorial outcome.

## 8. Official references

- IEEE TIFS Author Portal: https://iee.atyponrex.com/journal/tifs-ieee
- IEEE author guidelines / SPS Information for Authors (check live)
- IEEE AI-generated content guidance: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
- IEEE AESS summary of AI content rules: https://ieee-aess.org/using-ai-generated-content-ieee-article-and-its-review

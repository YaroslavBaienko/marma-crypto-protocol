---
name: ieee-publication-prep
description: "Prepare, validate, upload and track an IEEE journal manuscript end-to-end. Use when the user mentions IEEE, TIFS, TIP, IEEEtran, EDICS, Author Portal, ScholarOne, submission package, reviewer PDF, ORCID, CRediT, preprints, prior publication or resubmission disclosures, including readiness checks."
---

# IEEE publication preparation

Use this skill when a manuscript is going to an IEEE journal or when an existing IEEE submission is
being audited, revised, or tracked. The goal is not just a readable PDF: the portal answers, author
identity, file bytes, disclosures and post-submission record must all tell the same story.

## Inputs to collect first

- Target journal, article type, current official author guidelines (date/URL).
- Manuscript PDF, LaTeX source, figures, bibliography, cover letter, supplemental material.
- Author identity: legal name, email, affiliation, ORCID, CRediT roles.
- Prior public versions: preprints, conference papers, rejected/withdrawn submissions, code/data deposits.
- Frozen hashes of every file that will be uploaded.

## Ten-gate workflow

### Gate 0 — venue profile

Fetch the journal's current "Information for Authors" and record page limit, abstract limit, template,
margin requirement, EDICS taxonomy, page charges and preprint policy. Do not use an old EDICS number
list when the portal exposes a hierarchical `IF-*` taxonomy.

### Gate 1 — identity and ORCID

Cross-check four places: manuscript footnote, cover letter, portal author profile and ORCID public API.
A portal link is not proof by itself; query `https://pub.orcid.org/v3.0/<id>/record`. If the manuscript
uses an empty/placeholder ORCID while the portal links a populated record, correct every artifact,
rebuild, and re-upload. Never unlink the correct portal ORCID to match a stale manuscript.

### Gate 2 — manuscript build

Build with the official class (e.g. IEEEtran) and check: page limit, abstract word count, two-column
10 pt layout, embedded fonts, no undefined citations/`??`, references resolve, figures/tables fit.
When the society states a 1-inch margin rule but the template uses narrower margins, prepare a second
PDF with compliant margins and decide which one the portal will receive. Record that decision.

### Gate 3 — artifact consistency

- The LaTeX archive must have `main.tex` at its root, plus class, bst, figures and `main.pdf`.
- Rebuild source zip and PDF after every textual change; stale README/source files are common.
- Hash every upload file with SHA-256 and record sizes. Verify the zip test and that the embedded
  `main.pdf` matches the separately uploaded PDF.
- Never upload internal legal/audit/checklist/bundle files to the journal.

### Gate 4 — disclosures

Separate three questions that are often conflated:
1. **Identical preprint / public author copy** (e.g. GitHub release): list it, do not put it in the
   reference list if the journal follows the IEEE two-track preprint rule.
2. **Non-identical related preprints**: these are prior art; cite them and explain the relationship.
3. **Prior publication / prior rejected manuscript**: if any part was published or presented, provide
   the statement/files; if versions were desk-rejected elsewhere, answer the related-resubmission
   question truthfully, list venue IDs, and upload a statement. Do not claim no prior submission.
Also handle code/data (DataPort is optional but do not falsely claim a deposit), COI, funding, patent,
and AI-generated-content disclosure under the current IEEE policy.

### Gate 5 — portal metadata

Title exactly as in the PDF; abstract exactly as in the PDF; author list, affiliation, corresponding
author; CRediT roles (one or more per author); EDICS leaf topics; subject categories. Read back the
Final Review page and compare every value with the frozen files.

### Gate 6 — upload

For a LaTeX manuscript the portal usually requires both:
- Main Document - LaTeX (`.zip` containing `main.tex`, not a generic package);
- Main Document - PDF (compiled manuscript).
Upload cover letter and only the supporting files the portal asks for. Check file sizes: a stale cover
or source zip is visible from its size even when the filename is unchanged.

### Gate 7 — reviewer PDF audit

Build and download the portal Reviewer PDF. Check the page map: portal metadata, possible blank
separator page, main manuscript, disclosure, prior files, statements. Confirm the current ORCID/title
appear in the manuscript and that no superseded file is included. A blank page or a 22-page prior
preprint is not necessarily fatal, but decide deliberately whether to keep it.

### Gate 8 — submit and freeze

After `Complete my submission`, record: submission UUID, date/time, file hashes, portal answers,
reviewer PDF hash/path, and Manuscript ID status. Commit the record to the repository and push.
The manuscript is now locked; do not submit it elsewhere.

### Gate 9 — post-submission

Watch for the Manuscript ID email (often via ScholarOne). Verify the submitted files in My Submissions,
especially any file replaced just before submit. Log the first decision and start revisions in a new
frozen directory rather than editing the submitted artifact.

## TIFS profile (verify against current guidelines before reuse)

- Regular Paper; initial **≤13 double-column pages** including appendices/references; revised ≤16.
- Abstract **150–250 words**; two-column, 10 pt; IEEEtran; margins ≥1 inch.
- Portal EDICS taxonomy: `IF-WAT` watermarking/data hiding (e.g. `IF-WAT-MODL` theoretical models),
  `IF-FOR-AUTH` multimedia content authentication; subject categories Watermarking/Data Hiding and
  Multimedia Forensics.
- Page charges: voluntary **$110/page first 10**; mandatory **$220/page above 10**.
- Hybrid subscription route has no APC; copyright eCF after acceptance; supplemental ≤6 pages.
- Preprints: identical copy listed but not in reference list; related non-identical preprints are prior
  art and must be cited/explained.

## Portal answer matrix

Read `references/portal-answer-matrix.md` before filling the Additional Information page.

## Artifact freeze

Use `references/submission-freeze.md` and `scripts/ieee_preflight.py` for the hash/check record.

## Lessons that caused real defects

Read `references/lessons-from-tifs-v3.md`. The recurring failures are: stale cover letter after an
ORCID edit, stale README/source inside the zip, portal sizes revealing old files, an identical
preprint undisclosed while the manuscript says "no identical preprint", and a prior file carrying old
author metadata.

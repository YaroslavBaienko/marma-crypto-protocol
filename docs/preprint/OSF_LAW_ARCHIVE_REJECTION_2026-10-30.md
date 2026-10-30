# OSF Law Archive rejection — diagnosis and resubmission options (2026-10-30)

**Preprint:** `osf.io/preprints/lawarxiv/a8q5x_v1`
**Title shown in OSF:** “Marma-Crypto Protocol: Deterministic Cryptographic Geometric Watermarking
and Sovereign Document Sealing via Coupled Sri Yantra Phase Spaces (DSTU 4145-2002 / PAdES-B-LTA)”
**Status shown to the author:** Rejected; not publicly available/searchable.
**OSF email:** submitted to Law Archive; not accepted; an admin contributor may edit and resubmit;
the moderator left a comment visible only to contributors.

> The exact moderator comment is **not** visible without an authenticated contributor session.
> The public OSF API currently answers “pending moderation” (a state/UI inconsistency); rely on
> the logged-in banner first. Do not resubmit the same version until the moderator comment has been
> read.

## 1. Most likely cause: out of scope for Law Archive

Law Archive is the **Open Archive for Legal Scholarship** hosted by Yale’s Lillian Goldman Law
Library on OSF. Its moderation policy requires **all** of:

1. **Scholarly content** — engages current/prior legal authorities and scholarship.
2. **Research area supported: law** — paper directly deals with law/legal information, or for
   interdisciplinary work, a legal perspective is integral to the thesis.
3. **Plausibly categorized** — subject taxonomy includes law.
4. **Correctly attributed** — prior public authorship; explicit generative-AI declaration if used.
5. **English.**
6. **Searchable text format.**

Source: [Law Archive — information and moderation policy](https://library.law.yale.edu/research/law-archive),
[provider metadata via OSF API](https://api.osf.io/v2/providers/preprints/lawarchive/).

The submitted manuscript is a **technical cryptography / document-security paper** with a legal
use case. The abstract is about geometric watermarking, QIM, DSTU 4145 and PAdES; it does not
engage legal authorities or make a legal thesis. On the criteria above, the likely failure is
**criterion 1/2 (not law-related scholarship)**, not PDF corruption, licensing or attribution.
That is a scope rejection; resubmitting the same manuscript will likely repeat it.

**Do not assume** the reason from this note alone: the moderator comment may instead mention AI
disclosure, attribution, subject categories or formatting. Read it first.

## 2. How to read the moderator comment (2 minutes)

1. Sign in to OSF with the **admin contributor** account.
2. Open the preprint page / OSF Preprints dashboard.
3. On the rejected banner, click **“Moderator feedback”** (or **“Show moderator feedback”**).
4. Copy the text into a reply to this note (or into the project record).
5. Check whether the banner says **Rejected** or **Pending**; if they disagree, screenshot both and
   contact OSF support (`support@osf.io`) with the preprint GUID.

OSF help: [Resubmit your preprint / View moderator feedback](https://help.osf.io/article/376-preprints-home-page).

## 3. Decision tree

### A. If the reason is “not law / out of scope” (most likely)

**Do not resubmit the same paper to Law Archive.** Choose a technical archive:

| Target | Fit | Notes |
|---|---|---|
| **TechRxiv** (IEEE) | Best for an IEEE/TIFS audience | IEEE’s preprint server; check TIFS/preprint disclosure; no peer review |
| **engrXiv** | Engineering archive (OSF) | Requires work relevant to engineering; AI policy declaration; permanent once posted |
| **arXiv cs.CR** | Strong technical visibility | May need endorsement; check the TIFS/preprint policy and license |
| **OSF Preprints (general)** | Broad, if no domain archive fits | Weaker discoverability for cryptography |

Before posting, check the **IEEE TIFS preprint policy** and update the manuscript’s prior-publication
disclosure in the TIFS submission record. Do not post a version that contradicts the TIFS file;
a preprint DOI is not a journal publication, but it must be disclosed consistently.

### B. If the reason is a fixable metadata issue

Examples: missing AI-use declaration, wrong subject category, incomplete attribution, non-searchable
PDF, missing license. Then:

- fix metadata in **Edit preprint**; use **Edit and Resubmit**;
- upload a new file only through **Create New Version**;
- keep the same OSF GUID and respond to the moderator comment in the resubmission note.

### C. If you want a legal audience (separate paper, not this manuscript)

A Law Archive paper needs a legal thesis and legal authorities. A viable separate article would be:

> **“Visible Cryptographic Seals as Legal Evidence: Authentication, Admissibility and the Limits of
> PDF Signatures under eIDAS and Ukrainian Law”**

It would need: legal research question, doctrine/statutes/case law, evidentiary standards,
expert-evidence rules, eIDAS/DSTU 4145 legal effect, admissibility limits, and the technical protocol
only as the object of study. Do not disguise the TIFS manuscript as law scholarship; that is what
moderation is designed to catch.

## 4. Prepared technical-archive metadata (draft)

**Title:** Marma-Crypto: Deterministic Cryptographic Geometric Watermarking and Sovereign Document
Sealing via Coupled Sri Yantra Phase Spaces (DSTU 4145-2002 / PAdES-B-LTA)

**Abstract (technical archive version):** A deterministic document-sealing protocol that embeds a
266-bit payload (256-bit digest + 10-bit recipient word) into the visible vector geometry of a seal,
with exact fail-closed verification, PAdES/eIDAS complementarity, and a recipient canary for
vector-preserved copies. The paper formalises the layout, proves exactness under quantisation,
reports 1,800+ reproducible PDF samples and print-scan fail-closed tests, and discusses the limits of
fragile vector carriers for screenshot/photo leak attribution.

**Subjects/keywords:** cryptography; information hiding; watermarking; document security; PDF;
PAdES; eIDAS; DSTU 4145-2002; digital forensics; legaltech.

**Disclosures:** IEEE TIFS submission `T-IFS-29736-2026`; prior public preprint (Zenodo/SSRN/Figshare)
already disclosed in the TIFS submission; AI-assistance declaration if applicable; code availability
and license.

## 5. What not to do

- Do not resubmit the same PDF to Law Archive without a legal reframe; a second scope rejection is
  likely and burns moderator time.
- Do not create multiple preprint versions across Law Archive, engrXiv, arXiv and Zenodo with
  inconsistent titles/abstracts; one DOI should be canonical.
- Do not claim “accepted” or “published” in the TIFS record because of a preprint.
- Do not remove the existing OSF record without checking OSF’s deletion/withdrawal policy; a
  rejected preprint is not publicly searchable, but the record may remain in the contributor
  dashboard.

## 6. Next action

Send the moderator comment text (or a screenshot of the feedback popup). Then:

- **out of scope** → prepare TechRxiv/engrXiv/arXiv package and update TIFS disclosure;
- **metadata fix** → edit/resubmit on OSF;
- **legal audience** → draft the separate law article with a real legal thesis.

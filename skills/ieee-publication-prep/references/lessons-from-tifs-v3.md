# Lessons from the TIFS v3 submission

These are concrete failures found during a real submission; check each one in future work.

1. **ORCID mismatch.** The portal linked a populated ORCID while the manuscript/cover used a different
   empty record. Always resolve both IDs through the ORCID public API and make the whole package match
   the correct record before upload. Rebuild PDF/source/cover/release after the fix.
2. **Stale cover after a late edit.** The portal Final Review showed a 30.3 KB cover while the corrected
   file was 37.6 KB. File size is a cheap stale-file detector; download and inspect the submitted files
   after submission.
3. **Stale README inside the source zip.** The zip contained an old build note (wrong citation counts,
   old page count). Rebuild the zip after every edit to README/main.tex/figures.
4. **Identical public author copy vs preprints.** A GitHub release was identical to the submitted PDF;
   the cover letter initially said no posted preprint was identical. That statement must be corrected
   before submission: identical public copies are listed as preprints and excluded from the reference
   list; related non-identical preprints are cited as prior art.
5. **Old metadata in prior files.** A 22-page prior Zenodo PDF included an old ORCID and old employer
   affiliation, while the current manuscript had a new independent-researcher record. Historical files
   may legitimately differ, but disclose the history and decide whether the full prior file is needed
   in the reviewer PDF.
6. **Portal artifacts.** The Reviewer PDF contained a blank separator page and Atypon-added line numbers
   that were not in `main.pdf`. Judge the manuscript by `main.pdf`, and judge the submission by the
   Reviewer PDF separately.
7. **Unbalanced last page.** References ended in the left column only, leaving a blank right column.
   Not fatal, but a final build can balance it or a typesetter will.
8. **Margins.** Standard IEEEtran margins may be narrower than the society's stated ≥1 inch. Keep a
   compliant alternate build and record which PDF was uploaded.
9. **Data answer.** Answer `No` to DataPort only when no DataPort deposit exists; do not equate that
   with "no data/code". Code availability can still be stated in the manuscript.
10. **Submission record.** Immediately after Submit, record UUID, hashes, portal answers, reviewer-PDF
    hash and Manuscript ID status. Once locked, the portal may not let you change files.

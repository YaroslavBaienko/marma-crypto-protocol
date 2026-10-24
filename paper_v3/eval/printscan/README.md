# Print-scan kit — physical capture test

## What to do
1. Print every PDF in `to_print/` at 100% scale (A4, no "fit to page") — the seal is near the
   bottom-left corner of page 1.
2. Scan each printed page at 200-300 dpi, or take a straight, well-lit phone photo.
3. Save each capture in `raw/` with the same base name: `raw/<doc_id>_stamped.jpg` (or `.png`/`.pdf`).
4. Tell the agent when the captures are in place; the processing script converts them to PDFs,
   runs the verifier and records the fail-closed result.

## Expected result
The vector carrier does not survive printing and scanning. The verifier must return **absent**
(fail-closed) on every physical capture. The stamped PDF itself (digital control) verifies as
**valid**. This is the physical counterpart of the simulated flattening experiment.

## Notes
- Black-and-white printing is fine: the carrier is a near-black stroke and the kit thickens it to
  1.2 pt so the seal stays visible; the digital control (stamped PDF) still verifies exactly.
- Do not resize/crop the page; keep the full sheet visible.
- No client documents: the five source PDFs are synthetic corpus documents.
- Raw captures are large; they are not committed to git.

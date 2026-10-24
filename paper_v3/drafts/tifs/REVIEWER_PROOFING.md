# TIFS reviewer-proofing — expected objections and prepared answers

Use this as (a) a pre-submission checklist and (b) a source of exact sentences to insert in the
manuscript so the objection is answered before it is raised.

## 1. "The corpus is synthetic; where is the real-world evidence?"
**Answer:** ten public project PDFs (whitepapers, manuscript PDFs, patent descriptions; no client
data) were stamped and attacked under the same protocol — 100 samples, same exact/fail-closed
behaviour (Table "Public project-document anchors"). A physical print-scan kit is prepared; the expected
result is fail-closed because printing rasters the vector layer.
**Sentence to add:** "The public anchors test documents produced by production PDF writers rather
than a population of enterprise DMS pipelines; the latter is stated as future work."

## 2. "Baselines are not state of the art / are not re-implemented fairly."
**Answer:** the paper does not quote numbers from other papers. STDM-DCT, Fourier-descriptor and
LSB-RDH are re-implemented on the *same* 27-slot carrier at both slot and PDF level; DE-RDH is
reported as capacity-limited (0 pairs). The comparison is framed as a capability frontier, not a
ranking.
**Sentence to add:** "No baseline number is copied from prior work; every comparison is produced by
the same harness on the same carrier."

## 3. "Exactness is deterministic — the 95% CIs are meaningless."
**Answer:** yes; exactness is deterministic by construction. The variance that matters is not seed
variance but generator/pipeline/attack variance; the CI is reported only for completeness and is
explicitly labelled uninformative.
**Sentence to add:** "The reported intervals are not evidence of empirical robustness; the relevant
variation is the generator and the post-sealing pipeline."

## 4. "Physical print-scan is missing."
**Answer:** the paper simulates print-scan (200 dpi, blur, noise, JPEG) and reports the physical
capture as an explicit pending experiment with a prepared kit; the expected outcome is fail-closed,
not payload recovery, because the vector layer does not survive rasterisation.
**Sentence to add:** "Physical capture is expected to fail closed; payload recovery from raster
captures belongs to the optical companion channel, which is out of scope here."

## 5. "What is new relative to fragile watermarking and visible digital seals?"
**Answer:** not a new modulation family. The narrow claim: a *visible seal* carries a 256-bit digest
bit-exactly (signature-to-rendering binding), an incidence invariant detects non-payload edits, and a
disjoint recipient channel provides attribution; the implementation precondition is stated.
**Sentence to add:** "The contribution is the binding and the invariant, not a new QIM variant."

## 6. "Geometry does not matter — the ablation shows generic carriers work."
**Answer:** correct on capacity/distortion; the geometry contributes an invariant, not capacity. The
paper claims only that.
**Sentence to add:** "The incidence configuration adds detection of centre-line edits outside the
payload slots; it does not add capacity."

## 7. "Capacity is per seal, not per document — the headline number is misleading."
**Answer:** capacity is per seal and the visible seal area is reported (≈126×185 pt, 23,227 pt²,
0.0115 bit/pt²); no document-wide capacity claim is made.
**Sentence to add:** "Capacity is per visible seal; scaling to a document is a deployment choice."

## 8. "Security claims are overstated."
**Answer:** the paper claims fragility and fail-closed behaviour, not cryptographic security; it
explicitly refuses "vector commitment" and "traitor tracing" terminology and states the residual
attacks (new document + new seal).
**Sentence to add:** "No cryptographic security is claimed from a watermarking argument."

## 9. "Key management / 1,024 recipients is a toy scale."
**Answer:** stated as a deployment boundary: 10-bit identifier, 1,024 copies per key epoch, key
rotation or a larger identifier space at a known capacity cost; key management is out of scope.
**Sentence to add:** "The recipient channel is an attribution mechanism at a stated scale, not a
collusion-resistant fingerprinting code."

## 10. "Reproducibility?"
**Answer:** corpus builder, harness, seeds and manifest are versioned; measured tables are generated
by the harness; no hand-typed numbers.

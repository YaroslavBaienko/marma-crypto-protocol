#set page(paper: "us-letter", margin: 2.2cm)
#set text(font: "Aptos", size: 10pt, lang: "en")
#set par(justify: true, leading: 0.65em)

#align(right)[Yaroslav V. Baienko \
Attorney-at-Law, Legal Engineer & Applied Cryptography Researcher \
ORCID: 0009-0006-7498-2133]
#v(1em)

Dear Editor-in-Chief,

#v(0.4em)
Please consider the manuscript *Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry* for publication in *IEEE Transactions on Information Forensics and Security* as a regular paper.

#v(0.4em)
*Problem.* A PDF signature verifies the bytes it covers, not the page a human sees; the visible seal is typically not cryptographically bound to the signed content, and published attacks on PDF signatures exploit this gap. The paper treats the problem as fragile watermarking: can the visible mark itself carry a bit-exact digest, so that the mark a person sees is also the mark that is verified?

#v(0.4em)
*Contribution.* The digest is embedded, bit-exactly, into the geometry of a visible seal (nine triangles, 27 scalar degrees of freedom) using keyed dithered QIM over an integer coordinate lattice with an exact IEEE-754 argument; a disjoint carrier degree of freedom carries a per-recipient identifier. No external QR/barcode symbol is added. The paper reports the implementation precondition that matters in practice — the PDF writer must preserve at least nine decimal places and the verifier must parse coordinates as text — and shows that common workflows (five-decimal writers, 32-bit-float drawing APIs) destroy the lattice.

#v(0.4em)
*Evaluation.* A 180-file corpus from three generators (LibreOffice, Typst, Chromium print) in native, flattened and print-scan-simulated variants, plus ten public real-world documents; 1,800 + 100 stamped PDFs with stream-level attacks; carrier ablation (incidence geometry vs generic polyline vs grid); and same-carrier baselines re-implemented at both slot and PDF level. Capacity-limited baselines are reported as such; the paper does not claim cryptographic security from a watermarking argument and explicitly complements, rather than replaces, PAdES/eIDAS signatures.

#v(0.4em)
*Preprints and prior venues.* All posted preprints of this research line are disclosed in the submission: Zenodo concept DOI 10.5281/zenodo.23429017 (latest version 10.5281/zenodo.23560975, v2.1.0-rev1), SSRN DOI 10.2139/ssrn.7631458, and Figshare DOI 10.6084/m9.figshare.34697025. The submitted manuscript is a substantially re-framed and expanded v3; none of these preprints is included in the reference list. A Ukrainian patent application (a 2026 06266) covers the sealing method. The manuscript is not under consideration elsewhere. The evaluation harness, corpus manifest and seeds are available for reproducibility.

#v(0.8em)
Thank you for your consideration.

#v(0.8em)
Sincerely, \
Yaroslav V. Baienko

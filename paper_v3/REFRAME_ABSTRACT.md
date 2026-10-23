# v3 re-framing — title, abstract, contributions

**Target persona:** watermarking / multimedia-forensics reader (not a cryptographer, not a lawyer).
**Rule:** the paper is a *fragile-authentication watermarking* paper; PAdES/DSTU is the deployment
context in one subsection, not the frame.

## Title candidates (pick one)

1. **Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry**
2. **When the Signature Is Valid but the Page Is Not: Bit-Exact Vector-Geometry Authentication for PDF Documents**
3. **Bit-Exact Fragile Watermarking of Visible PDF Seals for Signature-to-Rendering Binding**

Recommended: **1** (sober, venue-legible) for journals; **2** for a conference/industry talk.

## Abstract (draft, ~230 words)

> A PDF signature verifies the bytes it covers, not the page a human sees. The visible layer —
> seals, stamps and logos — is typically not cryptographically bound to the signed content, so a
> document can present a valid signature next to altered or transplanted visual material. Published
> attacks on PDF signatures (CCS 2019; NDSS 2021; IEEE S&P 2021) exploit exactly this gap.
>
> We study a fragile-authentication watermarking approach that closes the gap at the rendering
> level: the digest of the signed document is embedded, bit-exactly, into the geometry of the
> visible seal itself, so the mark a person sees is also the mark that is verified. The carrier is a
> planar incidence configuration of triangles; the payload uses keyed dithered quantization index
> modulation over an integer coordinate lattice with an exact IEEE-754 rounding analysis, and a
> disjoint carrier degree of freedom carries a per-recipient identifier for leak attribution. No
> external QR/barcode symbol is added. Verification fails on a single-vertex change and is
> reproducible across Python/Node/browser renderers.
>
> We evaluate on a corpus of documents produced by LibreOffice, Typst and browser print pipelines,
> plus flattened and print-scan simulated variants; baselines (scalar QIM, spread-transform dither
> modulation, difference-expansion RDH, prediction-error expansion, Fourier-descriptor
> watermarking) are re-implemented **on the same carrier and distortion budget**, and an ablation
> isolates the contribution of the geometric carrier from a generic polygon and a grid.
>
> Limitations: the vector layer does not survive rasterisation (a separate optical channel is out of
> scope here); the method complements, and does not replace, PAdES/eIDAS signatures.

*(Numbers omitted until the evaluation is run — no placeholder claims.)*

## Contributions (ordered as a watermarking paper)

1. **Bit-exact fragile payload in vector geometry.** A 256-bit document digest is encoded into
   coordinate lattices with an exact rounding bound; BER = 0 by construction on the digital path,
   which makes cryptographic digest recovery possible without error-correcting codes.
2. **No auxiliary symbol.** The visible seal is the carrier: removing or transplanting the seal
   breaks verification, unlike QR-based visible digital seals that can be detached.
3. **Disjoint recipient channel.** A separate carrier degree of freedom carries a per-recipient
   identifier; keyed dithering makes the allocation statistically indistinguishable in the ideal
   model (formal statement to be tightened for v3).
4. **Empirical protocol.** Same-carrier re-implementation of five baselines, real-generator corpus,
   flattening and print-scan simulation, and a carrier ablation — the evidence the v2.x drafts
   lacked.

## What moves out (companion paper / appendix)

* `Marma-Optical` screen-photo ECC, universal emblems (Tryzub/CAD/corporate shield), REST API,
  O(1) batch sealing → companion paper targeting a multimedia/forensics venue or IH&MMSec/WIFS.
* Cryptographic protocol detail (GOST/Kupyna combiner, DSTU 4145 signing, RFC 6979) → one
  deployment subsection + supplementary material.
* Geometry theorems (algebraic irrationality) → a short appendix; the main text keeps only what the
  carrier needs. Theorem 1 is not a contribution of the watermarking paper unless the ablation shows
  the geometry matters.

## Vocabulary rules (enforced in v3)

* Write "fragile authentication", "tamper-evident", "digest binding"; **not** "vector commitment"
  (unless a formal definition/opening is given), **not** "traitor tracing" (unless collusion bounds
  are proven — otherwise "per-recipient leak attribution").
* Write "keyed dithered QIM"; do not claim cryptographic security from a watermarking argument.
* Every quantitative claim must point to a table/figure produced by `paper_v3/eval/`.

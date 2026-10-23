#set page(paper: "a4", margin: (x: 2.2cm, y: 2.3cm))
#set text(font: "Aptos", size: 9.6pt, lang: "en")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: it => { v(0.35em); it; v(0.2em) }

#align(center)[
  #text(size: 16pt, weight: "bold")[Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry]
  #v(0.4em)
  #text(size: 10pt)[Draft 1 — evaluation harness results (v0). Target length 14–16 pp; this draft is the technical core.]
  #v(0.3em)
  #text(size: 9pt)[Yaroslav V. Baienko]
]

#v(0.5em)
#align(center)[#text(size: 9pt, style: "italic")[Abstract]]
#block(width: 100%)[
A PDF signature verifies the bytes it covers, not the page a human sees. The visible layer — seals, stamps and logos — is typically not cryptographically bound to the signed content, so a document can present a valid signature next to altered or transplanted visual material. Published attacks on PDF signatures (CCS 2019; NDSS 2021; IEEE S&P 2021) exploit exactly this gap.

We study a fragile-authentication watermarking approach that closes the gap at the rendering level: the digest of the signed document is embedded, bit-exactly, into the geometry of the visible seal itself, so the mark a person sees is also the mark that is verified. The carrier is a planar incidence configuration of triangles; the payload uses keyed dithered quantization index modulation (QIM) over an integer coordinate lattice with an exact IEEE-754 rounding analysis, and a disjoint carrier degree of freedom carries a per-recipient identifier for leak attribution. No external QR or barcode symbol is added.

We evaluate on a corpus of 60 documents produced by LibreOffice, Typst and Chromium print pipelines, each in native, flattened and print-scan-simulated variants. On 1,800 stamped PDFs the 266-bit payload is recovered exactly, survives 8-decimal re-serialisation, fails closed at 7 decimals, and any edited payload coordinate is detected; flattening destroys the vector carrier and therefore fails closed. Baselines re-implemented on the same carrier expose a capacity–distortion trade-off rather than a single “winner”.

Limitations: the vector layer does not survive rasterisation; the baselines are evaluated at slot level in this draft; and the method complements, rather than replaces, PAdES/eIDAS signatures.
]

= Introduction
A signed PDF can be *valid* and still mislead. The signature covers a byte range; the visual seal is an image or a vector drawing that the signature does not necessarily cover, and incremental updates or flattened copies are outside the signed bytes. The research literature on PDF signature attacks documents both hidden content (@mainka2021) and signature spoofing (@mladenov2019), and industry workflows add a third problem: a document room can hand every recipient a *visually identical* copy, so a leak cannot be attributed.

This paper asks a watermarking question rather than a cryptographic one: can a fragile mark be carried by the visible layer itself, so that (i) the mark is exactly recoverable from the rendered page, (ii) any modification of the mark is detected, and (iii) the mark identifies the recipient copy? The answer explored here is a bit-exact quantization-index-modulation payload embedded in the coordinates of a vector seal.

The contributions of this draft are: (1) a bit-exact fragile payload in vector geometry, with an exact rounding bound; (2) a carrier that uses the seal itself, so removing or transplanting the seal breaks verification; (3) a disjoint recipient channel; and (4) an evaluation protocol with same-carrier baselines, three document generators, flattened and print-scan variants, and a carrier ablation.

= Related Work
*Quantization-based data hiding.* QIM and dither modulation were introduced by @chen2001; structured codebooks and the scalar Costa scheme followed in @eggers2003, and rational dither modulation addressed value-metric scaling in @perez2004. Spread-spectrum watermarking (@cox1997) and early data-hiding constructions (@bender1996) remain the reference points for robustness-oriented schemes. Our method is deliberately *fragile*: it borrows the QIM lattice but requires exact, not robust, recovery.

*Reversible data hiding.* Difference expansion (@tian2003), histogram shifting (@ni2006) and prediction-error expansion (@thodi2007) define the RDH family. On a 27-slot carrier these schemes are capacity-limited, which we report rather than hide; 2D vector-map RDH (@wang2014, @peng2019) operates on much larger vertex sets.

*Vector graphics watermarking.* Fourier-descriptor watermarking of 2D vector graphics (@doncel2007), blind vector-graphics schemes (@li2003, @hou2014), polar-coordinate vector-data watermarking (@mouhamed2012) and mesh-spectral maps (@ohbuchi2003) are the closest carrier-level relatives. PDF watermarking itself has been studied in @hatoum2018, and print-scan resilience in @he2005.

*PDF signature security.* Shadow attacks (@mainka2021), signature spoofing (@mladenov2019), certification attacks (@rohlmann2021) and practical decryption exfiltration (@muller2019) establish the threat model. Standards (@iso32000, @etsipades, @eidas) define what a compliant signature does and does not cover.

*Commitments and fingerprinting.* Vector commitments (@catalano2013, @libert2016) and traitor tracing (@boneh1999, @tardos2008) are related but not claimed here: the construction is a watermark, not a commitment scheme, and the recipient channel is attribution, not collusion-resistant tracing. We use the terminology accordingly.

= Threat Model and Requirements
The adversary can (a) edit the PDF content stream, (b) re-serialise coordinates at reduced precision, (c) flatten the page to a raster image, (d) transplant a visual seal from another document, and (e) redistribute a copy. The verifier knows the canonical seal geometry and the document digest. Requirements: *exactness* (the 256-bit digest is recovered bit-for-bit), *fragility* (any edit is detected), *fail-closed* behaviour (when the vector layer is gone, the verifier refuses rather than accepts), and *attribution* (a recipient identifier is carried independently of the digest).

= Method
== Carrier
The seal is drawn as nine triangles. Each triangle contributes three degrees of freedom — base line, apex, half-width — for 27 scalar slots. Because the triangles share a construction centre, the bilateral relation $l x + r x = 2 c x$ and the common centre are geometric invariants, checked independently of the payload.

== Bit-exact payload
A 256-bit digest is split into 26 words of 10 bits; the 27th word carries a 10-bit recipient identifier. A 10-bit word $w$ maps to the coordinate shift $delta(w) = (18 w - 9207) times 10^(-9)$ pt, i.e. a multiple of $18$ npt $= 1.8 times 10^(-8)$ pt. For coordinates of the order of $10^2$ pt the IEEE-754 double spacing is below $1.5 times 10^(-14)$ pt, so the lattice is exactly representable; re-serialising at 8 decimal places leaves a rounding error below half a step.

== Keyed dither and recipient channel
A key derives a permutation and a word-level dither; the digest words are dithered and permuted before embedding, and the recipient word is placed in the remaining slot. The dither does not change the lattice spacing, so exactness is preserved; it changes which physical slot carries which word, so an unkeyed reader cannot align the payload with the geometry.

== PDF implementation note
The carrier must be written with at least nine decimal places. Common PDF writers emit five decimals, which destroys a $1.8 times 10^(-8)$ pt lattice; the reference implementation therefore injects the path operators into the content stream directly rather than using a drawing API. The verifier parses the numbers from the stream as text and converts them to double precision, because a drawing API that stores coordinates as 32-bit floats loses the lattice as well.

= Evaluation
== Corpus
Sixty synthetic documents are generated by three independent pipelines: LibreOffice (DOCX to PDF), Typst, and Chromium print-to-PDF. Each document exists in three variants: *native*, *flattened* (300 dpi raster re-wrapped as an image-only PDF) and *print-scan simulated* (200 dpi, Gaussian blur, sensor noise, JPEG q=70). The corpus contains 180 PDFs (51.1 MB) with a SHA-256 manifest.

== Protocol
For each document and seed, the payload is H(doc_sha ‖ seed); the 266-bit payload is embedded with keyed QIM, and the stamped PDF is attacked in the content stream (8/7-decimal truncation, payload-coordinate edit, centre-line edit) or flattened. The carrier is extracted by parsing the stream. The experiment runs 60 documents × 30 seeds (1,800 samples), plus 360 samples on flattened/print-scan inputs, plus an ablation over three carriers and keyed/unkeyed embedding.

== Results
#figure(image("../figures/fig_capacity_distortion.svg", width: 78%), caption: [Capacity vs geometric distortion on the same 27-slot carrier. The proposed payload carries 266 bits at RMSE $5.3 times 10^(-6)$ pt; the capacity-limited baselines are marked at their maximum capacity.])
<fig-cap>

#table(columns: (auto, auto, auto, auto), align: center)[
  [Metric], [Result], [95% CI], [Samples],
  [Exact digest recovery], [100%], [0.00], [1800/1800],
  [Survives 8-decimal truncation], [100%], [0.00], [1800/1800],
  [Detected at 7-decimal truncation], [100%], [0.00], [1800/1800],
  [Edited payload coordinate detected], [100%], [0.00], [1800/1800],
  [Flattening removes the carrier], [100%], [0.00], [1800/1800],
]
#block[#text(size: 8pt, style: "italic")[PDF-level results on 60 native documents × 30 seeds. Mean geometric RMSE $5.31 times 10^(-6)$ pt (PSNR_geom = 155.1 dB).]]

#table(columns: (auto, auto, auto, auto, auto), align: center)[
  [Carrier], [Keyed], [Exact], [Trunc-8], [Centre edit detected],
  [Sri Yantra], [yes], [100%], [100%], [100%],
  [Sri Yantra], [no], [100%], [100%], [100%],
  [Generic polyline], [yes], [100%], [100%], [0%],
  [Generic polyline], [no], [100%], [100%], [0%],
  [Grid], [yes], [100%], [100%], [0%],
  [Grid], [no], [100%], [100%], [0%],
]
#block[#text(size: 8pt, style: "italic")[Carrier ablation: all carriers carry the same 27 slots, so exactness is equal, but only the incidence configuration has a geometric invariant that detects a centre-line edit.]]

#table(columns: (auto, auto, auto, auto), align: center)[
  [Method], [Capacity], [RMSE (pt)], [Exact],
  [Proposed (keyed QIM)], [266], [$5.31 times 10^(-6)$], [yes],
  [STDM-DCT], [140], [$6.00 times 10^(-5)$], [yes],
  [Fourier descriptors], [13], [$7.36 times 10^(-5)$], [yes],
  [LSB-RDH], [27], [$7.81 times 10^(-10)$], [n/a],
  [DE-RDH], [0], [$2.91 times 10^(-10)$], [n/a],
]
#block[#text(size: 8pt, style: "italic")[Same-carrier baselines (30 seeds, slot level). Capacity-limited schemes are not a “weak baseline”: they simply cannot carry a 266-bit digest on 27 slots. The trade-off is the point of #link(<fig-cap>)[Figure 1].]]

== Discussion
Three observations follow. First, exactness is not a marginal improvement: it is the property that allows a cryptographic digest, rather than an error-tolerant watermark, to be bound to the visible layer. Second, the geometry is not a capacity trick — all carriers carry the same payload at the same distortion — but the incidence configuration provides an independent invariant that detects edits outside the payload slots. Third, the protocol has an implementation precondition: the PDF writer must preserve at least nine decimal places, and a verifier must parse numbers as text; otherwise the lattice is destroyed before any attacker acts.

= Security Discussion
The construction is fragile by design: it authenticates the rendering layer, not the cryptographic signature. It does not prevent an attacker from producing a *new* document with a *new* valid seal; it makes a transplanted or edited seal detectable relative to a known document digest. The recipient channel provides attribution for a leaked copy; it is not a collusion-resistant fingerprinting code, and we do not claim traitor-tracing security. The keyed dither prevents an unkeyed reader from aligning the payload; a formal steganographic-security claim is left to future work, and the draft deliberately avoids the term “zero mutual information”.

= Limitations and Conclusion
The evaluation is a first harness result. The baselines are re-implemented at slot level and must be lifted to the PDF level before submission; the print-scan variant is a simulation, not a physical scanner; and the corpus is synthetic. The capacity numbers are per seal, not per document area, and must be reported with the visible seal area in the camera-ready version. Within these limits the result is consistent and reproducible: 1,800 PDF-level samples recover the 266-bit payload exactly, 8-decimal re-serialisation is safe, 7-decimal re-serialisation and any payload edit are detected, and flattening fails closed. The next revision expands the related work, lifts the baselines to the PDF level, adds a physical print-scan set, and reports the full ablation over document generators.

#bibliography("../references.bib", style: "ieee")

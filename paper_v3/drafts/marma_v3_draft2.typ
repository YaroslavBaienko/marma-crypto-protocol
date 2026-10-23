#set page(paper: "a4", margin: (x: 2.2cm, y: 2.3cm))
#set text(font: "Aptos", size: 9.6pt, lang: "en")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: it => { v(0.35em); it; v(0.2em) }

#align(center)[
  #text(size: 15.5pt, weight: "bold")[Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry]
  #v(0.4em)
  #text(size: 9.5pt)[Draft 2 — technical core for the Digital Signal Processing transfer (target 12–16 pp)]
  #v(0.3em)
  #text(size: 9pt)[Yaroslav V. Baienko]
]

#v(0.4em)
#align(center)[#text(size: 9pt, style: "italic")[Abstract]]
#block(width: 100%)[
A PDF signature verifies the bytes it covers, not the page a human sees. The visible layer — seals, stamps and logos — is typically not cryptographically bound to the signed content, so a document can present a valid signature next to altered or transplanted visual material; published attacks on PDF signatures exploit exactly this gap. We study a fragile-authentication watermarking approach that closes it at the rendering level: the digest of the signed document is embedded, bit-exactly, into the geometry of the visible seal itself, so the mark a person sees is also the mark that is verified. The carrier is a planar incidence configuration of nine triangles (27 scalar degrees of freedom); the payload uses keyed dithered quantization index modulation over an integer coordinate lattice with an exact IEEE-754 rounding argument, and a disjoint carrier degree of freedom carries a per-recipient identifier for leak attribution. No external QR or barcode symbol is added.

We evaluate on a corpus of 60 documents produced by LibreOffice, Typst and Chromium print pipelines, each in native, flattened and print-scan-simulated variants (180 PDFs). On 1,800 stamped PDFs the 266-bit payload is recovered exactly, survives 8-decimal re-serialisation, fails closed at 7 decimals, and any edited payload coordinate is detected; flattening destroys the vector carrier and therefore fails closed. Baselines re-implemented on the same carrier expose a capacity–distortion trade-off rather than a single winner. Two implementation facts are stated explicitly: the PDF writer must preserve at least nine decimal places, and the verifier must parse coordinates as text — drawing APIs that store 32-bit floats destroy a $1.8 times 10^(-8)$ pt lattice. The method complements, and does not replace, PAdES/eIDAS signatures; the optical/screen-photo channel and the API are reported separately.
]

= Introduction
A signed PDF can be *valid* and still mislead. The signature covers a byte range; the visual seal is an image or a vector drawing that the signature does not necessarily cover, and incremental updates or flattened copies live outside the signed bytes. The literature on PDF signature attacks documents hidden content (@mainka2021) and signature spoofing (@mladenov2019), and document workflows add a third problem: a data room can hand every recipient a visually identical copy, so a leak cannot be attributed.

This paper asks a watermarking question rather than a cryptographic one: can a fragile mark be carried by the visible layer itself, so that (i) the mark is exactly recoverable from the rendered page, (ii) any modification of the mark is detected, and (iii) the mark identifies the recipient copy? The answer explored here is a bit-exact quantization-index-modulation payload embedded in the coordinates of a vector seal. The word *fragile* is deliberate: the goal is not robustness to editing but detection of it.

The contributions of this draft are: (1) a bit-exact fragile payload in vector geometry with an exact rounding bound; (2) a carrier that uses the seal itself, so removing or transplanting the seal breaks verification; (3) a disjoint recipient channel; and (4) an evaluation protocol with same-carrier baselines, three document generators, flattened and print-scan variants, and a carrier ablation.

= Related Work
== Fragile versus robust watermarking
Robust watermarking aims to survive processing; fragile watermarking aims to detect it. Our work belongs to the second class and is therefore not comparable to robust schemes on BER under compression — the meaningful axes are exact recovery, distortion and detection. The QIM family (@chen2001; @eggers2003; @perez2004) supplies the lattice; spread-spectrum schemes (@cox1997) and early data-hiding constructions (@bender1996) supply the historical contrast. Watermarking security analysis (@cayre2005) and QIM steganalysis (@yang2018) frame what a keyed dither can and cannot promise.

== Reversible data hiding
Difference expansion (@tian2003), histogram shifting (@ni2006) and prediction-error expansion (@thodi2007) define the RDH family. On a 27-slot carrier these schemes are capacity-limited, which we report rather than hide; 2D vector-map RDH (@wang2014, @peng2019) operates on much larger vertex sets, where capacity is not the binding constraint.

== Vector graphics and PDF watermarking
Fourier-descriptor watermarking of 2D vector graphics (@doncel2007), blind vector-graphics schemes (@li2003, @hou2014), polar-coordinate vector-data watermarking (@mouhamed2012) and mesh-spectral maps (@ohbuchi2003) are the closest carrier-level relatives. PDF watermarking itself has been studied in @hatoum2018, and print-scan resilience in @he2005. Our carrier is unusual in that the mark is a *visible seal*, not a hidden embedding in an existing drawing; this is what makes the transplant attack meaningful.

== PDF signature security and standards
Shadow attacks (@mainka2021), signature spoofing (@mladenov2019), certification attacks (@rohlmann2021) and practical decryption exfiltration (@muller2019) establish the threat model. Standards (@iso32000, @etsipades, @eidas) define what a compliant signature does and does not cover. Our method does not change the signature; it makes the visible layer that the signature leaves uncovered tamper-evident.

== Commitments, fingerprinting, terminology
Vector commitments (@catalano2013, @libert2016) and traitor tracing (@boneh1999, @tardos2008) are related but not claimed here: the construction is a watermark, not a commitment scheme, and the recipient channel is attribution, not collusion-resistant tracing. The paper deliberately avoids “vector commitment” and “traitor tracing” as descriptions of its own mechanism.

= Threat Model and Requirements
The adversary can (a) edit the PDF content stream, (b) re-serialise coordinates at reduced precision, (c) flatten the page to a raster image, (d) transplant a visual seal from another document, and (e) redistribute a copy. The verifier knows the canonical seal geometry and the document digest. We state four requirements:

+ *Exactness.* The 256-bit digest is recovered bit for bit; a single wrong bit is a failure.
+ *Fragility.* Any edit of a payload coordinate changes the recovered digest.
+ *Fail-closed.* When the vector layer is absent (flattening), the verifier refuses rather than accepts.
+ *Attribution.* A recipient identifier is carried independently of the digest.

The threat model is deliberately weaker than a cryptographic one: we do not claim that an adversary cannot produce a new document with a new seal, only that an edited or transplanted seal is detectable relative to a known document digest.

= Method
== Carrier and degrees of freedom
The seal is drawn as nine triangles. Each triangle contributes three degrees of freedom — base line, apex, half-width — for 27 scalar slots. Because the triangles share a construction centre, the bilateral relation $l x + r x = 2 c x$ and the common centre are geometric invariants, checked independently of the payload. A generic 27-vertex polyline and a 9×3 grid are used as ablations: they carry the same 27 slots at the same distortion, but have no such invariant.

== Bit-exact word mapping
A 256-bit digest is split into 26 words of 10 bits; the 27th word carries a 10-bit recipient identifier. A 10-bit word $w$ maps to the coordinate shift
$ delta(w) = (18 w - 9207) times 10^(-9) "pt", $
i.e. a multiple of $18$ npt $= 1.8 times 10^(-8)$ pt, with $w in [0, 1023]$. The smallest step is therefore $1.8 times 10^(-8)$ pt.

== Exactness argument
At coordinates of the order of $3 times 10^2$ pt the IEEE-754 double spacing is $2^(-52) times 2^9 approx 1.1 times 10^(-13)$ pt, more than four orders of magnitude below the step, so every lattice point is exactly representable and a recovered word has no rounding ambiguity. Re-serialising a coordinate with eight decimal places rounds it to the nearest $10^(-8)$ pt, an error of at most $5 times 10^(-9)$ pt, below half a step ($9 times 10^(-9)$ pt); seven decimal places (error up to $5 times 10^(-8)$ pt) exceeds half a step and destroys the word. This bound is the reason the evaluation attacks truncation at 8 and 7 decimals rather than at arbitrary precision.

== Keyed dither and recipient channel
A key derives a permutation $pi_K$ of the 27 slots and a word-level dither $d_K$. The digest words are dithered and permuted before embedding, and the recipient word is placed in the remaining slot. The dither does not change the lattice spacing, so exactness is preserved; it changes which physical slot carries which word, so an unkeyed reader cannot align the payload with the geometry. The recipient channel is written in the same way: a 10-bit identifier is mapped to a shift and placed in the 27th slot.

== Verification algorithm
#block(fill: luma(245), inset: 8pt, radius: 4pt)[
*Input:* PDF page, canonical geometry, document digest, key.
+ Parse the content stream as text and locate the carrier path (unique stroke colour/width).
+ Convert the coordinate strings to double precision; reconstruct the 27 slots from the path.
+ Undo the permutation and dither with the key; recover the 27 words.
+ Recompute the digest of the signed document and compare it with the recovered 256-bit digest.
+ Check the geometric invariants (bilateral symmetry and common centre) for the incidence configuration.
+ If the carrier is absent, return *absent* (fail-closed), not *valid*.
]

== PDF implementation precondition
The carrier must be written with at least nine decimal places. Common PDF writers emit five decimals, which destroys the $1.8 times 10^(-8)$ pt lattice; the reference implementation therefore injects path operators into the content stream directly rather than using a drawing API. The verifier must parse the numbers as text, because drawing APIs that store coordinates as 32-bit floats lose the lattice as well (a drawing API returns coordinates quantised at about $10^(-5)$ pt, i.e. three orders of magnitude coarser than the step).

= Evaluation
== Corpus
Sixty synthetic documents are generated by three independent pipelines: LibreOffice (DOCX to PDF), Typst, and Chromium print-to-PDF. Each document exists in three variants: *native*, *flattened* (300 dpi raster re-wrapped as an image-only PDF) and *print-scan simulated* (200 dpi, Gaussian blur, sensor noise, JPEG q=70). The corpus contains 180 PDFs (51.1 MB) with a SHA-256 manifest.

== Protocol
For each document and seed, the payload is H(doc_sha ‖ seed); the 266-bit payload is embedded with keyed QIM, and the stamped PDF is attacked in the content stream (8/7-decimal truncation, payload-coordinate edit, centre-line edit) or flattened. The carrier is extracted by parsing the stream. The experiment runs 60 documents × 30 seeds (1,800 samples), plus 360 samples on flattened/print-scan inputs, plus an ablation over three carriers and keyed/unkeyed embedding.

== Results
#figure(image("../figures/fig_capacity_distortion.svg", width: 76%), caption: [Capacity vs geometric distortion on the same 27-slot carrier. The proposed payload carries 266 bits at RMSE $5.3 times 10^(-6)$ pt; the capacity-limited baselines are marked at their maximum capacity.])
<fig-cap>

#table(columns: (auto, auto, auto, auto), align: center)[
  [Metric], [Result], [95% CI], [Samples],
  [Exact digest recovery], [100%], [0.00], [1800/1800],
  [Survives 8-decimal truncation], [100%], [0.00], [1800/1800],
  [Detected at 7-decimal truncation], [100%], [0.00], [1800/1800],
  [Edited payload coordinate detected], [100%], [0.00], [1800/1800],
  [Flattening removes the carrier], [100%], [0.00], [1800/1800],
]
#block[#text(size: 8pt, style: "italic")[PDF-level results on 60 native documents × 30 seeds. Mean geometric RMSE $5.31 times 10^(-6)$ pt (PSNR_geom = 155.1 dB). The 95% CI is zero because exactness is deterministic by construction; the meaningful variation comes from the document generator and from physical attacks, which are reported as future work.]]

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
#block[#text(size: 8pt, style: "italic")[Same-carrier baselines (30 seeds, slot level). Capacity-limited schemes are not a “weak baseline”: they cannot carry a 266-bit digest on 27 slots. The trade-off is the point of Figure 1.]]

== Discussion
Three observations follow. First, exactness is not a marginal improvement: it is the property that allows a cryptographic digest, rather than an error-tolerant watermark, to be bound to the visible layer. Second, the geometry is not a capacity trick — all carriers carry the same payload at the same distortion — but the incidence configuration provides an independent invariant that detects edits outside the payload slots. Third, the protocol has an implementation precondition: the PDF writer must preserve at least nine decimal places, and a verifier must parse numbers as text; otherwise the lattice is destroyed before any attacker acts.

= Attack Matrix and Security Discussion
#table(columns: (auto, auto, auto), align: center)[
  [Attack], [Expected outcome], [Measured],
  [Payload-coordinate edit], [digest changes → detected], [100%],
  [Centre-line edit (non-payload)], [geometry invariant fails], [100% (incidence only)],
  [8-decimal re-serialisation], [digest unchanged], [100% exact],
  [7-decimal re-serialisation], [digest changes → detected], [100%],
  [Flattening], [carrier absent → fail-closed], [100% absent],
  [Seal transplant], [digest mismatch], [by construction],
]
#block[#text(size: 8pt, style: "italic")[The construction authenticates the rendering layer, not the cryptographic signature. It does not prevent an attacker from producing a new document with a new valid seal; it makes a transplanted or edited seal detectable relative to a known document digest. The recipient channel provides attribution for a leaked copy; it is not a collusion-resistant fingerprinting code, and traitor-tracing security is not claimed.]]

= Limitations and Conclusion
The evaluation is a first harness result. The baselines are re-implemented at slot level and must be lifted to the PDF level before submission; the print-scan variant is a simulation, not a physical scanner; the corpus is synthetic; and exactness is deterministic, so the reported confidence intervals are not informative about real-world variability. Capacity numbers are per seal, not per document area, and must be reported with the visible seal area in the final version. Within these limits the result is consistent and reproducible: 1,800 PDF-level samples recover the 266-bit payload exactly, 8-decimal re-serialisation is safe, 7-decimal re-serialisation and any payload edit are detected, and flattening fails closed. The next revision adds real-world PDFs and a physical print-scan set, lifts the baselines to the PDF level, and reports the full ablation over document generators.

#bibliography("../references.bib", style: "ieee")

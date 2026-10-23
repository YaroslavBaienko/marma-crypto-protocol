#set page(paper: "us-letter", margin: (x: 1.55cm, y: 1.8cm), columns: 2)
#set text(font: "Aptos", size: 8.8pt, lang: "en")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: it => { v(0.35em); it; v(0.2em) }

#align(center)[
  #text(size: 14pt, weight: "bold")[Fragile Authentication of PDF Signatures via Bit-Exact Quantization Index Modulation on Vector Geometry]
  #v(0.4em)
  #text(size: 8.5pt)[Manuscript submitted to IEEE Transactions on Information Forensics and Security — review draft (IEEE two-column layout approximation)]
  #v(0.3em)
  #text(size: 9pt)[Yaroslav V. Baienko]
  #v(0.2em)
  #text(size: 8pt)[*Index Terms* — fragile watermarking; quantization index modulation; vector graphics; PDF signatures; document authentication]
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

The contributions of this draft are: (1) a bit-exact fragile payload in vector geometry with an exact rounding bound; (2) a carrier that uses the seal itself, so removing or transplanting the seal breaks verification; (3) a disjoint recipient channel; and (4) an evaluation protocol with same-carrier baselines, three document generators, flattened and print-scan variants, and a carrier ablation. Section 2 positions the work against the watermarking literature, Section 3 states the threat model, Section 4 describes the carrier and the bit-exact embedding, Section 5 reports the PDF-level evaluation, Section 6 gives the attack matrix and the limits of the security argument, and Section 7 discusses threats to validity and reproducibility.

= Related Work
#table(columns: (auto, auto, auto, auto), align: left)[
  [Family], [Purpose], [Carrier], [What it optimises],
  [Spread spectrum (@cox1997)], [robustness], [pixels / coefficients], [survival under attacks],
  [QIM and dither modulation (@chen2001; @eggers2003; @perez2004)], [rate–distortion], [scalar samples], [capacity at a distortion budget],
  [RDH (@tian2003; @ni2006; @thodi2007; @wang2014; @peng2019)], [reversibility], [pixels / vertices], [exact cover recovery],
  [Vector-graphics watermarking (@doncel2007; @li2003; @hou2014; @mouhamed2012)], [robustness], [2D geometry], [survival under rescaling],
  [PDF watermarking (@hatoum2018)], [document marking], [text/objects], [blind detection],
  [This work], [fragility], [visible seal geometry], [bit-exact digest recovery],
]
#block[#text(size: 8pt, style: "italic")[Positioning: the paper borrows the QIM lattice but targets fragility, and uses the visible seal rather than an existing drawing as the carrier.]]

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


#block(fill: luma(247), inset: 8pt, radius: 4pt)[
*Definition 1 (exactness).* For every document $d$, `Verify(Stamp(d, k), d, k) = valid`, and the recovered 256-bit payload equals the digest of $d$ bit for bit.

*Definition 2 (fragility).* If any coordinate of the carrier path is modified, `Verify` returns `modified` — either because the recovered digest differs from the document digest, or because a geometric invariant fails.

*Definition 3 (fail-closed).* If the carrier path is absent (e.g. the page was rasterised), `Verify` returns `absent`. It never returns `valid` on a page whose carrier cannot be parsed.

*Definition 4 (attribution).* With the key, `Verify` returns the 10-bit recipient identifier; with a different key, the recovered identifier is not a valid attribution (the expected behaviour is a random-looking word, not the true identifier).
]

The threat model is deliberately weaker than a cryptographic one: we do not claim that an adversary cannot produce a new document with a new seal, only that an edited or transplanted seal is detectable relative to a known document digest.

= Method
== Carrier and degrees of freedom
The seal is drawn as nine triangles. Each triangle contributes three degrees of freedom — base line, apex, half-width — for 27 scalar slots. Because the triangles share a construction centre, the bilateral relation $l x + r x = 2 c x$ and the common centre are geometric invariants, checked independently of the payload. A generic 27-vertex polyline and a 9×3 grid are used as ablations: they carry the same 27 slots at the same distortion, but have no such invariant.

#figure(image("../../figures/fig_carriers.svg", width: 100%), caption: [The three carriers used in the ablation. All three carry the same 27 slots at the same distortion; only the incidence configuration (left) has the bilateral and common-centre invariants.])


== Bit-exact word mapping
A 256-bit digest is split into 26 words of 10 bits; the 27th word carries a 10-bit recipient identifier. A 10-bit word $w$ maps to the coordinate shift
$ delta(w) = (18 w - 9207) times 10^(-9) "pt", $
i.e. a multiple of $18$ npt $= 1.8 times 10^(-8)$ pt, with $w in [0, 1023]$. The smallest step is therefore $1.8 times 10^(-8)$ pt.

== Exactness argument
At coordinates of the order of $3 times 10^2$ pt the IEEE-754 double spacing is $2^(-52) times 2^9 approx 1.1 times 10^(-13)$ pt, more than four orders of magnitude below the step, so every lattice point is exactly representable and a recovered word has no rounding ambiguity. Re-serialising a coordinate with eight decimal places rounds it to the nearest $10^(-8)$ pt, an error of at most $5 times 10^(-9)$ pt, below half a step ($9 times 10^(-9)$ pt); seven decimal places (error up to $5 times 10^(-8)$ pt) exceeds half a step and destroys the word. This bound is the reason the evaluation attacks truncation at 8 and 7 decimals rather than at arbitrary precision.

#block[#text(size: 8pt, style: "italic")[*Lemma 1 (the word map is a bijection).* For $w in [0, 1023]$, $delta(w) = (18w - 9207) times 10^(-9)$ takes 1,024 distinct values in steps of $18 times 10^(-9)$ pt; decoding by $w' = round((round(delta dot 10^9) + 9207) / 18)$ returns $w$ for every value. *Proof sketch:* the map is affine and injective on the integers, and the spacing between neighbouring values is 18 integer nanometres, so the rounding in the decoder cannot cross a boundary.]]

#block[#text(size: 8pt, style: "italic")[*Lemma 2 (eight decimals are sufficient).* Re-serialising a coordinate to $d = 8$ decimal places produces error at most $0.5 times 10^(-8)$ pt; since half a step is $9 times 10^(-9)$ pt, the decoder still recovers the same word. At $d = 7$ the error bound is $5 times 10^(-8)$ pt, above half a step, and recovery is no longer guaranteed.]]



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
== Implementation details
The reference implementation is Python with PyMuPDF for page handling; the carrier is injected into the page content stream as path operators formatted with nine decimals, not drawn through the shape API. The carrier path is identified by a unique stroke colour and width, which keeps the verifier independent of the page content. The 256-bit digest is the SHA-256 of the canonical document bytes; the key schedule is derived from a secret and a document nonce with SHA-256, producing the 27-slot permutation and the word-level dither. Verification returns one of three states — *valid*, *modified*, *absent* — and never maps *absent* to *valid*. Multi-page documents are stamped page by page if a per-page seal is desired; the digest binds the canonical document bytes, so a seal on any page verifies the whole document. Recipient identifiers are assigned as 10-bit words, which bounds a deployment to 1,024 tracked copies per key epoch; larger deployments rotate the key or extend the identifier space, which changes the payload budget and is out of scope here.


= Evaluation
== Corpus
Sixty synthetic documents are generated by three independent pipelines: LibreOffice (DOCX to PDF), Typst, and Chromium print-to-PDF. Each document exists in three variants: *native*, *flattened* (300 dpi raster re-wrapped as an image-only PDF) and *print-scan simulated* (200 dpi, Gaussian blur, sensor noise, JPEG q=70). The corpus contains 180 PDFs (51.1 MB) with a SHA-256 manifest.

#table(columns: (auto, auto, auto, auto, auto), align: center)[
  [Generator], [Documents], [Variants], [Pages (native)], [Size],
  [LibreOffice DOCX to PDF], [20], [native / flattened / print-scan], [2], [18.4 MB],
  [Typst], [20], [native / flattened / print-scan], [2], [20.3 MB],
  [Chromium print-to-PDF], [20], [native / flattened / print-scan], [1], [12.5 MB],
  [Total], [60], [180 PDFs], [—], [51.1 MB],
]
#block[#text(size: 8pt, style: "italic")[Corpus composition. The carrier is a visible seal of about $126 times 185$ pt (23,227 pt²), i.e. 266 payload bits correspond to $0.0115$ bit/pt² of visible seal area.]]



== Protocol
For each document and seed, the payload is H(doc_sha ‖ seed); the 266-bit payload is embedded with keyed QIM, and the stamped PDF is attacked in the content stream (8/7-decimal truncation, payload-coordinate edit, centre-line edit) or flattened. The carrier is extracted by parsing the stream. The experiment runs 60 documents × 30 seeds (1,800 samples), plus 360 samples on flattened/print-scan inputs, plus an ablation over three carriers and keyed/unkeyed embedding.


== Metrics and attack parameters
*Geometric RMSE* is the root-mean-square coordinate change over the 27 slots; *PSNR_geom* is $20 log_10(300 "/" "RMSE")$ with the 300 pt geometry normalisation. *Exact* is one only if all 27 recovered words equal the embedded words; otherwise the sample contributes a bit-error rate over 27 words. *Detection* is one if the recovered words differ from the expected words (payload edit) or if a geometric invariant fails (centre-line edit). Truncation rewrites every coordinate number in the carrier path to 8 or 7 decimal places. The payload-coordinate edit changes one coordinate by $10^(-4)$ pt; the centre-line edit changes a non-payload coordinate by $0.5$ pt. Flattening replaces the page by a 300 dpi raster image. All attacks are applied to the stamped copy; the flattened/print-scan corpus variants are inputs to the protocol, not attacks on a stamped document.

== Results
#figure(image("../../figures/fig_capacity_distortion.svg", width: 100%), caption: [Capacity vs geometric distortion on the same 27-slot carrier. The proposed payload carries 266 bits at RMSE $5.3 times 10^(-6)$ pt; the capacity-limited baselines are marked at their maximum capacity.])
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
  [Population], [Samples], [Exact], [RMSE (pt)],
  [Native documents], [1800], [100%], [$5.31 times 10^(-6)$],
  [Flattened / print-scan PDFs, carrier stamped on top], [360], [100%], [$5.28 times 10^(-6)$],
  [Carrier ablation (3 carriers × 2 keys)], [720], [100%], [$5.31 times 10^(-6)$],
]
#block[#text(size: 8pt, style: "italic")[All populations in one view. The flattened/print-scan variants are inputs to the protocol, not attacks on a stamped document; the attack on a stamped document is flattening itself, reported in Table 2 as fail-closed. On the development machine stamping costs about 1.05 ms and verification about 0.33 ms per page.]]

== Public real-world anchors
Ten unique public project documents (whitepapers, manuscript PDFs and patent description PDFs; no client data) were stamped and attacked under the same protocol, 10 seeds each (100 samples). The results match the synthetic corpus: exact recovery in 100% of samples, 8-decimal re-serialisation survives, 7-decimal re-serialisation and payload edits are detected, and flattening removes the carrier. Mean geometric RMSE is $5.32 times 10^(-6)$ pt (PSNR_geom = 155.0 dB).

#table(columns: (auto, auto, auto), align: center)[
  [Population], [Samples], [Exact],
  [Synthetic native documents], [1800], [100%],
  [Synthetic flattened / print-scan], [360], [100%],
  [Public real-world anchors], [100], [100%],
]
#block[#text(size: 8pt, style: "italic")[Real-world anchors were only used to check that production-generated PDFs accept the carrier path; they do not exercise a population of enterprise DMS pipelines.]]





#table(columns: (auto, auto, auto, auto), align: center)[
  [Method], [Capacity], [RMSE (pt)], [Exact],
  [Proposed (keyed QIM)], [266], [$5.31 times 10^(-6)$], [yes],
  [STDM-DCT], [140], [$6.00 times 10^(-5)$], [yes],
  [Fourier descriptors], [13], [$7.36 times 10^(-5)$], [yes],
  [LSB-RDH], [27], [$7.81 times 10^(-10)$], [n/a],
  [DE-RDH], [0], [$2.91 times 10^(-10)$], [n/a],
]
#block[#text(size: 8pt, style: "italic")[Same-carrier baselines (30 seeds, slot level). Capacity-limited schemes are not a “weak baseline”: they cannot carry a 266-bit digest on 27 slots. The trade-off is the point of Figure 1.]]

PDF-level re-runs of the baselines on the same carrier (20 documents × 10 seeds, 600 samples) confirm that they remain exact through 8-decimal re-serialisation for STDM and Fourier, while the nanometre-scale LSB embedding is destroyed by 8-decimal rounding:

#table(columns: (auto, auto, auto, auto, auto), align: center)[
  [Method], [Capacity], [RMSE (pt)], [Exact], [Exact at 8 dec.],
  [STDM-DCT], [140], [$6.16 times 10^(-5)$], [100%], [100%],
  [Fourier descriptors], [13], [$7.27 times 10^(-5)$], [100%], [100%],
  [LSB-RDH], [27], [$7.03 times 10^(-10)$], [100%], [0%],
]
#block[#text(size: 8pt, style: "italic")[PDF-level baselines. The capacity column is the binding constraint: only the proposed scheme carries the 266-bit digest on the 27-slot carrier.]]



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


= Threats to Validity
*Internal validity.* Exactness is deterministic by construction, so the zero-width confidence intervals in Table 2 do not measure real-world variability; the meaningful variation must come from document generators, production PDF writers and physical capture, which this draft only partially exercises.

*External validity.* The corpus is synthetic and generated by three pipelines on one machine; real documents pass through enterprise DMS flattening, print-to-PDF converters, optimisers and archival re-writers whose coordinate serialisation differs. The 8-decimal precondition is a filter that such pipelines may fail — which is a finding, but it means the method protects only documents whose vector layer survives the pipeline.

*Construct validity.* The baselines are implemented at slot level: they share the carrier and the distortion metric but not the PDF-level embedding code of the proposed method, which favours the proposed method on implementation maturity. Lifting the baselines to the PDF level is the first item of the next revision.

*Conclusion validity.* The comparisons are exact-match and distortion measurements with 30 seeds; they are not hypothesis tests about a population of documents, and the draft avoids significance claims.

= Reproducibility and Declarations
*Reproducibility.* The corpus builder, carrier layer, attack harness and baseline implementations are versioned with the manuscript; the corpus manifest records a SHA-256 per file and the corpus is regenerated deterministically from a seed. The measured tables are produced by the harness, not typed by hand.

*Data availability.* The code and the corpus manifest are available from the author; the corpus itself is generated by the provided script and is not redistributed as a binary blob. The archived preprint is available at the concept DOI 10.5281/zenodo.23429017.

*Declarations.* Competing interests: none. Funding: none. The method is covered by a pending Ukrainian patent application (a 2026 06266). The manuscript is not under consideration elsewhere.

= Limitations and Conclusion
The evaluation is a first harness result. The baselines are re-implemented at slot level and must be lifted to the PDF level before submission; the print-scan variant is a simulation, not a physical scanner; the corpus is synthetic; and exactness is deterministic, so the reported confidence intervals are not informative about real-world variability. Capacity numbers are per seal, not per document area, and must be reported with the visible seal area in the final version. Within these limits the result is consistent and reproducible: 1,800 PDF-level samples recover the 266-bit payload exactly, 8-decimal re-serialisation is safe, 7-decimal re-serialisation and any payload edit are detected, and flattening fails closed. The next revision adds real-world PDFs and a physical print-scan set, lifts the baselines to the PDF level, reports the full ablation over document generators, and measures the cost of the 8-decimal precondition across production PDF writers. The longer-term question is whether the same construction can protect documents that are already rasterised, which the companion optical-channel paper addresses rather than this one.


= Appendix A: Proof details
*Lemma 1.* Write $delta(w) = (18w - 9207) times 10^(-9)$. For integer $w$, the values are distinct because $18w$ is strictly increasing; neighbouring words differ by exactly $18 times 10^(-9)$ pt. The decoder computes $n = round(delta dot 10^9) = 18w - 9207$ exactly while the coordinate error is below $0.5 times 10^(-9)$ pt; then $round((n + 9207)/18) = w$. The observed coordinate error is bounded in Lemma 2, below half a nanometre in the integer representation.

*Lemma 2.* Rounding a real coordinate $x$ to $d$ decimal places yields $|x - round_d(x)| <= 0.5 times 10^(-d)$ pt. For $d = 8$ this is at most $5 times 10^(-9)$ pt, while half the lattice step is $9 times 10^(-9)$ pt; the decoder's integer rounding therefore returns the same word. For $d = 7$ the bound is $5 times 10^(-8)$ pt, above half a step, so two adjacent words can be confused. The bound is worst-case; the empirical evaluation confirms the predicted transition at exactly $d = 7$.

= Appendix B: Generator settings
The corpus is generated with LibreOffice headless (DOCX to PDF, default settings), Typst (A4, 2.2 cm margins), and Chromium print-to-PDF (headless, no header/footer). Flattening uses a 300 dpi raster; the print-scan simulation uses 200 dpi, a Gaussian blur, additive Gaussian sensor noise and JPEG quality 70. All settings are recorded in the corpus builder so that the corpus can be regenerated from the published script and seed.

#bibliography("../../references.bib", style: "ieee")

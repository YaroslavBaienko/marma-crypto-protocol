#let GF = math.op("GF")
#set document(
  title: "Marma-Crypto: A Cryptographic Geometric Watermarking and Sovereign Document Sealing Protocol via Sri Yantra Nonlinear Concurrency and Elliptic Curves over GF(2^257) (DSTU 4145-2002)",
  author: "Yaroslav V. Baienko",
)

#set page(
  paper: "a4",
  margin: (top: 26mm, bottom: 26mm, left: 25mm, right: 25mm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(font: "Libertinus Serif", size: 8.5pt, fill: rgb("#555555"))
      #emph[Y. V. Baienko — Marma-Crypto Protocol Whitepaper (Sri Yantra × DSTU 4145-2002)]
      #h(1fr)
      #emph[Publication Series: EDU-VEDI-WP-2026-01-EN]
      #v(-4pt)
      #line(length: 100%, stroke: 0.4pt + rgb("#b8860b"))
    ]
  },
  footer: context [
    #set text(font: "Libertinus Serif", size: 8.5pt, fill: rgb("#555555"))
    #line(length: 100%, stroke: 0.4pt + rgb("#cccccc"))
    #v(2pt)
    © 2026 Yaroslav V. Baienko (RNOKPP 3255419579). Sealed via Marma-Crypto Protocol & DSTU 4145-2002.
    #h(1fr)
    Page #counter(page).display("1 of 1", both: true)
  ]
)

#set text(
  font: "Libertinus Serif",
  size: 10.5pt,
  lang: "en",
  region: "US",
  fill: rgb("#1e1e1e"),
)

#set par(
  justify: true,
  leading: 0.68em,
  first-line-indent: 1.2em,
)

#show heading: set par(first-line-indent: 0pt)
#show heading.where(level: 1): it => block(above: 1.5em, below: 0.8em)[
  #set text(font: "Libertinus Serif", size: 13pt, weight: "bold", fill: rgb("#1b2a4a"))
  #it
]
#show heading.where(level: 2): it => block(above: 1.1em, below: 0.6em)[
  #set text(font: "Libertinus Serif", size: 11pt, weight: "bold", fill: rgb("#7d5906"))
  #it
]

#set heading(numbering: "1.")

// ============================================================================
// TITLE BLOCK (SATOSHI NAKAMOTO 2008 WHITEPAPER STYLE)
// ============================================================================
#align(center)[
  #block(width: 94%)[
    #set par(justify: false, first-line-indent: 0pt)
    #text(size: 9pt, weight: "bold", tracking: 1.5pt, fill: rgb("#9a6f0a"))[
      TECHNICAL WHITEPAPER & DEFENSIVE PRIOR ART SPECIFICATION
    ]
    #v(6pt)
    #text(size: 16.5pt, weight: "bold", fill: rgb("#1b2a4a"))[
      Marma-Crypto: A Cryptographic Geometric Watermarking and Sovereign Document Sealing Protocol via Sri Yantra Nonlinear Concurrency and Elliptic Curves over $GF(2^(257))$ (DSTU 4145-2002)
    ]
    #v(8pt)
    #text(size: 11.5pt, weight: "bold", fill: rgb("#1e1e1e"))[
      Yaroslav V. Baienko
    ]
    #v(2pt)
    #text(size: 9.5pt, fill: rgb("#444444"))[
      Attorney-at-Law, Legal Engineer & Applied Cryptography Researcher (Odesa / Kyiv, Ukraine)\
      Email: #raw("zerhug@gmail.com") · Qualified Certificate Serial: #raw("10FF6F932221FA00CB4407000000000130616768")\
      GPG Fingerprint (RSA-4096): #raw("3D5A ACFD E32C 98FE 8819 9D47 D2A2 C1C4 9164 673B")
    ]
  ]
]

#v(10pt)

// ABSTRACT
#align(center)[
  #block(
    width: 90%,
    inset: (x: 16pt, y: 12pt),
    stroke: (left: 2.5pt + rgb("#b8860b"), right: 0.5pt + rgb("#d8c898"), top: 0.5pt + rgb("#d8c898"), bottom: 0.5pt + rgb("#d8c898")),
    fill: rgb("#fdfbf7"),
    radius: 3pt,
  )[
    #set par(justify: true, first-line-indent: 0pt)
    #align(center)[#text(weight: "bold", size: 10.5pt, fill: rgb("#1b2a4a"))[Abstract]]
    #v(4pt)
    #text(size: 9.6pt)[
      A purely mathematical document integrity system would allow an author to irrevocably bind the semantic content of a text to the visible vector geometry of a seal without relying on external verification registries, pixel noise, or aesthetically intrusive stamps. Conventional digital signatures detach the binary PKCS\#7 container from the visual rendering of the page, whereas raster watermarks degrade under scaling and vector conversion. In this paper, we propose the *Marma-Crypto* protocol — a dual-layer cryptographic geometric watermarking system that maps an elliptic curve digital signature vector $(r, s)$ over the characteristic-two Galois field $GF(2^(257))$ per Ukrainian National Standard DSTU 4145-2002 (coupled with GOST 34.311-95 and DSTU 7564:2014 "Kupyna" message digests) directly into floating-point vertex micro-perturbations $delta_k in [-10^(-5), +10^(-5)]$ of the nine interlocking triangles of the classical *Sri Yantra* (*Nava-Cakra*). Because the nine triangles are governed by a nonlinear concurrency system of 54 triple intersections (*marmas*) and preserve the exact bilateral symmetry invariant $l x_k + r x_k = 2 C_x = 600.0$, the resulting vector seal is optically indistinguishable from the canonical geometric archetype while providing instantaneous, zero-tolerance detection of any single-byte text modification or coordinate drift exceeding $10^(-7)$ units.
    ]
  ]
]

#v(8pt)

= Introduction

Digital document authentication in legal practice, international arbitration, engineering, and intellectual property protection relies on two historically disconnected mechanisms: binary cryptographic containers (CMS/CAdES, PDF PAdES) and visual watermarks. Considered in isolation, each mechanism exhibits a fundamental structural limitation.

First, standard qualified electronic signatures (QES) exist as an invisible ASN.1 binary payload appended to a file. The visual stamp rendered on a PDF page—typically a rectangular blue box or QR code—is merely a decorative annotation: the geometric coordinates of its lines carry no cryptographic entropy and satisfy no algebraic equation linking them to the document's digest.

Second, classical digital steganography (Least Significant Bit modification in raster bitmaps, DCT/wavelet frequency modulation, or periodic Lissajous guilloché grids) is designed for pixel matrices or offset banknote printing. When applied to modern vector documents (`.pdf`, `.svg`, `.docx`, CAD blueprints), raster perturbations either vanish upon vector re-rendering or degrade typographic fidelity.

We pose the following problem: *Can we construct a closed planimetric configuration of high algebraic coupling in which the floating-point vertex coordinates of vector polygons simultaneously satisfy a strict system of nonlinear geometric invariants and bijectively encode the $(r, s)$ elliptic curve signature vector of the document's content?*

In this Whitepaper, we demonstrate that the nonlinear nine-triangle configuration of the *Sri Yantra* (reconstructed analytically by A. P. Kulaichev, 1984), coupled with elliptic curve arithmetic over $GF(2^(257))$ (DSTU 4145-2002), provides an exact mathematical solution.

= Nonlinear Planimetric Concurrency of the 9-Triangle Sri Yantra

The central geometric core of the Sri Yantra (*Nava-Cakra*) is formed by the mutual intersection of nine primary isosceles triangles inscribed within a circle of radius $R_0$ centered at the *Bindu* $(C_x, C_y) = (300, 300)$ in the canonical coordinate domain $[0, 600]^2$:
- four upward-pointing *Śiva* triangles ($Delta_("U1"), Delta_("U2"), Delta_("U3"), Delta_("U4")$) with $y_("apex") < y_("base")$;
- five downward-pointing *Śakti* triangles ($nabla_("D1"), nabla_("D2"), nabla_("D3"), nabla_("D4"), nabla_("D5")$) with $y_("apex") > y_("base")$.

== Algebraic Collinearity and Intersection Operators

Given two distinct points $(x_a, y_a)$ and $(x_b, y_b)$ ($y_a != y_b$) defining a lateral edge of a triangle, the linear extension operator to an arbitrary horizontal ordinate $y$ is defined as:
$ cal(L)(y_a, x_a, y_b, x_b; y) = x_a + (x_b - x_a) frac(y - y_a, y_b - y_a). $

The intersection of two non-parallel lateral edges $ell_1 = ((x_1, y_1), (x_2, y_2))$ and $ell_2 = ((x_3, y_3), (x_4, y_4))$ is given by the bilinear Cramer operator $cal(I)(ell_1, ell_2) = (x^*, y^*)$:
$ D = (x_1 - x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 - x_4), $
$ x^* = frac((x_1 y_2 - y_1 x_2)(x_3 - x_4) - (x_1 - x_2)(x_3 y_4 - y_3 x_4), D), quad
  y^* = frac((x_1 y_2 - y_1 x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 y_4 - y_3 x_4), D). $

== Triple Concurrency Condition (54 Marmas)

Unlike an arbitrary collection of polygons, the nine triangles of the Sri Yantra are constrained by a simultaneous system of nonlinear concurrency equations requiring three lines to intersect at a single point (*marma* $M_(i j k)$):
$ det mat(
  A_i, B_i, C_i;
  A_j, B_j, C_j;
  A_k, B_k, C_k
) = 0 quad forall (i, j, k) in cal(M)_(54), $
where $A_m x + B_m y + C_m = 0$ denote the line equations of the respective lateral edges and horizontal bases. Consequently, the entire 27-degree-of-freedom configuration reduces to 4 free parameters of the inner core, from which all remaining vertices are deterministically propagated via nested chains of $cal(I)$ and $cal(L)$.

#figure(
  image("sri_yantra_whitepaper_diagram.svg", width: 58%),
  caption: [Canonical vector reconstruction of the Sri Yantra with embedded Marma-Crypto signature (DSTU 4145-2002, 9 interlocking triangles, 43 sub-triangles, 54 triple marmas, 8-petal _Padma_, 16-petal _Kamala_, and triple _Bhupura_).]
)

= Bilateral Symmetry Invariant & Micro-Coordinate Modulation

Each of the nine triangles $T_k$ ($k in {1, dots, 9}$), ordered in the canonical sequence $("D1", "U1", "D2", "U2", "D3", "D4", "U3", "D5", "U4")$, is uniquely parameterized by the 4-tuple:
$ T_k = (y_(k,"base"), y_(k,"apex"), l x_k, r x_k), $
where $y_(k,"base")$ is the horizontal base ordinate, $y_(k,"apex")$ is the apex ordinate on the central vertical axis $x = C_x = 300.0$, and $l x_k, r x_k$ are the left and right base abscissae.

== Theorem on Bilateral Symmetry Preservation under Perturbation $vec(delta)_9$

*Definition 1 (Symmetry Invariant).* The canonical diagram satisfies the exact bilateral symmetry relation across $C_x = 300.0$:
$ cal(S)_k (T_k) = frac(l x_k + r x_k, 2) - C_x = 0, quad forall k in {1, dots, 9}. $

*Definition 2 (Micro-Coordinate Modulation Operator).* Given a cryptographic perturbation vector $vec(delta) = (delta_1, delta_2, dots, delta_9) in [-10^(-5), +10^(-5)]^9$, the modulated triangle $tilde(T)_k = cal(W)(T_k, delta_k)$ is defined by:
$ tilde(y)_(k,"base") = y_(k,"base") + delta_k, quad
  tilde(y)_(k,"apex") = y_(k,"apex") - delta_k, quad
  tilde(l x)_k = l x_k - frac(delta_k, 2), quad
  tilde(r x)_k = r x_k + frac(delta_k, 2). $

*Proof.* Substituting the modulated coordinates $tilde(T)_k$ into the symmetry functional $cal(S)_k$ yields:
$ cal(S)_k (tilde(T)_k) = frac(tilde(l x)_k + tilde(r x)_k, 2) - C_x = frac((l x_k - delta_k \/ 2) + (r x_k + delta_k \/ 2), 2) - C_x = frac(l x_k + r x_k, 2) - C_x = 0. $
Thus, for any signature vector $vec(delta) in [-10^(-5), +10^(-5)]^9$, the bilateral symmetry error $Delta_("sym") = max_k |cal(S)_k (tilde(T)_k)|$ vanishes identically within IEEE 754 `float64` precision ($< 10^(-12)$), while the embedded perturbation is uniquely recovered by the verifier as:
$ hat(delta)_k = frac((tilde(y)_(k,"base") - y_(k,"base")) - (tilde(y)_(k,"apex") - y_(k,"apex")), 2). $

= Elliptic Curve Signature Mapping over $GF(2^(257))$ (DSTU 4145-2002)

To achieve full cryptographic alignment with Ukraine's national public key infrastructure (КНЕДП), *Marma-Crypto* (`v1.2.0`) integrates three state cryptographic primitives with deterministic geometric quantization.

== Triple Cryptographic Digest Layer

Let $M$ denote the canonically normalized byte stream of the document's content. Three independent 256-bit digests are computed simultaneously:
1. $H_("GOST") = "GOST 34.311-95"(M)$ — 256-bit digest using the DSTU S-box parameterization;
2. $H_("Kupyna") = "DSTU 7564:2014"(M)$ — 256-bit national hash standard ("Kupyna-256");
3. $H_("SHA") = "SHA-256"(M)$ — FIPS 180-4 cross-platform digest.

== Elliptic Curve Arithmetic over $GF(2^(257))$ and Deterministic $(r, s)$ Generation

Signatures are computed over the binary extension field $GF(2^(257)) = GF(2)[t] \/ (t^(257) + t^(12) + 1)$ (`DSTU_PB_257`) per DSTU 4145-2002 on the elliptic curve:
$ E(GF(2^(257))): quad y^2 + x y = x^3 + a x^2 + b, quad a = 0, space b = 1, $
with base point $P = (x_P, y_P)$ of prime order $n$. To guarantee deterministic reproducibility of the geometric perturbation vector $vec(delta)_9$ and eliminate nonce-reuse vulnerabilities, the ephemeral scalar $e in [1, n-1]$ is derived via RFC 6979 HMAC-DRBG:
$ e = "HMAC-DRBG"_"SHA256" (d, H_("GOST")(M)) mod (n - 1) + 1. $

Computing the pre-signature point $R = e dot P = (x_R, y_R)$ on $E(GF(2^(257)))$, the field element $x_R$ is multiplied in $GF(2^(257))$ by $h = "ToField"(H_("GOST")(M))$ to produce $(r, s)$:
$ r = "Truncate"_n (h times.o_(GF(2^(257))) x_R), quad s = (e + d dot r) mod n. $

Public verification against the signer's public point $Q = -d dot P$ evaluates:
$ R' = s dot P + r dot Q = (x_(R'), y_(R')), quad r' = "Truncate"_n (h times.o_(GF(2^(257))) x_(R')) eq.quest r. $

== Bijective Quantization $(r, s) mapsto vec(delta)_9$

The elliptic curve signature $(r, s)$ and triple digests are compressed into a 256-bit binding vector:
$ V = "HMAC-SHA256"_"Key" ("MARMA-DSTU4145-V1.2" || H_("SHA") || H_("GOST") || H_("Kupyna") || r || s). $
Extracting nine 16-bit unsigned integers $u_k = "uint16"_"BE"(V[2k : 2k+2])$ ($k in {0, dots, 8}$) yields the exact micro-perturbation vector:
$ delta_(k+1) = lr((frac(u_k, 65535.0) - 0.5)) times 2 dot 10^(-5), quad k = 0, dots, 8. $

= Four-Layer Sovereign Document Sealing & Zero-Tolerance Verification

The *Marma-Crypto* suite embeds four concentric layers of verification into every sealed document:
1. *Full-Page Vector Watermark:* Centered Sri Yantra diagram on every PDF page (5.5% opacity, `#8A6608` gold stroke) with vertex coordinates modulated by $vec(delta)_9$.
2. *Corner Golden Bindu Seal:* Circular vector emblem featuring a 24-ray guilloché ring, 9 triangles, signer identity, key fingerprint, and SHA-256 micro-text.
3. *Embedded `MARMA_SEAL::v1.2-DSTU4145` Manifest:* Stores the public curve point $Q$, $(r, s)$ vector, and 9-triangle coordinates for offline mathematical verification ($Delta_("sym") < 10^(-7)$, $Delta_("coord") < 10^(-7)$).
4. *Qualified ETSI PAdES / CAdES Container:* Appends a state-compliant `/ByteRange` CMS signature with КНЕДП TSP timestamp and `/DSS` LTV revocation data verifiable on `czo.gov.ua`.

= Formal Patent & Priority Claims (WIPO / UKRNOIVI Standard)

*Claim 1 (Independent — Method).* A computer-implemented method for cryptographic-geometric document integrity protection and authenticity verification, comprising normalizing document content, computing cryptographic digests, and generating a digital signature using a signer's key, *characterized in that*:
1. a coupled planimetric system of nine mutually intersecting triangles of the Sri Yantra diagram (four upward-pointing and five downward-pointing) having 54 triple line-intersection nodes is used as a vector signature carrier;
2. a deterministic signature vector $(r, s)$ is computed on an elliptic curve over the Galois field $GF(2^(257))$ per DSTU 4145-2002 from the document digests computed per GOST 34.311-95 and DSTU 7564:2014;
3. the signature vector $(r, s)$ is mapped into a nine-dimensional micro-perturbation vector $vec(delta) = (delta_1, dots, delta_9)$ bounded by $|delta_k| <= 10^(-5)$ coordinate units;
4. the base ordinates $y_(k,"base")$, apex ordinates $y_(k,"apex")$, and lateral base abscissae $l x_k, r x_k$ of each of the nine triangles are modulated according to $tilde(y)_(k,"base") = y_(k,"base") + delta_k$, $tilde(y)_(k,"apex") = y_(k,"apex") - delta_k$, $tilde(l x)_k = l x_k - delta_k \/ 2$, and $tilde(r x)_k = r x_k + delta_k \/ 2$, thereby identically preserving the bilateral symmetry invariant $tilde(l x)_k + tilde(r x)_k = 2 C_x$;
5. upon verification, the nine-triangle coordinates are extracted and validated against both the elliptic curve equation $s dot P + r dot Q = R$ over $GF(2^(257))$ and the geometric thresholds $Delta_("sym") < 10^(-7)$ and $Delta_("coord") < 10^(-7)$, rejecting any unauthorized alteration of text or geometry.

*Claim 2 (Dependent — Dual PAdES/CAdES Sealing).* The method of Claim 1, wherein after embedding the vector watermark and corner Golden Bindu Seal, the document is further sealed with a qualified electronic signature in ETSI PAdES (`/ByteRange` + TSP + `/DSS`) or CAdES (`.p7s`) format.

= Conclusion

We have formulated and implemented the *Marma-Crypto* protocol, unifying the nonlinear planimetric geometry of the nine-triangle Sri Yantra with elliptic curve cryptography over $GF(2^(257))$ (DSTU 4145-2002). This Whitepaper is itself cryptographically sealed using the protocol it specifies, constituting a self-referential proof of authorship and priority.

#v(8pt)
#line(length: 100%, stroke: 0.5pt + rgb("#b8860b"))

#set heading(numbering: none)
= References

#set par(first-line-indent: 0pt)
1. *Kulaichev, A. P.* (1984). Sriyantra and its Mathematical Properties. _Indian Journal of History of Science_, 19(3), 279–292.
2. *Nakamoto, S.* (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. `https://bitcoin.org/bitcoin.pdf`.
3. *DSTU 4145-2002.* Information technology. Cryptographic protection of information. Digital signature based on elliptic curves. Formation and verification. Kyiv: Derzhstandart of Ukraine, 2002.
4. *GOST 34.311-95 / DSTU 7564:2014 ("Kupyna").* National Cryptographic Hash Function Standards of Ukraine.
5. *Pornin, T.* (2013). Deterministic Usage of DSA and ECDSA. _IETF RFC 6979_.
6. *ETSI EN 319 142-1 V1.1.1* (2016). Electronic Signatures and Infrastructures (ESI); PAdES digital signatures.

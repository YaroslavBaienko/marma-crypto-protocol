#let GF = math.op("GF")
#set document(
  title: "Marma-Crypto: A Cryptographic Geometric Watermarking and Sovereign Document Sealing Protocol via Sri Yantra Nonlinear Concurrency and Elliptic Curves over GF(2^257) (DSTU 4145-2002)",
  author: "Yaroslav V. Baienko",
)

#set page(
  paper: "a4",
  margin: (top: 24mm, bottom: 24mm, left: 24mm, right: 24mm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(font: "Libertinus Serif", size: 8.5pt, fill: rgb("#555555"))
      #emph[Y. V. Baienko — Marma-Crypto Protocol Whitepaper (Sri Yantra × DSTU 4145-2002)]
      #h(1fr)
      #emph[Publication Series: EDU-VEDI-WP-2026-01-EN (v1.2.1)]
      #v(-4pt)
      #line(length: 100%, stroke: 0.4pt + rgb("#b8860b"))
    ]
  },
  footer: context [
    #set text(font: "Libertinus Serif", size: 8.5pt, fill: rgb("#555555"))
    #line(length: 100%, stroke: 0.4pt + rgb("#cccccc"))
    #v(2pt)
    © 2026 Yaroslav V. Baienko (TIN 3255419579). DOI: 10.5281/zenodo.23429018 · Marma-Crypto Protocol.
    #h(1fr)
    Page #counter(page).display("1 of 1", both: true)
  ]
)

#set text(
  font: "Libertinus Serif",
  size: 10.3pt,
  lang: "en",
  region: "US",
  fill: rgb("#1e1e1e"),
)

#set par(
  justify: true,
  leading: 0.66em,
  first-line-indent: 1.2em,
)

#show heading: set par(first-line-indent: 0pt)
#show heading.where(level: 1): it => block(above: 1.4em, below: 0.75em)[
  #set text(font: "Libertinus Serif", size: 12.5pt, weight: "bold", fill: rgb("#1b2a4a"))
  #it
]
#show heading.where(level: 2): it => block(above: 1.05em, below: 0.55em)[
  #set text(font: "Libertinus Serif", size: 10.8pt, weight: "bold", fill: rgb("#7d5906"))
  #it
]

#set heading(numbering: "1.")

// ============================================================================
// TITLE BLOCK (ACADEMIC SPECIFICATION & DEFENSIVE PRIOR ART)
// ============================================================================
#align(center)[
  #block(width: 95%)[
    #set par(justify: false, first-line-indent: 0pt)
    #text(size: 8.8pt, weight: "bold", tracking: 1.4pt, fill: rgb("#9a6f0a"))[
      TECHNICAL WHITEPAPER & DEFENSIVE PRIOR ART SPECIFICATION
    ]
    #v(6pt)
    #text(size: 15.8pt, weight: "bold", fill: rgb("#1b2a4a"))[
      Marma-Crypto: A Cryptographic Geometric Watermarking and Sovereign Document Sealing Protocol via Sri Yantra Nonlinear Concurrency and Elliptic Curves over $GF(2^(257))$ (DSTU 4145-2002)
    ]
    #v(7pt)
    #text(size: 11.2pt, weight: "bold", fill: rgb("#1e1e1e"))[
      Yaroslav V. Baienko
    ]
    #v(2pt)
    #text(size: 9.2pt, fill: rgb("#444444"))[
      Attorney-at-Law, Legal Engineer & Applied Cryptography Researcher (Odesa / Kyiv, Ukraine)\
      Email: #raw("zerhug@gmail.com") · Qualified X.509 Serial: #raw("10FF6F932221FA00CB4407000000000130616768")\
      OpenPGP Fingerprint (RSA-4096): #raw("3D5A ACFD E32C 98FE 8819 9D47 D2A2 C1C4 9164 673B") · CERN Zenodo DOI: #raw("10.5281/zenodo.23429018")
    ]
  ]
]

#v(8pt)

// ABSTRACT
#align(center)[
  #block(
    width: 92%,
    inset: (x: 15pt, y: 11pt),
    stroke: (left: 2.5pt + rgb("#b8860b"), right: 0.5pt + rgb("#d8c898"), top: 0.5pt + rgb("#d8c898"), bottom: 0.5pt + rgb("#d8c898")),
    fill: rgb("#fdfbf7"),
    radius: 3pt,
  )[
    #set par(justify: true, first-line-indent: 0pt)
    #align(center)[#text(weight: "bold", size: 10.2pt, fill: rgb("#1b2a4a"))[Abstract]]
    #v(4pt)
    #text(size: 9.4pt)[
      A purely mathematical document integrity system must allow an author to irrevocably bind the semantic content of a text to the visible vector geometry of a seal without relying on centralized verification servers, raster pixel noise, or decorative visual stamps. Conventional digital signatures detach the binary CMS / PKCS\#7 (IETF RFC 5652) container from the visual rendering of the page, whereas raster watermarks degrade under scaling and vector conversion. In this paper, we propose the *Marma-Crypto* protocol — a dual-layer cryptographic geometric watermarking system that deterministically maps an elliptic curve digital signature vector $(r, s)$ over the characteristic-two Galois field $GF(2^(257))$ per Ukrainian National Standard DSTU 4145-2002 (coupled with GOST 34.311-95, DSTU 7564:2014 "Kupyna", and FIPS 180-4 SHA-256 message digests) via a 24-bit block quantizer directly into floating-point vertex micro-perturbations $delta_k in [-10^(-5), +10^(-5)]$ of the nine interlocking triangles of the classical *Sri Yantra* (*Nava-Cakra*). Because the nine triangles are governed by a nonlinear concurrency system of 54 triple intersections (*marmas*), identically preserve the analytical bilateral symmetry invariant $l x_k + r x_k = 2 C_x$, and encapsulate a long-term ETSI EN 319 142-1 (PAdES-B-LTA) signature container with an RFC 3161 Time-Stamp Token and ISO 32000-2 Document Security Store (`/DSS`), the resulting vector seal is optically indistinguishable from the canonical geometric archetype while enabling keyless public verification and zero-tolerance detection of any single-byte text modification or vertex drift exceeding $10^(-7)$ coordinate units.
    ]
  ]
]

#v(6pt)

= Introduction & Problem Formulation

Electronic document authentication in judicial proceedings, international commercial arbitration, engineering, and intellectual property protection relies on two historically disconnected mechanisms: binary cryptographic containers (IETF RFC 5652 CMS, ETSI EN 319 122 CAdES, ETSI EN 319 142 PAdES) and visual watermarks. Considered in isolation, each mechanism exhibits a fundamental structural limitation.

First, standard qualified electronic signatures (QES / EU eIDAS) exist as an invisible ASN.1 DER structure appended to a file stream. The visual stamp rendered on a PDF page—typically a rectangular box or raster QR code—is merely a decorative annotation: the geometric coordinates of its lines carry no cryptographic entropy and satisfy no algebraic equation linking them to the document's message digest.

Second, classical digital steganography (Least Significant Bit modification in raster bitmaps, DCT/wavelet frequency modulation, or periodic Lissajous guilloché grids) is designed for pixel matrices or offset banknote printing. When applied to modern vector formats (ISO 32000-2 `.pdf`, W3C `.svg`, ISO/IEC 29500 `.docx`, CAD blueprints), raster perturbations either vanish upon vector re-rendering or degrade typographic fidelity.

We formulate the following research problem: *Can we construct a closed planimetric configuration of high algebraic coupling in which the floating-point vertex coordinates of vector polygons simultaneously satisfy a strict system of nonlinear geometric invariants and bijectively encode the $(r, s)$ elliptic curve signature vector of the normalized document content while supporting keyless public verification?*

In this Whitepaper, we prove that the nonlinear nine-triangle configuration of the *Sri Yantra* (analytically investigated by A. P. Kulaichev, 1984 [1]), coupled with elliptic curve arithmetic over the binary Galois field $GF(2^(257))$ (DSTU 4145-2002), provides an exact mathematical solution.

= Nonlinear Planimetric Concurrency of the 9-Triangle Sri Yantra

The central geometric core of the Sri Yantra (*Nava-Cakra*) is formed by the mutual intersection of nine primary isosceles triangles inscribed within a circle of radius $R_0 = lambda dot 100$ centered on the symmetry axis $C_x = lambda dot 150$ in the canonical coordinate domain $[0, 2 C_x]^2$ (where scale factor $lambda = 1$ corresponds to the base domain $[0, 300]^2$ for PDF/OOXML vector seals and $lambda = 2$ corresponds to the expanded domain $[0, 600]^2$ for standalone reference SVG diagrams):
- four upward-pointing *Śiva* triangles ($Delta_("U1"), Delta_("U2"), Delta_("U3"), Delta_("U4")$) oriented toward the upper pole ($y_("apex") < y_("base")$);
- five downward-pointing *Śakti* triangles ($nabla_("D1"), nabla_("D2"), nabla_("D3"), nabla_("D4"), nabla_("D5")$) oriented toward the lower pole ($y_("apex") > y_("base")$).

== Algebraic Collinearity and Intersection Operators

Given two distinct points $(x_a, y_a)$ and $(x_b, y_b)$ ($y_a != y_b$) defining a lateral edge of a triangle, the linear extension operator to an arbitrary horizontal ordinate $y$ is defined as:
$ cal(L)(y_a, x_a, y_b, x_b; y) = x_a + (x_b - x_a) frac(y - y_a, y_b - y_a). $

The intersection of two non-parallel lateral edges $ell_1 = ((x_1, y_1), (x_2, y_2))$ and $ell_2 = ((x_3, y_3), (x_4, y_4))$ is given by the bilinear Cramer operator $cal(I)(ell_1, ell_2) = (x^*, y^*)$:
$ D = (x_1 - x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 - x_4), $
$ x^* = frac((x_1 y_2 - y_1 x_2)(x_3 - x_4) - (x_1 - x_2)(x_3 y_4 - y_3 x_4), D), quad
  y^* = frac((x_1 y_2 - y_1 x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 y_4 - y_3 x_4), D). $

== Triple Concurrency Condition (54 Marmas)

Unlike an arbitrary collection of polygons, the nine triangles of the Sri Yantra are constrained by a simultaneous system of nonlinear concurrency equations requiring three lines to intersect at a single nodal point (*marma* $M_(i j k)$):
$ det mat(
  A_i, B_i, C_i;
  A_j, B_j, C_j;
  A_k, B_k, C_k
) = 0 quad forall (i, j, k) in cal(M)_(54), $
where $A_m x + B_m y + C_m = 0$ denote the line equations of the respective lateral edges and horizontal bases. Consequently [1], the entire 27-degree-of-freedom configuration of nine symmetric triangles reduces to 4 free parameters of the inner core, from which all remaining vertices are deterministically propagated via nested compositions of $cal(I)$ and $cal(L)$ (enforcing exact nodal ordinate identities $a y_("U3") = b y_("D1")$, $b y_("U3") = a y_("D2")$, $a y_("U2") = b y_("D3")$, $b y_("U2") = a y_("D4")$, $b y_("U4") = a y_("D3")$, $a y_("U4") = b y_("D2")$, and $a y_("D5") = b y_("U1")$).

#figure(
  image("sri_yantra_whitepaper_diagram.svg", width: 54%),
  caption: [Canonical vector reconstruction of the Sri Yantra with embedded Marma-Crypto signature (DSTU 4145-2002, 9 interlocking triangles, 43 sub-triangles, 54 triple marmas, 8-petal _Padma_, 16-petal _Kamala_, and triple _Bhupura_).]
)

= Bilateral Symmetry Invariant & Micro-Coordinate Modulation

Each of the nine triangles $T_k$ ($k in {1, dots, 9}$), ordered in the canonical core indexing sequence $("D1", "U1", "U3", "U2", "D3", "D2", "U4", "D4", "D5")$, is uniquely parameterized by the scalar 4-tuple:
$ T_k = (l x_k, b y_k, a y_k, r x_k), $
where $l x_k, r x_k$ are the left and right horizontal base abscissae, $b y_k$ is the horizontal base ordinate, and $a y_k$ is the central apex ordinate on the vertical symmetry axis $x = C_x = 150 lambda$.

== Theorem on Bilateral Symmetry Preservation under Perturbation $vec(delta)_9$

*Definition 1 (Bilateral Symmetry Invariant).* The canonical diagram satisfies the exact symmetry relation across the central axis $C_x = 150 lambda$:
$ cal(S)_k (T_k) = frac(l x_k + r x_k, 2) - C_x = 0, quad forall k in {1, dots, 9}. $

*Definition 2 (Micro-Coordinate Modulation Operator).* Given a cryptographic perturbation vector $vec(delta) = (delta_1, delta_2, dots, delta_9) in [-10^(-5), +10^(-5)]^9$ and spatial scale factor $lambda = C_x \/ 150 in {1, 2}$, the modulated triangle $tilde(T)_k = cal(W)_lambda (T_k, delta_k)$ is defined by the affine antisymmetric transformation:
$ tilde(l x)_k = l x_k + lambda delta_k, quad
  tilde(r x)_k = 2 C_x - tilde(l x)_k = r x_k - lambda delta_k, quad
  tilde(b y)_k = b y_k + frac(lambda delta_k, 2), quad
  tilde(a y)_k = a y_k. $

*Proof.* Substituting the modulated coordinates $tilde(T)_k$ into the symmetry functional $cal(S)_k$ yields:
$ cal(S)_k (tilde(T)_k) = frac(tilde(l x)_k + tilde(r x)_k, 2) - C_x = frac((l x_k + lambda delta_k) + (r x_k - lambda delta_k), 2) - C_x = frac(l x_k + r x_k, 2) - C_x = 0. $
Thus, for any signature vector $vec(delta) in [-10^(-5), +10^(-5)]^9$, the bilateral symmetry error $Delta_("sym") = max_k |cal(S)_k (tilde(T)_k)|$ vanishes identically within IEEE 754 `binary64` precision ($< 10^(-12)$), while the embedded perturbation is redundantly verified across three independent coordinate channels per triangle ($tilde(l x)_k - l x_k = lambda delta_k$, $r x_k - tilde(r x)_k = lambda delta_k$, $2(tilde(b y)_k - b y_k) = lambda delta_k$) with an unperturbed apex anchor $tilde(a y)_k = a y_k$:
$ Delta_("coord") = max_(k in {1, dots, 9}) max lr((|tilde(l x)_k - (l x_k + lambda delta_k)|, space |tilde(r x)_k - (r x_k - lambda delta_k)|, space |tilde(b y)_k - (b y_k + lambda delta_k \/ 2)|, space |tilde(a y)_k - a y_k|)). $

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (center, left, right, right, right, right),
    fill: (x, y) => if y == 0 { rgb("#1b2a4a") } else if calc.even(y) { rgb("#f8f5ec") } else { white },
    stroke: 0.4pt + rgb("#c8b88a"),
    text(fill: white, weight: "bold")[No. $k$],
    text(fill: white, weight: "bold")[Triangle ($T_k$)],
    text(fill: white, weight: "bold")[$l x_k$ ($lambda = 1$)],
    text(fill: white, weight: "bold")[$b y_k$ ($lambda = 1$)],
    text(fill: white, weight: "bold")[$a y_k$ ($lambda = 1$)],
    text(fill: white, weight: "bold")[$r x_k$ ($lambda = 1$)],
    [1], [$nabla_("D1")$ (Śakti-1, down)], [`53.65669560`],  [`123.20508076`], [`250.00000000`], [`246.34330440`],
    [2], [$Delta_("U1")$ (Śiva-1, up)],    [`52.98401103`],  [`174.24660561`], [`50.00000000`],  [`247.01598897`],
    [3], [$Delta_("U3")$ (Śiva-3, up)],    [`98.71823313`],  [`220.03828947`], [`123.20508076`], [`201.28176687`],
    [4], [$Delta_("U2")$ (Śiva-2, up)],    [`78.26467998`],  [`197.92315674`], [`78.10499178`],  [`221.73532002`],
    [5], [$nabla_("D3")$ (Śakti-3, down)], [`90.48569229`],  [`78.10499178`],  [`160.66014976`], [`209.51430771`],
    [6], [$nabla_("D2")$ (Śakti-2, down)], [`80.98384839`],  [`103.12199145`], [`220.03828947`], [`219.01615161`],
    [7], [$Delta_("U4")$ (Śiva-4, up)],    [`114.94885006`], [`160.66014976`], [`103.12199145`], [`185.05114994`],
    [8], [$nabla_("D4")$ (Śakti-4, down)], [`116.35142605`], [`134.30757627`], [`197.92315674`], [`183.64857395`],
    [9], [$nabla_("D5")$ (Śakti-5, down)], [`124.61190803`], [`144.79777263`], [`174.24660561`], [`175.38809197`],
  ),
  caption: [Canonical planimetric coordinates of the 9 Sri Yantra triangles in the base domain $[0, 300]^2$ ($C_x = 150.0$, $l x_k + r x_k = 300.00000000$; for the $[0, 600]^2$ domain, all coordinates scale homogeneously by $lambda = 2$).]
)

= Cryptographic Core: DSTU 4145-2002 over Galois Field $GF(2^(257))$

The *Marma-Crypto* protocol unifies Ukrainian national cryptographic standards and international PKI specifications with deterministic mapping into the nonlinear geometry of the Sri Yantra.

== Triple Cryptographic Digest Layer

Let $M$ denote the canonically normalized byte stream of the document's content (for PDF, the page-ordered text stream excluding seal metadata lines; for OOXML `.docx`, the sequence of paragraphs and table cells; for `.svg`, the canonical metadata payload). Three independent 256-bit cryptographic digests are computed simultaneously:
1. $H_("GOST") = "GOST 34.311-95"(M)$ — 256-bit digest based on GOST 28147-89 with DSTU S-boxes [4];
2. $H_("Kupyna") = "DSTU 7564:2014"(M)$ — 256-bit national hash standard ("Kupyna-256") [5];
3. $H_("SHA") = "SHA-256"(M)$ — international FIPS 180-4 cross-platform digest.

== Elliptic Curve Arithmetic over $GF(2^(257))$ and Deterministic $(r, s)$ Generation

Digital signatures are computed over the binary extension field $GF(2^(257)) = GF(2)[t] \/ (t^(257) + t^(12) + 1)$ in polynomial basis (standard curve `DSTU_PB_257` per DSTU 4145-2002 [3]), defined by the Weierstrass equation:
$ E(GF(2^(257))): quad y^2 + x y = x^3 + a x^2 + b, quad a = 0, space b = 1, $
with base point $P = (x_P, y_P)$ of prime order $n$:
$ n = #raw("0x800000000000000000000000000000006759213AF182E987D3E17714907D470D"). $

To eliminate nonce-reuse vulnerabilities and guarantee 100% deterministic reproducibility of the geometric perturbation vector $vec(delta)_9$, the ephemeral scalar $e in [1, n-1]$ is derived via IETF RFC 6979 [6]:
$ e = "HMAC-DRBG"_"SHA256" (d, H_("GOST")(M)) mod (n - 1) + 1. $

Computing the pre-signature point $R = e dot P = (x_R, y_R) in E(GF(2^(257)))$, the non-zero field element $x_R$ is multiplied in $GF(2^(257))$ by $h = "ToField"(H_("GOST")(M))$ to produce $(r, s)$:
$ r = "Truncate"_n (h times.o_(GF(2^(257))) x_R), quad s = (e + d dot r) mod n. $

Public verification against the signer's public point $Q = -d dot P$ evaluates the fundamental DSTU 4145-2002 identity:
$ R' = s dot P + r dot Q = (x_(R'), y_(R')), quad r' = "Truncate"_n (h times.o_(GF(2^(257))) x_(R')) eq.quest r. $

== Keyless Public Binding & 24-Bit Quantization $(r, s) mapsto vec(delta)_9$

To enable *keyless public verification* of the vector geometry by any third party without exposing the author's private key, the hexadecimal signature components $(r, s)$ are compressed into a public 256-bit binding vector $V$:
$ V = "SHA-256"(r_("hex") || #raw("\"::\"") || s_("hex")). $

From the first $9 times 3 = 27$ bytes of digest $V$, nine 24-bit big-endian unsigned integers $u_k = "uint24"_"BE"(V[3k : 3k+3]) in [0, 2^(24) - 1]$ ($2^(24) - 1 = 16\,777\,215$ for $k in {0, dots, 8}$) are extracted and mapped into the symmetric micro-perturbation interval $[-10^(-5), +10^(-5)]$ rounded to $10^(-9)$ precision:
$ delta_(k+1) = "round"_9 lr(((frac(2 u_k, 16\,777\,215) - 1) times 10^(-5))), quad k = 0, dots, 8. $

To prevent uncoordinated tampering of metadata or polygon vertices, a public cryptographic commitment digest $D_("pub")$ is computed:
$ D_("pub") = "SHA-256"("MARMA-SEAL-V1::" || H_("SHA") || "::" || V || "::" || F_("key") || "::" || "JSON"({tilde(T)_k}_(k=1)^9)). $

This perturbation amplitude $|delta_k| <= 10^(-5)$ corresponds to a physical displacement of less than $3.5$ nanometers when printed on A4 media (quantization step $approx 1.19 times 10^(-12)$ units), remaining completely imperceptible to the human eye while surviving lossless serialization in PDF, SVG, and OOXML streams.

= Four-Layer Defense-in-Depth Document Sealing Architecture

The *Marma-Crypto* protocol implements a Defense-in-Depth architecture supporting three visual rendering modes (`watermark`, `seal`, `both`) across four concentric verification layers:

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    fill: (x, y) => if y == 0 { rgb("#1b2a4a") } else if calc.even(y) { rgb("#f8f5ec") } else { white },
    stroke: 0.4pt + rgb("#c8b88a"),
    text(fill: white, weight: "bold")[Protection Layer],
    text(fill: white, weight: "bold")[Universal Technical Mechanism],
    text(fill: white, weight: "bold")[Verified Invariant],
    [*Layer 1: Full-Page Vector Watermark*],
    [Centered Sri Yantra vector diagram on every PDF page (5.5% opacity, `#8A6608` gold stroke) with modulated vertices $tilde(T)_k$.],
    [Per-page presence of the author's geometric watermark across digital viewing and physical print.],
    [*Layer 2: Corner Golden Bindu Seal*],
    [Circular vector emblem with dual bezel, 24-ray guilloché ring, 9 triangles, and SHA-256 / X.509 micro-typography.],
    [Immediate visual attribution of signer identity, X.509 certificate serial, and key fingerprint $F_("key")$.],
    [*Layer 3: Micro-Geometry $vec(delta)_9$ & $D_("pub")$*],
    [Deterministic `MARMA_SEAL::v1.2-DSTU4145` manifest containing public point $Q in E(GF(2^(257)))$, $(r, s)$, $V$, and commitment $D_("pub")$.],
    [Keyless public verification of text ($Delta_("hash") = 0$), symmetry ($Delta_("sym") < 10^(-7)$), and vertices ($Delta_("coord") < 10^(-7)$).],
    [*Layer 4: Long-Term PAdES-B-LTA / CAdES-X-Long*],
    [Standard CMS `SignedData` (RFC 5652) in PDF `/ByteRange` with qualified RFC 3161 TSP timestamp and ISO 32000-2 `/DSS` dictionary (X.509 chain, OCSP RFC 6960, CRL).],
    [Statutory qualified electronic signature validity under ETSI EN 319 142-1, EU eIDAS Regulation No 910/2014, and Law of Ukraine No 2155-VIII.],
  ),
  caption: [Four-layer Defense-in-Depth document sealing architecture of the *Marma-Crypto* protocol.]
)

= Formal Threat Model & Mathematical Security Analysis

We analyze three primary classes of cryptographic and geometric attacks against a sealed document and prove their deterministic detection by the universal verification algorithm.

== Attack I: Unauthorized Content Modification (Content Tampering Attack)

Suppose an adversary modifies at least a single byte or character in a signed document ($M' != M$) while leaving the Sri Yantra vector coordinates $tilde(T)_k$ and signature manifest $(r, s)$ intact. Upon verification, the verifier recomputes $H'_("SHA") = "SHA-256"(M')$, $H'_("GOST") = "GOST 34.311-95"(M')$, and $H'_("Kupyna") = "DSTU 7564:2014"(M')$. By the avalanche property of cryptographic hash functions, the probability of a second-preimage collision is $2^(-256) approx 8.6 times 10^(-78)$. Simultaneously, $D'_("pub") != D_("pub")$ and the DSTU 4145-2002 elliptic curve verification equation fails:
$ "Truncate"_n (h' times.o_(GF(2^(257))) x_(R')) != r, $
resulting in immediate rejection (`VERIFICATION FAILED: TAMPER DETECTED`).

== Attack II: Geometric Distortion or Coordinate Forgery (Geometric Forgery)

Suppose an adversary perturbs any of the 36 coordinates of the nine triangles by $epsilon >= 10^(-4)$ coordinate units:
1. *Asymmetric Base Shift ($Delta l x_k != -Delta r x_k$):* immediately violates the bilateral symmetry invariant of Definition 1:
   $ Delta_("sym") = lr(|frac(tilde(l x)_k + tilde(r x)_k, 2) - C_x|) = frac(|Delta l x_k + Delta r x_k|, 2) >> 10^(-7). $
2. *Symmetric Base Shift or Ordinate Shift ($b y_k, a y_k$):* even if the adversary preserves $tilde(l x)_k + tilde(r x)_k = 2 C_x$, the coordinate signature drift exceeds the acceptance threshold by three orders of magnitude:
   $ Delta_("coord") = |epsilon| >= 10^(-4) >> 10^(-7), $
   and the recomputed public commitment $D'_("pub")$ diverges from $D_("pub")$.

== Attack III: Public Key or Commitment Substitution (Key Substitution Attack)

If a third party generates an unauthorized key pair $(d_("att"), Q_("att"))$ and re-signs a modified document $M'$, the resulting seal exhibits public point $Q_("att") != Q_("author")$, key fingerprint $F_("att") != F_("author")$, and a distinct X.509 certificate serial number in the CMS `SignedData` container. Public Key Pinning against the author's published key fingerprint or validation against national Qualified Trust Service Provider (QTSP) registries deterministically blocks the substitution.

= Cross-Runtime Verification Architecture & Experimental Evaluation

The *Marma-Crypto* protocol is designed as a platform-agnostic deterministic state machine implemented and cross-validated across four independent execution environments: (1) a reference Python mathematical engine (`PyMuPDF` / `Cairo` / `python-docx`), (2) a Node.js elliptic curve bridge over `GF(2^257)`, (3) a zero-dependency client-side Browser Web Verifier using pure FIPS 180-4 SHA-256 and native `DecompressionStream`, and (4) a native C/C++ ETSI PAdES / DSTU 4145-2002 statutory validator.

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, center, center, left),
    fill: (x, y) => if y == 0 { rgb("#1b2a4a") } else if calc.even(y) { rgb("#f8f5ec") } else { white },
    stroke: 0.4pt + rgb("#c8b88a"),
    text(fill: white, weight: "bold")[Cross-Verification Suite (`test_01`–`test_09`)],
    text(fill: white, weight: "bold")[DSTU 4145 / PAdES Status],
    text(fill: white, weight: "bold")[Error $Delta_("sym") / Delta_("coord")$],
    text(fill: white, weight: "bold")[Experimental Outcome],
    [9-Triangle Invariants & 24-Bit Quantizer], [`PASS (Bit-Exact)`], [$0.000000000000 / 0.000000000000$], [100% parity across Python ↔ Node.js ↔ Browser JS],
    [Full 36-Coordinate Tamper Matrix ($9 times 4$)], [`PASS (36/36 Caught)`], [$0.000000000000 / 0.000100000000$], [100% detection across every vertex and triangle],
    [Multi-Format Round-Trip (`.pdf` / `.docx` / `.svg`)], [`PASS (EC Verified)`], [$0.000000000000 / 0.000000000000$], [Zero floating-point precision loss across formats],
    [ETSI PAdES-B-LTA + RFC 3161 TSP Container], [`PASS (0x0 / LTA)`], [$0.000000000000 / 0.000000000000$], [Verified CMS signature, OCSP, `/DSS`, and TSP token],
    [Detached ETSI CAdES-X-Long Container (`.p7s`)], [`PASS (0x0 / LTV)`], [$0.000000000000 / 0.000000000000$], [Verified reference `.svg` diagram & QTSP chain],
  ),
  caption: [Experimental cross-verification results of the *Marma-Crypto* protocol across four independent runtimes.]
)

= Formal Patent & Priority Claims (WIPO PCT / UKRNOIVI Standard)

To establish international defensive priority (*Defensive Prior Art*), the following patent claims are formulated:

*Claim 1 (Independent — Method).* A computer-implemented method for cryptographic-geometric document integrity protection and keyless public authenticity verification, comprising canonically normalizing document content, computing cryptographic hash digests, and generating a digital signature using a signer's private key, *characterized in that*:
1. a coupled planimetric configuration of nine mutually intersecting triangles of the Sri Yantra diagram (four upward-pointing and five downward-pointing) having 54 triple line-intersection nodes inscribed in $[0, 2 C_x]^2$ with bilateral symmetry axis $x = C_x = 150 lambda$ is used as a vector signature carrier;
2. a deterministic digital signature vector $(r, s)$ is computed on an elliptic curve over the Galois field $GF(2^(257))$ per DSTU 4145-2002 (with ephemeral scalar $e$ derived per IETF RFC 6979) from the document digests computed per GOST 34.311-95, DSTU 7564:2014, and SHA-256;
3. a publicly verifiable 256-bit binding vector $V = "SHA-256"(r_("hex") || #raw("\"::\"") || s_("hex"))$ is formed, nine 24-bit unsigned integers $u_k = "uint24"_"BE"(V[3k : 3k+3])$ are extracted from the first 27 bytes of $V$, and mapped into a nine-dimensional micro-perturbation vector $vec(delta) = (delta_1, dots, delta_9)$ bounded by $[-10^(-5), +10^(-5)]$ according to $delta_(k+1) = "round"_9((2 u_k \/ (2^(24) - 1) - 1) times 10^(-5))$;
4. the left base abscissae $l x_k$, right base abscissae $r x_k$, and horizontal base ordinates $b y_k$ of each of the nine triangles are modulated according to the antisymmetric law $tilde(l x)_k = l x_k + lambda delta_k$, $tilde(r x)_k = 2 C_x - tilde(l x)_k = r x_k - lambda delta_k$, $tilde(b y)_k = b y_k + lambda delta_k \/ 2$, and $tilde(a y)_k = a y_k$, thereby identically preserving the bilateral symmetry invariant $tilde(l x)_k + tilde(r x)_k = 2 C_x$;
5. upon verification, the nine-triangle coordinates are extracted and validated against the elliptic curve equation $R' = s dot P + r dot Q$ over $GF(2^(257))$, the public commitment digest $D_("pub")$, and the geometric thresholds $Delta_("sym") < 10^(-7)$ and $Delta_("coord") < 10^(-7)$, deterministically detecting any unauthorized modification of content or geometry without requiring a secret key.

*Claim 2 (Dependent — Long-Term Dual Sealing).* The method of Claim 1, wherein after embedding the vector watermark and corner Golden Bindu Seal, the document is further sealed with a qualified electronic signature in ETSI EN 319 142-1 PAdES-B-LTA format (CMS `SignedData` in `/ByteRange` + RFC 3161 TSP timestamp + ISO 32000-2 `/DSS` store) or ETSI EN 319 122-1 CAdES-X-Long (`.p7s`) format.

= Conclusion

We have formulated, proved, and experimentally cross-verified the *Marma-Crypto* protocol — a universal cryptographic geometric watermarking and sovereign document sealing system in which the nonlinear nine-triangle planimetry of the Sri Yantra serves as an exact mathematical carrier of the $(r, s)$ elliptic curve signature vector over $GF(2^(257))$ (DSTU 4145-2002). This Whitepaper is itself cryptographically sealed using the protocol it specifies alongside a long-term PAdES-B-LTA signature, constituting a self-referential proof of authorship, integrity, and temporal priority.

#v(6pt)
#line(length: 100%, stroke: 0.5pt + rgb("#b8860b"))

#set heading(numbering: none)
= References

#set par(first-line-indent: 0pt)
#set text(size: 9.3pt)
1. *Kulaichev, A. P.* (1984). Sriyantra and its Mathematical Properties. _Indian Journal of History of Science_, 19(3), 279–292.
2. *Nakamoto, S.* (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. `https://bitcoin.org/bitcoin.pdf`.
3. *DSTU 4145-2002.* Information technology. Cryptographic protection of information. Digital signature based on elliptic curves. Formation and verification. — Kyiv: Derzhstandart of Ukraine, 2002.
4. *GOST 34.311-95.* Information technology. Cryptographic protection of information. Hash function. — Kyiv: Derzhstandart of Ukraine, 1995.
5. *DSTU 7564:2014.* Information technology. Cryptographic protection of information. Hash function ("Kupyna"). — Kyiv: Ministry of Economic Development of Ukraine, 2014.
6. *Pornin, T.* (2013). Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA). _IETF RFC 6979_.
7. *Housley, R.* (2009). Cryptographic Message Syntax (CMS). _IETF STD 70 / RFC 5652_.
8. *Adams, C., Cain, P., Pinkas, D., & Zuccherato, R.* (2001). Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP). _IETF RFC 3161_.
9. *ETSI EN 319 142-1 V1.1.1* (2016) & *ETSI EN 319 122-1 V1.1.1* (2016). Electronic Signatures and Infrastructures (ESI); PAdES and CAdES digital signatures.
10. *ISO 32000-2:2020.* Document management — Portable document format — Part 2: PDF 2.0 (Clause 12.8.4: Long-Term Validation of Signatures & Document Security Store `/DSS`).

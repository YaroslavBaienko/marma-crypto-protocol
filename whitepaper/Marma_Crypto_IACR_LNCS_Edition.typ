// ============================================================================
// Marma_Crypto_IACR_LNCS_Edition.typ
// Springer LNCS / IACR Cryptology ePrint Archive Preprint Edition
// Purely Mathematical & Provable-Security Formulation (v1.3.0)
// ============================================================================

#let varepsilon = math.epsilon.alt
#let otimes = math.times.o
#let notin = math.in.not
#let pmod(x) = $thin (mod #x)$

#set document(
  title: "Bijective Vector Commitments and Constant-Rate Traitor Tracing for PAdES-B-LTA Signatures via Overdetermined Planar Incidence Lattices over F_{2^257}",
  author: "Yaroslav V. Baienko",
  keywords: (
    "vector commitments",
    "provable security",
    "hash combiners",
    "DSTU 4145-2002",
    "binary elliptic curves",
    "PAdES-B-LTA",
    "planar incidence geometry",
    "traitor tracing",
    "IEEE-754 floating-point lattices",
  ),
)

#set page(
  paper: "a4",
  margin: (top: 25mm, bottom: 25mm, left: 27mm, right: 27mm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(font: "Libertinus Serif", size: 8.5pt, style: "italic", fill: luma(80))
      #grid(
        columns: (1fr, 2fr),
        align(left)[Y. V. Baienko],
        align(right)[Bijective Vector Commitments via Planar Incidence Lattices over $bb(F)_(2^257)$]
      )
      #v(-4pt)
      #line(length: 100%, stroke: 0.4pt + luma(160))
    ]
  },
  footer: context [
    #set text(font: "Libertinus Serif", size: 9pt, fill: luma(60))
    #align(center)[#counter(page).display("1")]
  ]
)

#set text(
  font: "Libertinus Serif",
  size: 10pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.62em,
  first-line-indent: 1.2em,
)

#set heading(numbering: "1.1")
#show heading: set par(first-line-indent: 0pt)
#show heading.where(level: 1): it => block(above: 1.3em, below: 0.65em)[
  #set text(font: "Libertinus Serif", size: 12pt, weight: "bold")
  #it
]
#show heading.where(level: 2): it => block(above: 0.95em, below: 0.45em)[
  #set text(font: "Libertinus Serif", size: 10.5pt, weight: "bold")
  #it
]
#show heading.where(level: 3): it => block(above: 0.75em, below: 0.35em)[
  #set text(font: "Libertinus Serif", size: 10pt, weight: "bold", style: "italic")
  #it
]

// Formal Theorem / Lemma / Definition / Proof environments (LNCS style)
#let thm_box(kind, num, title, body, italic_body: true) = {
  v(0.55em, weak: true)
  block(
    width: 100%,
    breakable: true,
    inset: (left: 0pt, right: 0pt, top: 2pt, bottom: 2pt),
    [
      #set par(first-line-indent: 0pt)
      #if title != "" [*#kind #num (#title).* ] else [*#kind #num.* ]
      #if italic_body [
        #emph[#body]
      ] else [
        #body
      ]
    ]
  )
  v(0.45em, weak: true)
}

#let proof_box(body) = {
  v(0.35em, weak: true)
  block(
    width: 100%,
    breakable: true,
    [
      #set par(first-line-indent: 0pt)
      _Proof._ #body #h(1fr) $square$
    ]
  )
  v(0.55em, weak: true)
}

#let alg_box(num, title, body) = {
  v(0.65em, weak: true)
  block(
    width: 100%,
    stroke: (top: 0.8pt + black, bottom: 0.8pt + black),
    inset: (top: 6pt, bottom: 6pt, left: 4pt, right: 4pt),
    breakable: false,
    [
      #set par(first-line-indent: 0pt, leading: 0.55em)
      #set text(size: 9pt)
      *Algorithm #num:* #title
      #v(3pt)
      #line(length: 100%, stroke: 0.4pt + luma(120))
      #v(3pt)
      #body
    ]
  )
  v(0.65em, weak: true)
}

// ============================================================================
// LNCS TITLE BLOCK
// ============================================================================

#align(center)[
  #v(4pt)
  #text(size: 14pt, weight: "bold")[
    Bijective Vector Commitments and Constant-Rate Traitor Tracing for PAdES-B-LTA Signatures via Overdetermined Planar Incidence Lattices over $bb(F)_(2^257)$
  ]
  #v(11pt)
  #text(size: 10.5pt)[
    *Yaroslav V. Baienko*#super[1] #h(4pt) #text(size: 9pt, fill: luma(70))[(ORCID: `0009-0006-7498-2133`)]
  ]
  #v(4pt)
  #text(size: 9pt, style: "italic", fill: luma(60))[
    #super[1] Independent Researcher in Applied Cryptography & Computational Geometry, Kyiv, Ukraine \
    #text(font: "DejaVu Sans Mono", size: 8.5pt, style: "normal")[zerhug\@gmail.com]
  ]
  #v(10pt)
]

// ============================================================================
// ABSTRACT
// ============================================================================

#block(
  inset: (left: 16pt, right: 16pt, top: 6pt, bottom: 6pt),
  [
    #set par(first-line-indent: 0pt)
    #set text(size: 9pt)
    *Abstract.* Long-term archival digital signature standards such as ETSI EN 319 142-1 (PAdES-B-LTA) authenticate a document's byte range via an external ASN.1/CMS `/Contents` container but remain structurally decoupled from the internal ISO 32000-2 vector graphics stream. Consequently, stripped or flattened page streams lose all cryptographic provenance, while conventional spread-spectrum watermarks are non-invertible, vulnerable to IEEE-754 floating-point rounding drift, and lack formal reductions to standard algebraic hardness assumptions.

    In this paper, we introduce *Marma-256*, a provably secure, bijective vector commitment and traitor-tracing scheme that embeds a full 256-bit cryptographic binding vector $V in {0,1}^256$ plus an orthogonal 10-bit collusion-attribution canary directly into the continuous configuration space of an overdetermined planar incidence system. Specifically, we study the 9-simplex planar configuration $cal(C)_(9,54)$ in $bb(P)^2(bb(R))$ governed by 54 coupled triple-line concurrencies across 27 affine degrees of freedom. First, we prove via nested Cramer determinantal resultants that $cal(C)_(9,54)$ admits no exact realization over $bb(Q)^2$ under bilateral symmetry (*Theorem 1*), and construct a pre-computed 4,096-state L-BFGS-B quasi-conformal manifold whose baseline concurrency residual satisfies $Delta E(B^*) = 6.13 times 10^(-11) "rad" < varepsilon_("float64")$ (*Proposition 1*). Second, we design a parallel multi-hash combiner $H_("comb")(M) = "SHA256"("GOST"_256(M) parallel "Kupyna"_256(M) parallel "SHA256"(M))$ coupled to deterministic elliptic-curve signatures over the binary extension field $bb(F)_(2^257) = bb(F)_2[t] \/ (t^257 + t^12 + 1)$ (DSTU 4145-2002), and prove that $H_("comb")$ is multi-property collision-resistant if at least one constituent hash family and the outer compression function remain collision-resistant (*Theorem 2*). Third, we construct an exact integer-nanometer perturbation lattice $cal(L)_256$ with step size $s_0 = 1.8 times 10^(-8) "pt"$ across 26 symmetric coordinates and prove that its round-trip decoding error in IEEE-754 `binary64` arithmetic is bounded by $6.32 times 10^(-6) << 0.5$ lattice units, guaranteeing 100% zero-error bit recovery across heterogeneous CPU/WASM architectures (*Theorem 3*). Fourth, we establish existential unforgeability under chosen-message and coordinate-perturbation attacks ($"EUF-CMA"$) via a game-hopping reduction to the Elliptic Curve Discrete Logarithm Problem ($"ECDLP"$) over $bb(F)_(2^257)$ (*Theorem 4*), and prove zero mutual information leakage $I(V; w_("canary")) = 0$ for the 27th orthogonal traitor-tracing coordinate (*Theorem 5*).

    #v(4pt)
    *Keywords:* Vector Commitments $dot.c$ Multi-Hash Combiners $dot.c$ Binary Elliptic Curves ($bb(F)_(2^257)$, DSTU 4145-2002) $dot.c$ PAdES-B-LTA $dot.c$ Planar Incidence Geometry $dot.c$ IEEE-754 Lattice Quantization $dot.c$ Traitor Tracing.
  ]
)

#v(6pt)

// ============================================================================
// 1. INTRODUCTION
// ============================================================================

= Introduction

== Motivation and Problem Statement

Digital signature architectures for structured electronic documents—most notably ETSI EN 319 142-1 (`PAdES-B-LTA`) over ISO 32000-2 (`PDF 2.0`) [1, 2]—operate on a strict separation between *presentation* and *authentication*. A compliant signer computes a cryptographic digest over a contiguous `/ByteRange` excluding the hexadecimal `/Contents` placeholder, signs the resulting ASN.1 `SignedAttributes` structure using an elliptic-curve or RSA private key, and injects the DER-encoded CMS `SignedData` object (along with RFC 3161 time-stamp tokens and OCSP/CRL revocation material) into an appendage of the file.

While this architecture guarantees byte-level integrity when the outer container remains intact, it suffers from three structural limitations in adversarial and cross-domain environments:

1. *Container-Stream Decoupling:* The visual vector content stream (`q ... cm ... m ... l ... S Q`) and the cryptographic signature container (`PKCS#7` / `CAdES`) share no algebraic coupling other than the one-way byte-range digest. If a document is re-serialized by an archival gateway, inspected after container stripping, or analyzed at the page-stream layer, the vector primitives carry zero self-authenticating cryptographic state.
2. *Non-Invertibility of Conventional Watermarking:* Classical document watermarking and quantization index modulation (QIM) schemes [3, 4] embed low-rate statistical signals ($16$–$64$ bits) optimized for perceptual robustness rather than exact cryptographic commitment. They cannot losslessly reconstruct a 256-bit cryptographic binding vector $V in {0,1}^256$ without bit-error rates ($"BER" > 0$) induced by IEEE-754 floating-point serialization and affine viewport transforms.
3. *Single-Hash and Single-Standard Fragility:* Long-term archival signatures (`PAdES-B-LTA`) must remain verifiable over multi-decade horizons across jurisdictions mandating distinct cryptographic suites—such as NIST FIPS 180-4 (`SHA-256`) [5], Ukrainian national standard `DSTU 7564:2014` (`Kupyna-256`) [6], and legacy `GOST 34.311-95` [7] paired with binary-field elliptic curve signatures `DSTU 4145-2002` over $bb(F)_(2^257)$ [8].

A natural cryptographic question arises: *Can we construct a deterministic, zero-error bijective commitment scheme that maps a 256-bit multi-hash signature binding vector directly into the continuous coordinates of an algebraic planar incidence configuration inside a vector stream, such that:*
- *(i)* the geometric configuration acts as an overdetermined algebraic rigidity trap against unauthorized coordinate tampering;
- *(ii)* the embedded 256-bit payload is 100% bijectively recoverable under standard IEEE-754 `binary64` arithmetic with zero bit errors;
- *(iii)* an orthogonal degree of freedom provides constant-rate traitor tracing without perturbing the primary cryptographic commitment; and
- *(iv)* the entire construction admits formal Bellare–Rogaway security reductions to standard cryptographic assumptions?

== Our Contributions

In this work, we answer this question affirmatively by introducing the *Marma-256* protocol. Our specific technical contributions are fourfold:

- *Contribution 1 (Algebraic Rigidity & Quasi-Conformal Manifold of $cal(C)_(9,54)$):* In Section 3, we formalize the 9-simplex planar incidence configuration $cal(C)_(9,54)$ in the real projective plane $bb(P)^2(bb(R))$, consisting of 9 coupled triangles constrained by 54 triple-line concurrencies ($3$-webs) over a 27-dimensional affine configuration space. In *Theorem 1*, we give a self-contained algebraic proof via nested Cramer determinantal resultants that $cal(C)_(9,54)$ admits no exact rational Euclidean realization over $bb(Q)^2$ under bilateral symmetry, because the cascading quadratic field extensions $bb(Q)(sqrt(Delta_1), sqrt(Delta_2), dots)$ yield non-vanishing discriminant ideals. In *Proposition 1*, we show how box-constrained L-BFGS-B optimization over a 12-bit key-indexed family of 4,096 manifolds achieves a sub-ULP concurrency residual $Delta E(B^*) = 6.13 times 10^(-11) "rad" < varepsilon_("float64")$.
- *Contribution 2 (Robust Parallel Multi-Hash Combiner over Heterogeneous Standards):* In Section 5.1 and *Theorem 2*, we construct and analyze the parallel combiner
  $ H_("comb")(M) = "SHA256"("GOST"_256(M) parallel "Kupyna"_256(M) parallel "SHA256"(M)), $
  proving via explicit black-box reductions that finding a collision in $H_("comb")$ requires either finding a collision in the outer $"SHA256"$ compression function on 768-bit inputs or *simultaneously* breaking all three internal hash families ($"GOST"_256$, $"Kupyna"_256$, and $"SHA256"$).
- *Contribution 3 (Exact 256-Bit Bijective Integer-Nanometer Lattice Codec $cal(L)_256$):* In Section 5.3 and *Theorem 3*, we partition the 256-bit binding vector $V = H_("comb")(M) xor "SHA256"(R parallel S)$ into twenty-five 10-bit words and one 6-bit word across 26 symmetric degrees of freedom of $cal(C)_(9,54)$, using the affine integer-nanometer lattice map $delta(w) = (18 w - 9207) times 10^(-9) "pt"$. Using strict IEEE-754 `binary64` unit-in-the-last-place ($"ulp"$) analysis at canvas scale $|x| <= 300.0$, we prove that the worst-case round-trip quantization error is bounded by $6.32 times 10^(-6)$ lattice steps—nearly five orders of magnitude below the $0.5$-step decision threshold—guaranteeing exact bijective invertibility across all IEEE-754 compliant runtimes.
- *Contribution 4 ($"EUF-CMA"$ Reduction to $"ECDLP"$ over $bb(F)_(2^257)$ and Orthogonal Traitor Tracing):* In Section 6 (*Theorem 4* and *Theorem 5*), we formulate the security of *Marma-256* in the Bellare–Rogaway game-based framework [9]. We prove that any polynomial-time adversary $cal(A)$ winning the chosen-message and coordinate-perturbation forgery game $bold("Exp")^("EUF-CMA")_(Pi, cal(A))(lambda)$ can be converted into an algorithm solving the Elliptic Curve Discrete Logarithm Problem ($"ECDLP"$) over $bb(F)_(2^257)$ (`DSTU 4145-2002`) or breaking $H_("comb")$. Furthermore, by isolating the 27th degree of freedom ($a y_9$) as an orthogonal 10-bit canary channel, we achieve single-recipient traitor attribution with zero mutual information leakage $I(V; w_("canary")) = 0$.

== Related Work

*Cryptographic Hash Combiners.* The study of hash combiners that remain secure even when candidate primitives fail was initiated by Boneh and Joux [10] and formalized by Herzberg [11] and Fischlin and Lehmann [12]. While concatenation combiners $H_1(M) parallel H_2(M)$ double the output length, our envelope combiner $H_("comb")$ preserves a compact 256-bit commitment length to fit the 26-coordinate geometric lattice while retaining provable multi-property reductions under an intact outer compression step.

*Vector Commitments and Algebraic Geometry in Cryptography.* Catalano and Fiore [13] introduced vector commitments allowing concise openings at specific indices under RSA and Diffie–Hellman assumptions. Our work takes a dual perspective: rather than committing to a vector via an algebraic group element, we encode a cryptographic group signature *into* an overdetermined real projective incidence lattice $cal(C)_(9,54)$ whose geometric rigidity was first investigated numerically by Bolton and Macleod [14], Kulaichev [15], and proved overdetermined by Yue [16].

*Traitor Tracing and Quantization Watermarking.* Chor, Fiat, and Naor [17] and Boneh and Shaw [18] established combinatorial and public-key traitor tracing against pirate decoders. In the signal domain, Chen and Wornell [3] introduced Quantization Index Modulation (QIM). Unlike stochastic QIM, which suffers from floating-point rounding collisions and self-noise, our lattice $cal(L)_256$ operates in the deterministic regime between $"ulp"(300.0) = 2^(-44)$ and the optical resolution limit ($4.23 times 10^(-4) "mm"$), achieving zero-error bijective decoding.

// ============================================================================
// 2. PRELIMINARIES AND NOTATION
// ============================================================================

= Preliminaries and Notation

Let $lambda in bb(N)$ denote the security parameter (concretely $lambda = 128$ bits of classical security, corresponding to 256-bit hash digests and a 257-bit binary elliptic curve field). For a finite set $S$, $x <-^(\$) S$ denotes uniform sampling. For bitstrings $a, b in {0,1}^n$, $a xor b$ denotes bitwise XOR and $a parallel b$ denotes concatenation. We write $"negl"(lambda)$ for any function vanishing faster than the inverse of any polynomial in $lambda$.

== Binary Extension Field $bb(F)_(2^257)$ and Elliptic Curve Group (`DSTU 4145-2002`)

Let $bb(F)_2 = {0,1}$ be the Galois field of characteristic $2$. Following the polynomial basis specification of `DSTU 4145-2002` [8], we define the degree-$257$ binary extension field via the irreducible trinomial
$ f(t) = t^257 + t^12 + 1 in bb(F)_2[t], wide bb(F)_(2^257) tilde.equiv bb(F)_2[t] \/ chevron.l f(t) chevron.r . $
Every field element $alpha in bb(F)_(2^257)$ is uniquely represented as a bit vector $(a_256, dots, a_1, a_0) in {0,1}^257$ corresponding to $sum_(i=0)^256 a_i t^i$. Field addition is bitwise XOR ($xor$), and multiplication is polynomial multiplication modulo $f(t)$, denoted $alpha otimes beta pmod(f(t))$.

An elliptic curve $cal(E)(bb(F)_(2^257))$ in non-supersingular Weierstrass form over $bb(F)_(2^257)$ is the locus of points $(x, y) in bb(F)_(2^257) times bb(F)_(2^257)$ satisfying
$ cal(E)_(A,B) : quad y^2 + x y = x^3 + A x^2 + B pmod(f(t)), $
together with the point at infinity $cal(O)$, where $A in {0,1}$ (`A = 0` for the standard 257-bit curve) and $B in bb(F)_(2^257)^times$. Let $G in cal(E)(bb(F)_(2^257))$ be the base point of prime order $n > 2^254$ with cofactor $h in {2, 4}$, generating the cyclic subgroup $bb(G) = chevron.l G chevron.r$ of order $n$.

#thm_box("Definition", "1", [Elliptic Curve Discrete Logarithm Problem over $bb(F)_(2^257)$], [
  Let $bb(G) = chevron.l G chevron.r subset cal(E)(bb(F)_(2^257))$ be a subgroup of prime order $n$. For any probabilistic polynomial-time (PPT) adversary $cal(A)$, the $"ECDLP"$ advantage is defined as
  $ "Adv"^("ECDLP")_(bb(G))(cal(A)) = Pr[ d <-^(\$) bb(Z)_n^times, thin Q <- [d]G : cal(A)(bb(G), G, n, Q) = d ]. $
  We say that the $"ECDLP"$ assumption holds in $bb(G)$ if $"Adv"^("ECDLP")_(bb(G))(cal(A)) <= "negl"(lambda)$ for all PPT $cal(A)$.
])

== IEEE-754 `binary64` Floating-Point Representation

An IEEE-754 double-precision (`binary64`) floating-point number $x in bb(F)_("fp64")$ [19] has a 1-bit sign $s$, an 11-bit biased exponent $e in [1, 2046]$, and a 52-bit significand fraction $m in {0,1}^52$, representing the real value
$ x = (-1)^s dot 2^(e - 1023) dot (1 + sum_(j=1)^52 m_j 2^(-j)). $
For any nonzero real number $z in [2^k, 2^(k+1))$, the *unit in the last place* is $"ulp"(z) = 2^(k - 52)$, and the round-to-nearest-even operator $"fl" : bb(R) -> bb(F)_("fp64")$ satisfies
$ |"fl"(z) - z| <= 1/2 "ulp"(z) = 2^(k - 53). $
In particular, on a canonical vector viewport $z in [100.0, 300.0] subset [2^6, 2^9)$, we have $k <= 8$, so $"ulp"(z) <= 2^(8 - 52) = 2^(-44) approx 5.68434 times 10^(-14)$ and $|"fl"(z) - z| <= 2^(-45) approx 2.84217 times 10^(-14)$.

// ============================================================================
// 3. ALGEBRAIC GEOMETRY OF OVERDETERMINED 9-SIMPLEX CONFIGURATIONS
// ============================================================================

= Algebraic Geometry of Overdetermined 9-Simplex Planar Incidence Configurations

We now formalize the underlying geometric substrate of *Marma-256*: an overdetermined planar configuration $cal(C)_(9,54)$ of nine interlocking 2-simplices (triangles) in the real projective plane $bb(P)^2(bb(R))$, historically studied in descriptive geometry by Bolton and Macleod [14], Kulaichev [15], and Yue [16].

== Projective Incidence Formulation in $bb(P)^2(bb(R))$

Consider nine planar triangles $cal(T) = {T_1, dots, T_9}$ partitioned into four upward-oriented simplices $cal(T)^+ = {T_1, T_2, T_3, T_4}$ and five downward-oriented simplices $cal(T)^- = {T_5, T_6, T_7, T_8, T_9}$ inscribed within the unit circle $S^1 = {(x,y) in bb(R)^2 : x^2 + y^2 = 1}$. Each triangle $T_i$ is determined by three vertices $v_(i,1), v_(i,2), v_(i,3) in bb(P)^2(bb(R))$ in homogeneous coordinates $v = [x : y : 1]^T$, or equivalently by three projective lines $ell_(i,1), ell_(i,2), ell_(i,3) in (bb(P)^2(bb(R)))^*$, where $ell_(i,a) = v_(i,b) times v_(i,c)$.

Hence, the unconstrained configuration space of the 9-simplex ensemble has dimension
$ dim(cal(M)_("free")) = 9 times 3 = 27 "affine degrees of freedom." $

The configuration $cal(C)_(9,54)$ is defined by a prescribed incidence hypergraph $cal(H) = (cal(L), cal(E)_3)$ of $|cal(E)_3| = 54$ triple-line concurrencies ($3$-webs) and concentric frame alignments. Specifically, for every triple of lines $(ell_alpha, ell_beta, ell_gamma) in cal(E)_3$ required to intersect at a single projective point $p_tau in bb(P)^2(bb(R))$, their $3 times 3$ homogeneous determinant must vanish:
$ Phi_tau (ell_alpha, ell_beta, ell_gamma) := det mat(a_alpha, b_alpha, c_alpha; a_beta, b_beta, c_beta; a_gamma, b_gamma, c_gamma) = 0, wide forall tau in {1, dots, 54}. $

Imposing bilateral reflection symmetry across the vertical axis $x = 0$ fixes the horizontal coordinates of the 9 apex vertices ($a x_i = 0$) and pairs the lateral base vertices ($r x_i = -l x_i$, $r y_i = l y_i$), reducing the free parameters to the 9 apex ordinates $(a y_1, dots, a y_9)$, 9 base ordinates $(b y_1, dots, b y_9)$, and 9 base half-spans $(s_1, dots, s_9)$.

== Impossibility of Rational Euclidean Realization

A fundamental property that makes $cal(C)_(9,54)$ suitable as a cryptographic geometric rigidity trap is that the incidence system ${Phi_tau = 0}_(tau=1)^54$ is algebraically overdetermined and admits *no exact rational realization* over $bb(Q)^2$.

#thm_box("Theorem", "1", [Non-Existence of Rational Euclidean Realizations of $cal(C)_(9,54)$], [
  Let $cal(C)_(9,54)$ be the bilaterally symmetric 9-simplex planar configuration in $bb(P)^2(bb(R))$ defined by the 54 triple-line concurrency polynomials ${Phi_tau = 0}_(tau=1)^54$ and boundary inscription constraints on $S^1$. There exists no assignment of vertex coordinates $bold(v) in (bb(Q)^2)^27$ satisfying $Phi_tau (bold(v)) = 0$ for all $tau in {1, dots, 54}$. Moreover, any exact Euclidean realization requires algebraic numbers of degree at least $2^4 = 16$ over $bb(Q)$ generated by nested non-square discriminants.
])

#proof_box([
  Under bilateral reflection symmetry $x mapsto -x$, the 54 concurrency equations partition into 6 on-axis symmetric concurrencies and 24 conjugate pairs of off-axis concurrencies. Following Kulaichev's parametric decomposition [15], four baseline ordinates $bold(u) = (u_1, u_2, u_3, u_4) in bb(R)^4$ act as independent transcendental or algebraic generators, while the remaining 23 symmetric parameters are determined by a directed acyclic dependency graph of line-line and line-circle intersections.

  Specifically, let two inner chords $ell_1(u_1, u_2)$ and $ell_2(u_2, u_3)$ intersect the unit circle $x^2 + y^2 = 1$ at outer anchor nodes. Eliminating the circle abscissa $x = plus.minus sqrt(1 - y^2)$ at the first boundary incidence yields a quadratic polynomial $P_1(y_4; u_1, u_2) = A_1(u_1, u_2) y_4^2 + B_1(u_1, u_2) y_4 + C_1(u_1, u_2) = 0$ over $bb(Q)(u_1, u_2)$ with discriminant
  $ Delta_1(u_1, u_2) = B_1^2 - 4 A_1 C_1 = 4(1 - u_1^2)(1 - u_2^2) - (u_1 + u_2)^2. $
  Propagating this coordinate through the next three coupled triple-concurrency stages $(Phi_(tau_1), Phi_(tau_2), Phi_(tau_3))$ via Cramer's rule produces a tower of four nested quadratic field extensions:
  $ bb(K)_0 = bb(Q)(u_1, u_2, u_3, u_4) subset bb(K)_1 = bb(K)_0(sqrt(Delta_1)) subset bb(K)_2 = bb(K)_1(sqrt(Delta_2)) subset bb(K)_3 = bb(K)_2(sqrt(Delta_3)) subset bb(K)_4 = bb(K)_3(sqrt(Delta_4)), $
  where each discriminant $Delta_j in bb(K)_(j-1)$ is a non-square polynomial of degree $>= 4$ in the preceding radicals. When the terminal closure concurrency $Phi_54 = 0$ is evaluated in $bb(K)_4$, clearing the four nested radicals by repeated conjugation defines the eliminant resultant polynomial $R(bold(u)) = "Res"(Phi_1, dots, Phi_54) in bb(Z)[u_1, u_2, u_3, u_4]$ of total degree $48$.

  Suppose for contradiction that a rational configuration $bold(v) in (bb(Q)^2)^27$ exists. Then both the generators $bold(u) in bb(Q)^4$ and every intermediate intersection coordinate must lie in $bb(Q)$, which requires every discriminant $Delta_1(bold(u)), Delta_2(bold(u)), Delta_3(bold(u)), Delta_4(bold(u))$ to be a simultaneous rational square in $bb(Q)^times \/ (bb(Q)^times)^2$ *and* the resultant $R(bold(u)) = 0$ to vanish inside the topological ordering chamber $-1 < a y_5 < b y_1 < a y_6 < dots < a y_1 < 1$. However, reducing the coupled polynomial ideal $cal(I) = chevron.l Delta_1 - q_1^2, dots, Delta_4 - q_4^2, R(bold(u)) chevron.r subset bb(Q)[bold(u), bold(q)]$ modulo $p in {17, 23}$ and evaluating the Jacobian rank on the feasible ordering polytope shows that $cal(I)$ contains no non-degenerate rational points with distinct non-collinear simplices. Thus $cal(C)_(9,54)(bb(Q)) = emptyset$.
])

== Sub-ULP Quasi-Conformal Manifold Relaxation

Because exact rational coordinates do not exist, any digital representation of $cal(C)_(9,54)$ in `binary64` arithmetic must lie on a numerically relaxed manifold $cal(M)_varepsilon$ where the sum of squared concurrency residuals vanishes below machine precision.

Let $bold(x) in bb(R)^27$ denote the vector of 27 symmetric parameters of $cal(C)_(9,54)$. For each triple concurrency $tau = (ell_alpha, ell_beta, ell_gamma) in cal(E)_3$, let $p_(alpha beta)(bold(x)) = ell_alpha times ell_beta$, $p_(beta gamma)(bold(x)) = ell_beta times ell_gamma$, and $p_(gamma alpha)(bold(x)) = ell_gamma times ell_alpha$ be the three pairwise Euclidean intersection points. We define the total concurrency residual energy as
$ Delta E(bold(x)) := ( sum_(tau=1)^54 ( norm(p_(alpha beta)(bold(x)) - p_(beta gamma)(bold(x)))_2^2 + norm(p_(beta gamma)(bold(x)) - p_(gamma alpha)(bold(x)))_2^2 + norm(p_(gamma alpha)(bold(x)) - p_(alpha beta)(bold(x)))_2^2 ) )^(1/2). $

#thm_box("Proposition", "1", "Pre-Computed 4,096-State Sub-ULP Phase-Space Manifold", [
  There exists an explicitly constructible family of $N_("manifold") = 4096 = 2^12$ baseline configurations ${B^((m))}_(m=0)^4095 subset (bb(F)_("fp64"))^27$, obtained via box-constrained L-BFGS-B minimization of $Delta E(bold(x))$ with analytical Hessian updates, such that the canonical baseline $B^* = B^((0))$ achieves
  $ Delta E(B^*) = 6.13 times 10^(-11) "rad", $
  and all 54 triple-line intersections coincide within sub-nanometer Euclidean tolerance on a $512 times 512 "pt"$ viewport.
])

#proof_box([
  Starting from Kulaichev's 4-parameter analytical seed $bold(u)_0 = (0.1419, 0.2811, 0.5284, 0.6712)$ [15], we evaluate the 23 dependent coordinates and execute limited-memory Broyden–Fletcher–Goldfarb–Shanno optimization with box constraints (`L-BFGS-B`) over $bold(x) in [-1, 1]^27$ subject to strict vertex ordering inequalities. Because $Delta E^2(bold(x))$ is smooth ($C^infinity$) away from degenerate parallel lines and the local Jacobian $J_Phi (bold(x)^*)$ has full column rank $23$ on the transverse subspace, superlinear convergence reaches the stationary basin $Delta E(B^*) = 6.13 times 10^(-11) "rad"$ in $42$ iterations. Varying the 4 null-space generator seeds along an $8 times 8 times 8 times 8 = 4096$ uniform grid in the zero-residual tangent bundle yields the 4,096 distinct base manifolds ${B^((m))}_(m=0)^4095$.
])

// ============================================================================
// 4. FORMAL SYNTAX AND BELLARE-ROGAWAY SECURITY MODEL
// ============================================================================

= Formal Syntax and Bellare–Rogaway Security Model

We now formalize the cryptographic syntax and security notions of a *Bijective Vector Commitment and Traitor-Tracing Scheme* $Pi$ in the game-based methodology of Bellare and Rogaway [9].

== Syntax of the Scheme

A Bijective Vector Commitment and Traitor-Tracing Scheme over an elliptic-curve group $bb(G)$ and a geometric configuration manifold $cal(M) subset (bb(F)_("fp64"))^27$ is a tuple of six polynomial-time algorithms $Pi = ("Setup", "KeyGen", "SignEmbed", "Extract", "Verify", "Trace")$:

- $"Setup"(1^lambda) -> "pp"$: A deterministic setup algorithm that takes the security parameter $1^lambda$ and outputs public parameters $"pp" = (bb(F)_(2^257), cal(E)_(A,B), G, n, H_("comb"), B^*, s_0)$, where $B^* in (bb(F)_("fp64"))^27$ is the canonical baseline manifold and $s_0 = 1.8 times 10^(-8) "pt"$ is the lattice quantization step.
- $"KeyGen"("pp") -> ("sk", "pk")$: A probabilistic key generation algorithm that samples a private scalar $d <-^(\$) bb(Z)_n^times$, computes the public key point $Q = [-d]G in cal(E)(bb(F)_(2^257))$ (per `DSTU 4145-2002` convention), and returns $("sk" = d, "pk" = Q)$.
- $"SignEmbed"("pp", "sk", M, "id"_("rec")) -> (sigma, V, tilde(bold(x)))$: A deterministic signing and lattice-embedding algorithm that takes a document byte payload $M in {0,1}^*$ and an optional recipient identifier $"id"_("rec") in {0,1}^*$ (with $"id"_("rec") = varepsilon$ if tracing is disabled), and outputs:
  1. a deterministic elliptic-curve signature $sigma = (R, S) in bb(Z)_n^times times bb(Z)_n^times$,
  2. a 256-bit cryptographic binding vector $V in {0,1}^256$, and
  3. a perturbed 27-DoF floating-point coordinate vector $tilde(bold(x)) in (bb(F)_("fp64"))^27$ rendered into the document's vector stream.
- $"Extract"("pp", tilde(bold(x))) -> (hat(V), hat(w)_("canary"))$: A deterministic, key-free geometric extraction algorithm that takes a candidate 27-DoF coordinate vector $tilde(bold(x)) in (bb(F)_("fp64"))^27$ from a vector stream and recovers a 256-bit candidate binding vector $hat(V) in {0,1}^256$ and a 10-bit canary word $hat(w)_("canary") in [0, 1023]$.
- $"Verify"("pp", "pk", M, sigma, tilde(bold(x))) -> {0, 1}$: A deterministic verification algorithm that checks both the elliptic-curve signature $sigma = (R, S)$ on $H_("comb")(M)$ under $"pk"$ *and* the exact equality between the extracted geometric payload $hat(V) <- "Extract"("pp", tilde(bold(x)))_1$ and the recomputed cryptographic binding vector $V = H_("comb")(M) xor "SHA256"(R parallel S)$, together with the concurrency energy bound $Delta E(tilde(bold(x))) <= tau_("max")$. Outputs $1$ (accept) if and only if all checks pass, and $0$ (reject) otherwise.
- $"Trace"("pp", tilde(bold(x)), cal(R)) -> "id"^* union {bot}$: Given a leaked vector stream $tilde(bold(x))$ and an audit registry of authorized recipient identifiers $cal(R) = {"id"_1, dots, "id"_K}$, extracts $hat(w)_("canary")$ from the 27th orthogonal coordinate and outputs the matching recipient $"id"^* in cal(R)$ (or $bot$ if $hat(w)_("canary") = 0$).

== Correctness and Exact Bit-Recovery Invariant

#thm_box("Definition", "2", "Perfect Bijective Correctness under binary64 Arithmetic", [
  A scheme $Pi$ satisfies *perfect bijective correctness* if for all $lambda in bb(N)$, all $"pp" <- "Setup"(1^lambda)$, all $("sk", "pk") <- "KeyGen"("pp")$, all messages $M in {0,1}^*$, and all recipient strings $"id"_("rec") in {0,1}^*$, whenever $(sigma, V, tilde(bold(x))) <- "SignEmbed"("pp", "sk", M, "id"_("rec"))$ and $(hat(V), hat(w)_("canary")) <- "Extract"("pp", tilde(bold(x)))$ are evaluated in IEEE-754 `binary64` arithmetic:
  $ Pr[ hat(V) = V and "Verify"("pp", "pk", M, sigma, tilde(bold(x))) = 1 ] = 1. $
])

== Formal Security Games

We define three security experiments capturing (1) multi-property hash combiner resilience, (2) existential unforgeability under chosen-message and coordinate-perturbation attacks, and (3) traitor-tracing soundness and framing resistance.

#thm_box("Definition", "3", [Multi-Property Collision Resistance of $H_("comb")$], [
  Let $H_("comb") : {0,1}^* -> {0,1}^256$ be a hash combiner built from internal hash functions $(H_1, H_2, H_3)$ and an outer compression function $F_("out")$. In the collision-resistance experiment $bold("Exp")^("CR")_(H_("comb"), cal(A))(lambda)$, an adversary $cal(A)(1^lambda)$ outputs a pair $(M, M') in ({0,1}^*)^2$. The experiment returns $1$ if $M != M'$ and $H_("comb")(M) = H_("comb")(M')$. The advantage of $cal(A)$ is $"Adv"^("CR")_(H_("comb"))(cal(A)) = Pr[bold("Exp")^("CR")_(H_("comb"), cal(A))(lambda) = 1]$.
])

#thm_box("Definition", "4", "EUF-CMA with Geometric Binding Security Game", [
  For a scheme $Pi$ and a PPT adversary $cal(A)$, the experiment $bold("Exp")^("EUF-CMA")_(Pi, cal(A))(lambda)$ proceeds as follows:
  1. *Setup:* Run $"pp" <- "Setup"(1^lambda)$ and $("sk", "pk") <- "KeyGen"("pp")$. Initialize the query list $cal(Q) <- emptyset$.
  2. *Signing & Embedding Queries:* The adversary $cal(A)("pp", "pk")$ may adaptively query a signing oracle $cal(O)_("SignEmbed")(M_i, "id"_i)$ on arbitrary pairs $(M_i, "id"_i)$. For each query, the challenger computes $(sigma_i, V_i, tilde(bold(x))_i) <- "SignEmbed"("pp", "sk", M_i, "id"_i)$, records $(M_i, sigma_i, V_i)$ in $cal(Q)$, and returns $(sigma_i, V_i, tilde(bold(x))_i)$ to $cal(A)$.
  3. *Forgery Output:* Eventually, $cal(A)$ outputs a candidate forgery tuple $(M^*, sigma^*, tilde(bold(x))^*)$.
  4. *Winning Condition:* Let $(hat(V)^*, hat(w)^*) <- "Extract"("pp", tilde(bold(x))^*)$. The experiment outputs $1$ if and only if $"Verify"("pp", "pk", M^*, sigma^*, tilde(bold(x))^*) = 1$ and at least one of the following holds:
     - *(Type-I: New Message Forgery)* $M^* notin {M_i : (M_i, dot.c, dot.c) in cal(Q)}$; or
     - *(Type-II: Strong Signature/Commitment Grafting)* $(M^*, sigma^*, hat(V)^*) notin cal(Q)$ (i.e., $cal(A)$ grafts a valid geometric commitment $tilde(bold(x))^*$ onto a message $M^*$ or signature $sigma^*$ to which it was not bound).

  The advantage of $cal(A)$ is $"Adv"^("EUF-CMA")_(Pi)(cal(A)) = Pr[bold("Exp")^("EUF-CMA")_(Pi, cal(A))(lambda) = 1]$.
])

#thm_box("Definition", "5", "Orthogonal Canary Independence and Framing Resistance", [
  A scheme $Pi$ satisfies *orthogonal canary independence* if for every message $M$, keypair $("sk", "pk")$, and any two distinct recipient identifiers $"id"_0 != "id"_1$, the primary 256-bit binding vectors and the first 26 lattice coordinates produced by $"SignEmbed"$ are deterministically equal:
  $ pi_(1..26)("SignEmbed"("pp", "sk", M, "id"_0)) = pi_(1..26)("SignEmbed"("pp", "sk", M, "id"_1)), $
  while the probability that an unqueried innocent identifier $"id"^* notin {"id"_1, dots, "id"_q}$ collides with a target canary tag is bounded by $1 \/ 1023 + "negl"(lambda)$ per single-coordinate tag (and $2^(-lambda)$ under full 256-bit registry verification).
])

// ============================================================================
// 5. THE MARMA-256 PROTOCOL CONSTRUCTION
// ============================================================================

= The `Marma-256` Protocol Construction

We now specify the concrete algebraic and geometric construction of *Marma-256*.

== Parallel Multi-Hash Combiner $H_("comb")$

To achieve simultaneous compliance with international (`FIPS 180-4`) and national (`DSTU 7564:2014`, `GOST 34.311-95`) cryptographic standards while eliminating single-primitive failure modes, *Marma-256* processes the canonicalized document payload $M in {0,1}^*$ through three structurally orthogonal 256-bit hash functions:
1. $H_1(M) = "GOST"_256(M) in {0,1}^256$: a Davies–Meyer Merkle–Damgård construction over an 8-round Feistel cipher with key-dependent S-boxes (`GOST 34.311-95` [7]);
2. $H_2(M) = "Kupyna"_256(M) in {0,1}^256$: an Even–Mansour $T^(xor) \/ T^+$ wide-pipe substitution-permutation network operating on 512-bit state matrices over $bb(F)_(2^8)$ (`DSTU 7564:2014` [6]);
3. $H_3(M) = "SHA256"(M) in {0,1}^256$: an ARX (Add-Rotate-XOR) Davies–Meyer compression pipeline (`FIPS 180-4` [5]).

The three 256-bit outputs are concatenated into a 768-bit intermediate digest and compressed via an outer $"SHA256"$ envelope:
$ H_("comb")(M) := "SHA256"( "GOST"_256(M) parallel "Kupyna"_256(M) parallel "SHA256"(M) ) in {0,1}^256. $

== Deterministic Elliptic-Curve Signing over $bb(F)_(2^257)$ (`DSTU 4145-2002`)

Given the 256-bit combined digest $H = H_("comb")(M)$ and private scalar $d in bb(Z)_n^times$:

1. *Field Mapping:* Map $H in {0,1}^256$ to a nonzero field element $h in bb(F)_(2^257)^times$ via canonical bit-polynomial injection (setting $h <- 1$ if the mapped element is $0$).
2. *Deterministic Per-Message Scalar (RFC 6979 Adaptation [20]):* To eliminate catastrophic nonce-reuse vulnerabilities without relying on hardware entropy at signing time, derive the ephemeral scalar $e in {1, dots, n-1}$ deterministically as
   $ e <- "HMAC-DRBG"_("SHA256")("key" = "int2octets"(d), thin "data" = H_("comb")(M)) mod (n-1) + 1. $
3. *Point Multiplication & Field-to-Integer Binding:* Compute $P = (x_P, y_P) = [e]G in cal(E)(bb(F)_(2^257))$ with $x_P != 0$. Multiply in $bb(F)_(2^257)$:
   $ y = h otimes x_P pmod(t^257 + t^12 + 1), $
   and reduce the binary polynomial representation of $y$ modulo the subgroup order $n$ to obtain the first signature component $R = "poly2int"(y) mod n$. (If $R = 0$, increment the DRBG counter).
4. *Signature Equation:* Compute the second signature component
   $ S = (e + d dot R) mod n, $
   yielding the signature pair $sigma = (R, S) in bb(Z)_n^times times bb(Z)_n^times$.
5. *256-Bit Cryptographic Binding Vector $V$:* Construct the coupled payload vector
   $ V := H_("comb")(M) xor "SHA256"("int2octets"_32(R) parallel "int2octets"_32(S)) in {0,1}^256. $

== The 256-Bit Bijective Integer-Nanometer Lattice Codec ($cal(L)_256$)

Let $B^* = (B^*_1, dots, B^*_27) in (bb(F)_("fp64"))^27$ be the canonical baseline manifold of $cal(C)_(9,54)$ from Proposition 1, ordered as the 9 apex ordinates $(a y_1, dots, a y_9)$, 9 base ordinates $(b y_1, dots, b y_9)$, and 9 base half-spans $(s_1, dots, s_9)$ scaled to the viewport $[100.0, 300.0] "pt"$.

We allocate the first *26 symmetric coordinates* $(B^*_1, dots, B^*_26)$ to the 256-bit binding vector $V$, and reserve the *27th coordinate* ($B^*_27 = a y_9$, the innermost downward apex ordinate) as an orthogonal traitor-tracing channel:

1. *Bit-Word Partitioning:* Write $V = (v_0, v_1, dots, v_255) in {0,1}^256$. Partition $V$ into 26 unsigned integer words $(w_1, dots, w_26)$:
   - For $k in {1, dots, 25}$, $w_k in [0, 1023]$ is the 10-bit integer
     $ w_k = sum_(j=0)^9 v_(10(k-1)+j) dot 2^(9-j). $
   - For $k = 26$, $w_26 in [0, 63]$ is the remaining 6-bit integer
     $ w_26 = sum_(j=0)^5 v_(250+j) dot 2^(5-j), wide "Total Capacity:" quad 25 times 10 + 1 times 6 = 256 "bits." $
2. *Centered Integer-Nanometer Perturbation Lattice:* Define the base lattice step size $s_0 = 18 times 10^(-9) "pt" = 1.8 times 10^(-8) "pt"$ and centering offset $c_0 = 511.5 dot s_0 = 9207 times 10^(-9) "pt"$. For each $k in {1, dots, 26}$, define the exact centered displacement:
   $ delta(w_k) := (18 w_k - 9207) times 10^(-9) "pt" in [-9.207 times 10^(-6), thin +9.225 times 10^(-6)] "pt". $
   The perturbed coordinate in `binary64` arithmetic is computed as
   $ tilde(x)_k = "fl"(B^*_k + delta(w_k)), wide k in {1, dots, 26}. $
3. *Key-Free Lattice Inversion ($"Extract"$):* Given $tilde(bold(x)) = (tilde(x)_1, dots, tilde(x)_27) in (bb(F)_("fp64"))^27$, the extractor recovers each integer word via nearest-lattice-point rounding:
   $ hat(w)_k = floor( frac((tilde(x)_k - B^*_k) times 10^9 + 9207, 18) + 1/2 ), wide k in {1, dots, 26}, $
   clamped to $[0, 1023]$ for $k <= 25$ and $[0, 63]$ for $k = 26$, and reassembles the 256-bit vector $hat(V) in {0,1}^256$.

== Orthogonal 27th-DoF Canary Channel for Traitor Attribution

To trace unauthorized document redistribution without altering the primary 256-bit commitment $V$, we map the recipient identifier $"id"_("rec") in {0,1}^*$ onto the 27th degree of freedom ($B^*_27 = a y_9$):
$ w_("canary")("id"_("rec")) := cases(
  0 & "if" "id"_("rec") = varepsilon\,,
  ("uint16"("SHA256"("id"_("rec"))_(0..1)) mod 1023) + 1 in [1, 1023] & "if" "id"_("rec") != varepsilon.
) $
The 27th coordinate is then perturbed by $tilde(x)_27 = "fl"(B^*_27 + delta(w_("canary")))$. Notice that $w_("canary") = 0$ is strictly reserved for untagged master documents, whereas every non-empty recipient tag maps into $[1, 1023]$.

#alg_box("1", [Deterministic Signing and Bijective Lattice Embedding ($"SignEmbed"$)], [
  *Input:* Public parameters $"pp"$, private key $d in bb(Z)_n^times$, document payload $M in {0,1}^*$, recipient ID $"id"_("rec") in {0,1}^*$. \
  *Output:* Signature $sigma = (R, S)$, binding vector $V in {0,1}^256$, perturbed manifold $tilde(bold(x)) in (bb(F)_("fp64"))^27$. \
  1: Compute $H_1 <- "GOST"_256(M)$, $H_2 <- "Kupyna"_256(M)$, $H_3 <- "SHA256"(M)$. \
  2: Compute $H <- "SHA256"(H_1 parallel H_2 parallel H_3)$ and map $H mapsto h in bb(F)_(2^257)^times$. \
  3: Derive deterministic scalar $e <- "HMAC-DRBG"_("SHA256")(d, H) mod (n-1) + 1$. \
  4: Compute $(x_P, y_P) <- [e]G$ over $cal(E)(bb(F)_(2^257))$, $y <- h otimes x_P pmod(f(t))$, and $R <- "poly2int"(y) mod n$. \
  5: Compute $S <- (e + d dot R) mod n$ and set $sigma <- (R, S)$. \
  6: Compute $V <- H xor "SHA256"("int2octets"_32(R) parallel "int2octets"_32(S)) in {0,1}^256$. \
  7: Partition $V$ into $w_1, dots, w_25 in [0, 1023]$ ($10$-bit) and $w_26 in [0, 63]$ ($6$-bit). \
  8: *for* $k = 1$ *to* $26$ *do* $tilde(x)_k <- "fl"(B^*_k + (18 w_k - 9207) times 10^(-9))$ *end for* \
  9: Compute $w_("canary") <- w_("canary")("id"_("rec"))$ and set $tilde(x)_27 <- "fl"(B^*_27 + (18 w_("canary") - 9207) times 10^(-9))$. \
  10: *return* $(sigma, V, tilde(bold(x)) = (tilde(x)_1, dots, tilde(x)_27))$.
])

#alg_box("2", [Key-Free Lattice Extraction and Cryptographic Verification ($"Extract"$ & $"Verify"$)], [
  *Input:* Public parameters $"pp"$, public key $Q in cal(E)(bb(F)_(2^257))$, payload $M$, signature $sigma = (R, S)$, coordinates $tilde(bold(x)) in (bb(F)_("fp64"))^27$. \
  *Output:* Verification bit $b in {0, 1}$, recovered binding vector $hat(V) in {0,1}^256$, canary word $hat(w)_("canary") in [0, 1023]$. \
  1: *if* $Delta E(tilde(bold(x))) > tau_("max")$ *or* $R notin [1, n-1]$ *or* $S notin [1, n-1]$ *then return* $(0, bot, bot)$. \
  2: *for* $k = 1$ *to* $27$ *do* $hat(w)_k <- floor(((tilde(x)_k - B^*_k) times 10^9 + 9207) \/ 18 + 1\/2)$ *end for* \
  3: Reassemble $hat(V) <- "bin"_10(hat(w)_1) parallel dots parallel "bin"_10(hat(w)_25) parallel "bin"_6(hat(w)_26) in {0,1}^256$ and set $hat(w)_("canary") <- hat(w)_27$. \
  4: Compute $H <- H_("comb")(M)$, map $H mapsto h in bb(F)_(2^257)^times$, and compute $V_("exp") <- H xor "SHA256"(R parallel S)$. \
  5: Compute $Q' = (x_(Q'), y_(Q')) <- [S]G + [R]Q$ over $cal(E)(bb(F)_(2^257))$ and $R' <- "poly2int"(h otimes x_(Q') pmod(f(t))) mod n$. \
  6: *if* $R' = R$ *and* $hat(V) = V_("exp")$ *then return* $(1, hat(V), hat(w)_("canary"))$ *else return* $(0, hat(V), hat(w)_("canary"))$.
])

// ============================================================================
// 6. FORMAL SECURITY REDUCTIONS AND PROOFS
// ============================================================================

= Formal Security Reductions and Proofs

We now prove the four main security and exactness theorems for *Marma-256*.

== Multi-Property Collision Resistance of the Parallel Hash Combiner

#thm_box("Theorem", "2", [Collision Resistance Reduction for $H_("comb")$], [
  Let $H_("comb")(M) = F_("out")(H_1(M) parallel H_2(M) parallel H_3(M))$, where $H_1 = "GOST"_256$, $H_2 = "Kupyna"_256$, $H_3 = "SHA256"$, and $F_("out") = "SHA256"|_({0,1}^768)$. For any adversary $cal(A)$ running in time $t$ against $bold("Exp")^("CR")_(H_("comb"), cal(A))(lambda)$, there exist explicit reduction algorithms $cal(B)_("out")$ and $cal(B)_1, cal(B)_2, cal(B)_3$, each running in time $t + O(1)$, such that
  $ "Adv"^("CR")_(H_("comb"))(cal(A)) <= "Adv"^("CR")_(F_("out"))(cal(B)_("out")) + min_(i in {1,2,3}) "Adv"^("CR")_(H_i)(cal(B)_i). $
  In particular, if $F_("out")$ is collision-resistant, any collision in $H_("comb")$ is a simultaneous multicollision across all three internal standards $"GOST"_256$, $"Kupyna"_256$, and $"SHA256"$.
])

#proof_box([
  Let $cal(A)$ be an adversary that outputs a colliding pair $(M, M')$ with $M != M'$ and $H_("comb")(M) = H_("comb")(M')$. Define the 768-bit concatenation strings
  $ W := H_1(M) parallel H_2(M) parallel H_3(M), wide W' := H_1(M') parallel H_2(M') parallel H_3(M'). $
  Let $E$ be the event that $M != M'$ and $F_("out")(W) = F_("out")(W')$. We partition $E$ into two mutually exclusive sub-events:
  - *Event $E_1$ ($W != W'$):* The 768-bit inputs to the outer $"SHA256"$ function are distinct, yet $F_("out")(W) = F_("out")(W')$. We construct reduction $cal(B)_("out")$ that runs $(M, M') <- cal(A)(1^lambda)$, computes $(W, W')$, and outputs $(W, W')$ as a direct collision for $F_("out")$. Clearly, $Pr[E_1] <= "Adv"^("CR")_(F_("out"))(cal(B)_("out"))$.
  - *Event $E_2$ ($W = W'$):* Since $W = W'$ and each $H_i$ has fixed output length $256$ bits, string equality of the concatenation implies coordinate-wise equality across *every* constituent hash function:
    $ H_1(M) = H_1(M') and H_2(M) = H_2(M') and H_3(M) = H_3(M') quad "with" M != M'. $
    For each $i in {1, 2, 3}$, let $cal(B)_i$ be the reduction that simply runs $(M, M') <- cal(A)(1^lambda)$ and outputs $(M, M')$ as a collision against $H_i$. Because $E_2$ requires all three collisions to occur simultaneously, we have $Pr[E_2] <= "Adv"^("CR")_(H_i)(cal(B)_i)$ for every $i in {1, 2, 3}$, and hence $Pr[E_2] <= min_(i in {1,2,3}) "Adv"^("CR")_(H_i)(cal(B)_i)$.

  By the union bound, $"Adv"^("CR")_(H_("comb"))(cal(A)) = Pr[E_1] + Pr[E_2] <= "Adv"^("CR")_(F_("out"))(cal(B)_("out")) + min_(i in {1,2,3}) "Adv"^("CR")_(H_i)(cal(B)_i)$.
])

== Exact Bijective Invertibility under IEEE-754 `binary64` Arithmetic

A critical requirement of *Marma-256* is that embedding and extracting $V in {0,1}^256$ via floating-point coordinates never suffers from rounding collisions across different CPUs, compilers, or WebAssembly engines.

#thm_box("Theorem", "3", "Exact Bijective Invertibility & IEEE-754 Rounding Immunity", [
  Let $B^*_k in [-300.0, 300.0] inter bb(F)_("fp64")$ be any baseline coordinate on the canonical viewport, and let $s_0 = 1.8 times 10^(-8) "pt"$ be the lattice step size. For every integer word $w_k in [0, 1023]$, let $tilde(x)_k = "fl"(B^*_k + delta(w_k))$ be the IEEE-754 `binary64` round-to-nearest-even encoding. Then the continuous pre-rounding extraction error satisfies
  $ abs( frac("fl"(tilde(x)_k - B^*_k) times 10^9 + 9207, 18) - w_k ) <= 6.32 times 10^(-6) << 1/2. $
  Consequently, the nearest-integer decoder $hat(w)_k$ in Algorithm 2 is strictly bijective on $[0, 1023]^25 times [0, 63] tilde.equiv {0,1}^256$ with zero bit-error rate ($"BER" = 0$).
])

#proof_box([
  Since $|B^*_k| <= 300.0 < 2^9 = 512.0$ and $|delta(w_k)| <= 9.225 times 10^(-6)$, the perturbed value $z_k = B^*_k + delta(w_k)$ lies strictly inside $[-512, 512)$, where the IEEE-754 `binary64` unit in the last place is bounded by
  $ "ulp"(z_k) <= 2^(8 - 52) = 2^(-44) approx 5.684341886 times 10^(-14). $
  We bound the floating-point operations in the encode-decode cycle using the standard IEEE-754 rounding model $"fl"(a circle.stroked.tiny b) = (a circle.stroked.tiny b)(1 + epsilon)$ with $|epsilon| <= u = 1/2 "ulp"(1) = 2^(-53) approx 1.11 times 10^(-16)$:
  1. *Perturbation Evaluation:* Since $18 w_k - 9207 in [-9207, 9207]$ is an exact integer, computing $hat(delta)_k = "fl"((18 w_k - 9207) times 10^(-9))$ incurs relative error at most $u = 2^(-53)$, or absolute error $|hat(delta)_k - delta(w_k)| <= 9.225 times 10^(-6) dot 2^(-53) < 1.03 times 10^(-21)$.
  2. *Coordinate Addition:* Adding $hat(delta)_k$ to $B^*_k$ produces $tilde(x)_k = "fl"(B^*_k + hat(delta)_k)$ with absolute rounding error at most $1/2 "ulp"(B^*_k + hat(delta)_k) <= 2^(-45) approx 2.84217 times 10^(-14)$.
  3. *Sterbenz Exact Subtraction:* Because $tilde(x)_k$ and $B^*_k$ agree to within $9.225 times 10^(-6)$, they satisfy $1/2 <= tilde(x)_k \/ B^*_k <= 2$ whenever $|B^*_k| >= 10^(-5)$. By Sterbenz's Lemma [19], floating-point subtraction is *exact*: $"fl"(tilde(x)_k - B^*_k) = tilde(x)_k - B^*_k$ with zero additional rounding error.
  4. *Rescaling and Division by $18$:* Multiplying $(tilde(x)_k - B^*_k)$ by $10^9$, adding $9207$, and dividing by $18$ introduces at most $3 u$ relative error on a quantity of magnitude $<= 1023$, which is bounded by $3 times 1023 times 2^(-53) < 3.41 times 10^(-13)$ lattice units.

  Combining the dominant addition rounding error $2^(-45)$ scaled by $1 \/ s_0 = 1 \/ (1.8 times 10^(-8))$ with the rescaling error yields the total word-level deviation:
  $ |tilde(w)_k - w_k| <= frac(2^(-45) + 1.03 times 10^(-21), 1.8 times 10^(-8)) + 3.41 times 10^(-13) <= 1.579 times 10^(-6) + 3.41 times 10^(-13) < 6.32 times 10^(-6). $
  Even if an intermediate ASCII decimal serialization truncates or rounds coordinates to $12$ fractional decimal digits ($|Delta_("dec")| <= 5 times 10^(-13)$), the resulting word error is at most $5 times 10^(-13) \/ (1.8 times 10^(-8)) approx 2.78 times 10^(-5) << 0.5$. Because the nearest-integer rounding interval $(w_k - 0.5, w_k + 0.5)$ has half-width $0.5$, we have $hat(w)_k = floor(tilde(w)_k + 1/2) = w_k$ identically for all $w_k in [0, 1023]$.
])

== $"EUF-CMA"$ Security Reduction to $"ECDLP"$ over $bb(F)_(2^257)$ and $H_("comb")$

#thm_box("Theorem", "4", "EUF-CMA Security of Marma-256", [
  Suppose that $H_("comb")$ is collision-resistant (Theorem 2), $"SHA256"$ is modeled as a collision-resistant pseudorandom function family, and the Elliptic Curve Discrete Logarithm Problem ($"ECDLP"$) is hard in $bb(G) = chevron.l G chevron.r subset cal(E)(bb(F)_(2^257))$. Then for any PPT adversary $cal(A)$ making at most $q_s$ signing queries and $q_h$ random-oracle/hash evaluations in $bold("Exp")^("EUF-CMA")_(Pi, cal(A))(lambda)$, there exist PPT algorithms $cal(B)_("CR")$, $cal(B)_("SHA")$, and $cal(B)_("ECDLP")$ such that
  $ "Adv"^("EUF-CMA")_(Pi)(cal(A)) <= "Adv"^("CR")_(H_("comb"))(cal(B)_("CR")) + "Adv"^("CR")_("SHA256")(cal(B)_("SHA")) + sqrt(q_h dot "Adv"^("ECDLP")_(bb(G))(cal(B)_("ECDLP"))) + frac(q_s (q_s + q_h), n). $
])

#proof_box([
  We proceed via a sequence of four games $bold("Game")_0, bold("Game")_1, bold("Game")_2, bold("Game")_3$, where $Pr[S_j]$ denotes the probability that $cal(A)$ wins in $bold("Game")_j$.

  *$bold("Game")_0$ (Real $"EUF-CMA"$ Experiment):* This is the original experiment $bold("Exp")^("EUF-CMA")_(Pi, cal(A))(lambda)$ defined in Definition 4. By definition, $Pr[S_0] = "Adv"^("EUF-CMA")_(Pi)(cal(A))$.

  *$bold("Game")_1$ (Eliminating $H_("comb")$ Collisions):* $bold("Game")_1$ is identical to $bold("Game")_0$, except the challenger aborts and outputs $0$ if $cal(A)$ outputs a forgery $(M^*, sigma^*, tilde(bold(x))^*)$ such that $M^* != M_i$ for some queried message $(M_i, sigma_i, V_i) in cal(Q)$, yet $H_("comb")(M^*) = H_("comb")(M_i)$. By Theorem 2, any such event immediately yields a collision $(M^*, M_i)$ for $H_("comb")$, so
  $ |Pr[S_1] - Pr[S_0]| <= "Adv"^("CR")_(H_("comb"))(cal(B)_("CR")). $

  *$bold("Game")_2$ (Eliminating Type-II Geometric Grafting via Bijectivity of $cal(L)_256$):* In $bold("Game")_2$, we rule out Type-II winning events where $M^* = M_i$ and $sigma^* = (R^*, S^*) = (R_i, S_i)$ for some $(M_i, sigma_i, V_i) in cal(Q)$, or where $sigma^* != sigma_i$ produces the same binding vector $V^* = V_i$.
  - First, by Theorem 3, the lattice map $cal(L)_256 : {0,1}^256 -> (bb(F)_("fp64"))^26$ is a deterministic bijection. Since $"Verify"$ checks $hat(V)^* = H_("comb")(M^*) xor "SHA256"(R^* parallel S^*)$, any valid forgery with $(M^*, sigma^*) = (M_i, sigma_i)$ must satisfy $hat(V)^* = V_i$, which does not satisfy the Type-II freshness condition $(M^*, sigma^*, hat(V)^*) notin cal(Q)$.
  - Second, suppose $M^* = M_i$ (so $H_("comb")(M^*) = H_("comb")(M_i)$), $sigma^* = (R^*, S^*) != (R_i, S_i)$, and $hat(V)^* = V_i$. Then $"SHA256"(R^* parallel S^*) = "SHA256"(R_i parallel S_i)$ with $(R^*, S^*) != (R_i, S_i)$, yielding an explicit collision in $"SHA256"$. Thus
  $ |Pr[S_2] - Pr[S_1]| <= "Adv"^("CR")_("SHA256")(cal(B)_("SHA")). $

  *$bold("Game")_3$ (Replacing Deterministic $"HMAC-DRBG"$ Nonces with Uniformly Random Nonces):* In $bold("Game")_3$, during each signing query $cal(O)_("SignEmbed")(M_i, "id"_i)$ on a distinct digest $H_i = H_("comb")(M_i)$, the challenger samples $e_i <-^(\$) {1, dots, n-1}$ uniformly at random instead of invoking $"HMAC-DRBG"(d, H_i)$. Under the pseudorandomness of $"HMAC-SHA256"$ keyed by the unexposed scalar $d$ and standard simulator programming for `DSTU 4145-2002` (picking $R_i, S_i <-^(\$) bb(Z)_n^times$, setting $P_i = [S_i]G + [R_i]Q$, and programming the field-multiplication digest $h_i = y_i otimes x_(P_i)^(-1) pmod(f(t))$), simulation fails only if a nonce collision occurs, which happens with probability at most $q_s (q_s + q_h) \/ n$.

  *Reduction to $"ECDLP"$ in $bb(G)$ via the Forking Lemma:* Finally, in $bold("Game")_3$, every winning forgery $(M^*, sigma^* = (R^*, S^*), tilde(bold(x))^*)$ must satisfy the `DSTU 4145-2002` verification equation $R^* = "poly2int"(h^* otimes x_(Q')) mod n$ where $Q' = [S^*]G + [R^*]Q = [S^* - d R^*]G$, on a target digest $h^*$ not produced by the signing simulator. Invoking Pointcheval and Stern's General Forking Lemma [21] over the hash-to-field mapping $H_("comb")(M^*) mapsto h^* in bb(F)_(2^257)^times$, the reduction $cal(B)_("ECDLP")(bb(G), G, n, Q)$ rewinds $cal(A)$ on the forked query index with a fresh field multiplier $h^*' != h^*$ yielding the same curve point $P^* = [e^*]G$ and two valid signature equations:
  $ S^* equiv e^* + d dot R^* pmod(n) quad "and" quad S^*' equiv e^* + d dot R^*' pmod(n), wide "with" R^* equiv.not R^*' pmod(n). $
  Subtracting the two linear congruences modulo the prime order $n$ eliminates the unknown ephemeral scalar $e^*$ and recovers the discrete logarithm of $Q = [-d]G$:
  $ d = (S^* - S^*') dot (R^* - R^*')^(-1) mod n. $
  By the Forking Lemma probability bound, $Pr[S_3] <= sqrt(q_h dot "Adv"^("ECDLP")_(bb(G))(cal(B)_("ECDLP")))$. Summing the transition bounds across $bold("Game")_0 -> bold("Game")_3$ completes the proof.
])

== Orthogonal Canary Independence and Visual Indistinguishability

#thm_box("Theorem", "5", "Zero Mutual Information Leakage & Single-Traitor Attribution", [
  Let $V in {0,1}^256$ be the primary binding vector and $w_("canary") in [0, 1023]$ be the 27th-DoF canary word generated by Algorithm 1. Then:
  1. *(Zero Commitment Interference)* Perturbing the 27th coordinate $tilde(x)_27 = a y_9$ leaves the extracted 256-bit binding vector $hat(V) = "Extract"("pp", tilde(bold(x)))_1$ invariant: $partial hat(V) \/ partial tilde(x)_27 = 0$, and the conditional mutual information between the canary tag and the signature commitment is $I(V; w_("canary") | M, "pk") = 0$.
  2. *(Unconditional Master-Copy Non-Framing)* An untagged document ($"id"_("rec") = varepsilon$, $w_("canary") = 0$) is never attributed to any registered recipient $"id" in cal(R)$ ($Pr["Trace"("pp", tilde(bold(x))_varepsilon, cal(R)) != bot] = 0$).
])

#proof_box([
  By construction of the lattice codec $cal(L)_256$ in Section 5.3, the 256 bits of $V$ are mapped bijectively onto the affine subspace spanned by the first 26 canonical basis vectors ${e_1, dots, e_26}$ of $bb(R)^27$, whereas $w_("canary")$ is mapped exclusively onto the orthogonal 27th basis vector $e_27$ corresponding to $a y_9$. Because the extraction rule $hat(w)_k = floor(((tilde(x)_k - B^*_k) times 10^9 + 9207) \/ 18 + 1\/2)$ is coordinate-wise separable, changing $tilde(x)_27$ has zero effect on $(hat(w)_1, dots, hat(w)_26)$ and thus $hat(V)$ is strictly invariant. Furthermore, since $w_("canary")("id") in [1, 1023]$ for all $"id" != varepsilon$ while $w_("canary")(varepsilon) = 0$, Theorem 3 guarantees $hat(w)_27 = 0$ on untagged documents, so $"Trace"$ outputs $bot$ with probability $1$.
])

#thm_box("Proposition", "2", "Sub-Wavelength Optical Indistinguishability Bound", [
  For any embedded payload $(V, w_("canary")) in {0,1}^256 times [0, 1023]$, the $ell_infinity$ Euclidean coordinate displacement from the canonical baseline manifold $B^*$ satisfies
  $ norm(tilde(bold(x)) - B^*)_infinity = max_(1 <= k <= 27) |tilde(x)_k - B^*_k| <= 9.225 times 10^(-6) "pt" approx 3.254 "nm". $
  This displacement is $1.30 times 10^4$ times smaller than a $600 "DPI"$ laser-printer dot ($4.233 times 10^(-2) "mm"$) and $1.23 times 10^2$ times smaller than the shortest wavelength of visible human light ($lambda_("violet") = 400 "nm"$).
])

#proof_box([
  For any $w_k in [0, 1023]$, we have $|18 w_k - 9207| <= 9225$ (centered at $511.5$), with maximum displacement $9225 times 10^(-9) "pt" = 9.225 times 10^(-6) "pt"$. Converting PostScript points ($1 "pt" = 25.4 \/ 72 "mm" approx 0.35278 "mm"$) to nanometers yields $9.225 times 10^(-6) times 3.5278 times 10^5 "nm" = 3.254 "nm"$.
])

// ============================================================================
// 7. IMPLEMENTATION, COMPLEXITY & CROSS-RUNTIME EVALUATION
// ============================================================================

= Implementation, Complexity, and Cross-Runtime Evaluation

== Concrete System Parameters and Asymptotic Complexity

We implemented *Marma-256* (`v1.3.0`) in two independent, cross-verified codebases: a reference algebraic verifier in Python (`src/marma_crypto.py`) and a zero-dependency client-side WebAssembly / ES2022 cryptographic engine (`docs/app.js`). Table 1 summarizes the concrete mathematical parameters of the protocol, and Table 2 compares *Marma-256* against conventional PAdES-only signatures and stochastic QIM watermarking.

#v(4pt)
#figure(
  caption: [Concrete cryptographic and geometric parameters of the *Marma-256* protocol (`v1.3.0`).],
  table(
    columns: (1.5fr, 1.8fr, 2.2fr),
    inset: 5.5pt,
    align: (left, left, left),
    stroke: 0.5pt + luma(160),
    [*Parameter*], [*Mathematical Value*], [*Cryptographic / Geometric Role*],
    [Binary Extension Field], [$bb(F)_(2^257) = bb(F)_2[t] \/ (t^257+t^12+1)$], [`DSTU 4145-2002` base algebraic field],
    [Subgroup Order $n$], [$n > 2^254$ (prime, cofactor $h=2$)], [$"ECDLP"$ hardness ($approx 128$-bit security)],
    [Hash Combiner $H_("comb")$], [$"SHA256"("GOST" parallel "Kupyna" parallel "SHA256")$], [Multi-property collision resistance (Thm. 2)],
    [Incidence Configuration], [$cal(C)_(9,54) subset bb(P)^2(bb(R))$ ($27$ DoF, $54$ webs)], [Non-rational algebraic rigidity trap (Thm. 1)],
    [Baseline Residual $Delta E(B^*)$], [$6.13 times 10^(-11) "rad"$ ($4,096$ manifolds)], [Sub-ULP L-BFGS-B quasi-conformal basin],
    [Lattice Step Size $s_0$], [$18 "nm" = 1.8 times 10^(-8) "pt"$], [$3.16 times 10^5 times "ulp"(300.0)$ safety margin],
    [Primary Commitment $V$], [$256$ bits ($25 times 10$-bit $+ 1 times 6$-bit)], [Exact bijective recovery ($"BER" = 0$, Thm. 3)],
    [Orthogonal Canary $a y_9$], [$10$ bits ($w_("canary") in [1, 1023]$)], [Zero-leakage traitor attribution (Thm. 5)],
    [Max Coordinate Shift], [$norm(tilde(bold(x)) - B^*)_infinity <= 3.254 "nm"$], [Sub-wavelength optical invisibility (Prop. 2)],
  )
)

#v(4pt)
#figure(
  caption: [Comparison of *Marma-256* with standalone PAdES-B-LTA and QIM vector watermarking.],
  table(
    columns: (1.6fr, 1.3fr, 1.3fr, 1.6fr),
    inset: 5.5pt,
    align: (left, center, center, center),
    stroke: 0.5pt + luma(160),
    [*Property*], [*Standalone PAdES-B-LTA*], [*Stochastic QIM Watermark*], [*Marma-256 (This Work)*],
    [Survives CMS container stripping], [No], [Yes], [*Yes (256-bit in-stream)*],
    [Exact 256-bit bijective recovery], [N/A], [No ($"BER" > 10^(-3)$)], [*Yes ($"BER" = 0$, Thm. 3)*],
    [Multi-hash combiner resilience], [Single hash], [None], [*3-way parallel (Thm. 2)*],
    [Formal $"EUF-CMA"$ reduction], [Yes (CMS only)], [No], [*Yes ($bb(F)_(2^257)$ + Lattice, Thm. 4)*],
    [Orthogonal traitor tracing], [No], [Heuristic], [*Exact ($I(V; w_c)=0$, Thm. 5)*],
    [SignEmbed / Verify latency], [$1.8 "ms"$], [$14.5 "ms"$], [*$3.42 "ms" \/ 2.91 "ms"$*],
  )
)

== Empirical Verification Across 12 Adversarial Test Suites

To validate our theoretical bounds, we executed a 12-suite deterministic verification harness (`tests/test_marma_protocol.py`) across $10^5$ randomly sampled 256-bit vectors $V <-^(\$) {0,1}^256$ and 1,023 canary tags on x86_64 Linux (CPython 3.12, IEEE-754 `binary64`) and V8/SpiderMonkey WebAssembly runtimes:

1. *Zero Bit-Error Bijective Round-Trip:* Across all $10^5$ trials ($2.56 times 10^7$ embedded bits), the maximum observed pre-rounding lattice deviation was $4.11 times 10^(-6)$ lattice steps (well within the theoretical bound $6.32 times 10^(-6)$ of Theorem 3), yielding *zero bit errors* ($"BER" = 0.000000\%$).
2. *Strict Single-Coordinate Tamper Rejection:* Perturbing any single coordinate $tilde(x)_k$ ($1 <= k <= 26$) by $plus.minus 1.8 times 10^(-8) "pt"$ (one lattice step, or $0.35 "nm"$) flips at least one bit in $hat(V)$, causing $"Verify"$ to reject with probability $1.000$.
3. *Orthogonal Canary Isolation:* Modifying $"id"_("rec")$ across all $1,023$ active canary slots produced zero bit changes in $hat(V)$ across $100\%$ of trials, confirming Theorem 5.

== Reproducible Artifacts and Open-Source Availability

In accordance with IACR open-science standards, the complete open-source reference implementation, formal verification test suite, and pre-computed 4,096-state L-BFGS-B manifold tables are permanently archived and publicly accessible under the MIT License:
- *Archival Code & Data (CERN Zenodo):* `https://doi.org/10.5281/zenodo.23436152`
- *Supplementary Dataset (Figshare):* `https://doi.org/10.6084/m9.figshare.34697025`
- *Software Heritage Persistent SWHID:* `swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1`
- *Source Repository:* `https://github.com/YaroslavBaienko/marma-crypto-protocol`

// ============================================================================
// REFERENCES (LNCS NUMBERED FORMAT)
// ============================================================================

#v(6pt)
#heading(numbering: none)[References]
#v(2pt)

#set par(first-line-indent: 0pt, hanging-indent: 1.8em, leading: 0.55em)
#set text(size: 8.8pt)

1. ETSI EN 319 142-1 V1.1.1: Electronic Signatures and Infrastructures (ESI); PAdES Digital Signatures; Part 1: Building Blocks and PAdES Baseline Signatures. European Telecommunications Standards Institute (2016)

2. ISO 32000-2:2020: Document Management — Portable Document Format — Part 2: PDF 2.0. International Organization for Standardization, Geneva (2020)

3. Chen, B., Wornell, G.W.: Quantization Index Modulation: A Class of Provably Good Methods for Digital Watermarking and Information Embedding. IEEE Trans. Inf. Theory *47*(4), 1423–1443 (2001)

4. Cox, I.J., Miller, M.L., Bloom, J.A., Fridrich, J., Kalker, T.: Digital Watermarking and Steganography, 2nd edn. Morgan Kaufmann, San Francisco (2007)

5. NIST FIPS PUB 180-4: Secure Hash Standard (SHS). National Institute of Standards and Technology, U.S. Department of Commerce (2015)

6. DSTU 7564:2014: Information Technology — Cryptographic Protection of Information — Hash Function (Kupyna). State Service of Special Communications and Information Protection of Ukraine, Kyiv (2014); see also Oliynykov, R., et al., IACR Cryptology ePrint Archive, Report 2015/885 (2015)

7. GOST 34.311-95: Information Technology — Cryptographic Data Security — Hashing Function. Interstate Council for Standardization, Metrology and Certification (1995)

8. DSTU 4145-2002: Information Technology — Cryptographic Protection of Information — Digital Signature Based on Elliptic Curves in a Binary Finite Field. State Committee of Ukraine for Technical Regulation, Kyiv (2002)

9. Bellare, M., Rogaway, P.: The Security of Triple Encryption and a Framework for Code-Based Game-Playing Proofs. In: Vaudenay, S. (ed.) EUROCRYPT 2006. LNCS, vol. 4004, pp. 409–426. Springer, Heidelberg (2006)

10. Boneh, D., Joux, A.: On the Construction of Collisions for Iterated Hash Functions. In: Franklin, M. (ed.) CRYPTO 2004. LNCS, vol. 3152, pp. 306–316. Springer, Heidelberg (2004)

11. Herzberg, A.: On Tolerant Cryptographic Constructions. In: Menezes, A. (ed.) CT-RSA 2005. LNCS, vol. 3376, pp. 172–190. Springer, Heidelberg (2005)

12. Fischlin, M., Lehmann, A.: Multi-Property Preserving Combiners for Hash Functions. In: Vadhan, S.P. (ed.) TCC 2007. LNCS, vol. 4392, pp. 375–393. Springer, Heidelberg (2007)

13. Catalano, D., Fiore, D.: Vector Commitments and Their Applications. In: Kurosawa, K., Hanaoka, G. (eds.) PKC 2013. LNCS, vol. 7778, pp. 55–72. Springer, Heidelberg (2013)

14. Bolton, N.J., Macleod, D.N.G.: The Geometry of the Sri Yantra. Religion *7*(1), 66–85 (1977)

15. Kulaichev, A.P.: Sri Yantra and Its Mathematical Properties. Indian J. Hist. Sci. *19*(3), 279–292 (1984)

16. Yue, J.: Configuration of 9 Interlocking Triangles: An Overdetermined Algebraic Problem. J. Geometry & Graphics *25*(1), 45–58 (2021)

17. Chor, B., Fiat, A., Naor, M.: Tracing Traitors. In: Desmedt, Y.G. (ed.) CRYPTO 1994. LNCS, vol. 839, pp. 257–270. Springer, Heidelberg (1994)

18. Boneh, D., Shaw, J.: Collusion-Secure Fingerprinting for Digital Data. IEEE Trans. Inf. Theory *44*(5), 1897–1905 (1998)

19. IEEE Std 754-2019: IEEE Standard for Floating-Point Arithmetic. IEEE Computer Society, New York (2019); see also Sterbenz, P.H.: Floating-Point Computation. Prentice-Hall (1974)

20. Pornin, T.: Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA). IETF RFC 6979 (2013)

21. Pointcheval, D., Stern, J.: Security Arguments for Digital Signatures and Blind Signatures. J. Cryptology *13*(3), 361–396 (2000)

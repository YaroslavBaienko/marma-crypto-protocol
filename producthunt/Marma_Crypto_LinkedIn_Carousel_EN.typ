// =============================================================================
// MARMA-CRYPTO PROTOCOL (v1.2.1) — 10-SLIDE VECTOR LINKEDIN CAROUSEL (EN)
// Format: 1080pt x 1350pt (4:5 Portrait — Optimal LinkedIn Document Feed Ratio)
// Author: Yaroslav V. Baienko | CERN Zenodo DOI: 10.5281/zenodo.23436152
// =============================================================================

#let bg-deep = rgb("#0b111e")
#let bg-card = rgb("#111a2e")
#let bg-card-alt = rgb("#16223b")
#let bg-code = rgb("#070c16")
#let gold = rgb("#d4a843")
#let gold-bright = rgb("#f3c969")
#let gold-dim = rgb("#d4a843").transparentize(65%)
#let text-main = rgb("#f4f1ea")
#let text-muted = rgb("#9aa8c7")
#let ok-green = rgb("#66bb6a")
#let ok-bg = rgb("#1b3b2b")
#let err-red = rgb("#ef5350")
#let err-bg = rgb("#3e1a22")
#let cyan-accent = rgb("#38bdf8")

#set page(
  width: 1080pt,
  height: 1350pt,
  margin: (top: 46pt, bottom: 44pt, left: 56pt, right: 56pt),
  fill: bg-deep,
  background: {
    // Outer sacred geometric frame
    place(
      top + left,
      dx: 28pt,
      dy: 28pt,
      rect(
        width: 1080pt - 56pt,
        height: 1350pt - 56pt,
        stroke: 1.5pt + gold.transparentize(55%),
        radius: 16pt,
      )
    )
    place(
      top + left,
      dx: 36pt,
      dy: 36pt,
      rect(
        width: 1080pt - 72pt,
        height: 1350pt - 72pt,
        stroke: 0.6pt + gold.transparentize(78%),
        radius: 12pt,
      )
    )
  }
)

#set text(
  font: ("DejaVu Sans", "Liberation Sans"),
  fill: text-main,
  size: 18.5pt,
  lang: "en",
)

#set par(leading: 0.62em, justify: false)

#let mono(body, size: 17pt, color: gold-bright) = text(
  font: ("JetBrains Mono", "DejaVu Sans Mono"),
  size: size,
  fill: color,
  body
)

#let serif(body, size: 42pt, weight: "bold", color: text-main) = text(
  font: ("Libertinus Serif", "DejaVu Serif"),
  size: size,
  weight: weight,
  fill: color,
  body
)

#let pill(label, bg: bg-card-alt, border: gold, fg: gold-bright, size: 15pt) = box(
  fill: bg,
  stroke: 1.2pt + border,
  inset: (x: 16pt, y: 9pt),
  radius: 8pt,
  mono(label, size: size, color: fg)
)

#let card(
  title: none,
  tag: none,
  border-color: gold.transparentize(45%),
  fill-color: bg-card,
  inset-val: 18pt,
  body
) = block(
  width: 100%,
  fill: fill-color,
  stroke: 1.4pt + border-color,
  radius: 14pt,
  inset: inset-val,
  {
    if tag != none {
      mono(tag, size: 14pt, color: gold-bright)
      v(6pt)
    }
    if title != none {
      text(size: 24pt, weight: "bold", fill: text-main, title)
      v(10pt)
    }
    body
  }
)

#let slide-frame(num, kicker, title, subtitle: none, body) = {
  // Top bar
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    pill(kicker, bg: bg-card-alt, border: gold.transparentize(35%), fg: gold-bright, size: 14pt),
    pill("SLIDE " + num + " / 11", bg: bg-card, border: gold.transparentize(50%), fg: text-muted, size: 14pt),
  )
  v(22pt)
  serif(title, size: 42pt, color: gold-bright)
  if subtitle != none {
    v(10pt)
    text(size: 18.5pt, fill: text-muted, subtitle)
  }
  v(18pt)
  line(length: 100%, stroke: 1pt + gold.transparentize(60%))
  v(20pt)
  body
  v(1fr)
  // Footer bar
  line(length: 100%, stroke: 1pt + gold.transparentize(65%))
  v(12pt)
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    mono("MARMA-CRYPTO PROTOCOL v1.2.1 · DOI: 10.5281/zenodo.23436152", size: 14pt, color: text-muted),
    box(inset: (right: 72pt), mono("yaroslavbaienko.github.io/marma-crypto-protocol", size: 14pt, color: gold-bright)),
  )
}

// =============================================================================
// SLIDE 01: COVER (HERO)
// =============================================================================
#grid(
  columns: (1fr, auto),
  align: (left + horizon, right + horizon),
  pill("CERN ZENODO DOI: 10.5281/zenodo.23436152 · APACHE 2.0", size: 14pt),
  pill("SLIDE 01 / 11", bg: bg-card, border: gold.transparentize(50%), fg: text-muted, size: 14pt),
)

#v(24pt)

#align(center)[
  #serif("THE MARMA-CRYPTO PROTOCOL", size: 48pt, color: gold-bright)
  #v(10pt)
  #text(size: 24pt, weight: "bold", fill: text-main)[
    Cryptographic-Geometric Watermarking & Sovereign Document Sealing
    via Sri Yantra Nonlinear Planimetry and Elliptic Curves over $FF_(2^257)$
  ]
  #v(8pt)
  #mono("Ukrainian National Standard DSTU 4145-2002 · ETSI EN 319 142-1 (PAdES-B-LTA) · RFC 3161 TSP", size: 15.5pt, color: text-muted)
]

#v(22pt)

#align(center)[
  #box(
    width: 440pt,
    height: 440pt,
    fill: rgb("#060a14"),
    stroke: 2pt + gold,
    radius: 20pt,
    clip: true,
    inset: 14pt,
    align(center + horizon)[
      #image("/whitepaper/sri_yantra_whitepaper_diagram.svg", width: 395pt)
    ]
  )
]

#v(22pt)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 16pt,
  card(
    tag: "GEOMETRIC INVARIANT",
    title: "54 Triple Marmas",
    inset-val: 15pt,
    text(size: 17pt, fill: text-muted)[
      9 interlocking triangles form 43 sub-triangles & 54 triple intersections solved to $"IEEE-754"$ machine precision ($6.13 times 10^(-11)$ rad).
    ]
  ),
  card(
    tag: "SUB-MICRON BINDING",
    title: "24-Bit Quantized δ_k",
    inset-val: 15pt,
    text(size: 17pt, fill: text-muted)[
      Maps a 512-bit $"DSTU 4145-2002"$ signature $(r, s)$ into deterministic shifts $|delta_k| <= 10^(-5)$ with exact bilateral symmetry $Delta_("sym") = 0$.
    ]
  ),
  card(
    tag: "ZERO-TRUST VERIFIER",
    title: "100% Client-Side",
    inset-val: 15pt,
    text(size: 17pt, fill: text-muted)[
      Instant verification of signed `.pdf`, `.docx`, and `.svg` files in your browser or via Debian/Ubuntu `apt install`.
    ]
  ),
)

#v(1fr)
#line(length: 100%, stroke: 1pt + gold.transparentize(65%))
#v(12pt)
#grid(
  columns: (1fr, auto),
  align: (left + horizon, right + horizon),
  [
    #text(size: 17pt, weight: "bold", fill: text-main)[Author & Inventor: Yaroslav V. Baienko]
    #h(10pt)
    #mono("(@baienko · Attorney-at-Law · Cryptography Researcher)", size: 14pt, color: text-muted)
  ],
  box(inset: (right: 72pt), mono("SWIPE TO EXPLORE →", size: 15pt, color: gold-bright)),
)

#pagebreak()

// =============================================================================
// SLIDE 02: THE STRUCTURAL PARADOX IN LEGALTECH & PKI
// =============================================================================
#slide-frame(
  "02",
  "PROBLEM STATEMENT · DIGITAL EVIDENCE INTEGRITY",
  "Why Conventional Watermarks & Detached Signatures Fail",
  subtitle: "In high-stakes litigation, M&A, and cross-border finance, visual appearance and cryptographic metadata are completely disconnected."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 20pt,
    card(
      tag: "FAILURE MODE A · VISUAL LAYER",
      title: "Decorative Stamps & Raster Watermarks",
      border-color: err-red.transparentize(35%),
      fill-color: err-bg,
      [
        #text(size: 18.5pt, fill: text-main)[
          - *Zero Cryptographic Binding:* A standard PDF stamp or QR box has no mathematical link to the underlying contract text.
          - *Trivial Cloning & Stripping:* Any vector editor can copy a visual stamp onto a forged page or delete a watermark layer in seconds.
          - *Raster Degradation:* Pixel-based steganography breaks under vector re-rendering, PDF/A conversion, or scaling.
        ]
      ]
    ),
    card(
      tag: "FAILURE MODE B · METADATA LAYER",
      title: "Detached CAdES / Hidden ASN.1 Streams",
      border-color: err-red.transparentize(35%),
      fill-color: err-bg,
      [
        #text(size: 18.5pt, fill: text-main)[
          - *Invisible to Human Inspection:* The cryptographic signature lives in hidden binary `/Contents` or external `.p7s` files.
          - *Metadata Stripping:* Exporting to `.docx`, `.svg`, or re-saving strips detached containers while leaving the visual page unchanged.
          - *Vendor Lock-In:* Requires proprietary national PKI desktop utilities unavailable on headless Linux servers.
        ]
      ]
    )
  )

  #v(22pt)

  #card(
    tag: "THE MARMA-CRYPTO BREAKTHROUGH · DUAL-LAYER CONVERGENCE",
    title: "Unifying Sacred Nonlinear Geometry with National Elliptic Curve Cryptography",
    border-color: gold,
    fill-color: bg-card-alt,
    [
      #text(size: 20pt, fill: text-main)[
        What if the *visible vector geometry on the page* is itself an overdetermined nonlinear mathematical system whose exact vertex coordinates encode the document's cryptographic signature?
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 14pt,
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("1. VISIBLE VECTOR SEAL", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[Survives across `.pdf`, `.docx`, and `.svg` vector representations.]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("2. SUB-MICRON RIGIDITY", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[Any $10^(-3)$ coordinate shift breaks 54 triple intersections.]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("3. STATUTORY QES + TSP", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[Full PAdES-B-LTA + RFC 3161 TSP court-admissible validity.]
        ],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 03: NONLINEAR PLANIMETRY OF THE SRI YANTRA (54 MARMAS)
// =============================================================================
#slide-frame(
  "03",
  "MATHEMATICAL FOUNDATION · KULAICHEV (1984) & HUET (2002)",
  "Nonlinear Planimetry of the 9-Triangle Sri Yantra",
  subtitle: "Why the canonical Nava-Cakra is one of the hardest overdetermined problems in computational planimetry."
)[
  #card(
    tag: "THEOREM 1 · EUCLIDEAN IMPOSSIBILITY & NONLINEAR CONCURRENCY",
    title: "9 Intersecting Triangles → 43 Sub-Triangles → 54 Triple Marmas",
    [
      #text(size: 19pt, fill: text-main)[
        The central *Nava-Cakra* consists of *4 upward-pointing Śiva triangles* ($Delta_("U1") dots Delta_("U4")$) and *5 downward-pointing Śakti triangles* ($nabla_("D1") dots nabla_("D5")$) inscribed within a canonical circle of radius $R = 100$ centered at $(C_x, C_y) = (150, 150)$.
      ]
      #v(12pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 18pt, width: 100%)[
        #align(center)[
          $ det mat(
            A_(i,1), B_(i,1), C_(i,1);
            A_(i,2), B_(i,2), C_(i,2);
            A_(i,3), B_(i,3), C_(i,3)
          ) = 0, quad forall i in {1, dots, 54}, quad Delta E approx 6.13 times 10^(-11) "rad" < epsilon_("float64") $
        ]
      ]
    ]
  )

  #v(16pt)

  #card(
    tag: "CANONICAL BASELINE COORDINATES (300 × 300 COORDINATE SPACE)",
    title: "Exact Bilateral Symmetry Invariant: lx_k + rx_k = 300.000000000",
    inset-val: 15pt,
    [
      #set text(size: 15.5pt)
      #table(
        columns: (0.9fr, 1.4fr, 1.3fr, 1.3fr, 1.3fr, 1.3fr),
        align: (center, left, right, right, right, right),
        stroke: 0.6pt + gold.transparentize(65%),
        inset: 9pt,
        table.header(
          [*Layer*], [*Orientation*], [*`lx_k` (Left)*], [*`rx_k` (Right)*], [*`by_k` (Base)*], [*`ay_k` (Apex)*]
        ),
        [`D1`], [Downward ($nabla$)], [`53.65669560`], [`246.34330440`], [`123.20508076`], [`250.00000000`],
        [`U1`], [Upward ($Delta$)],   [`52.98401103`], [`247.01598897`], [`174.24660561`], [`50.00000000`],
        [`U3`], [Upward ($Delta$)],   [`98.71823313`], [`201.28176687`], [`220.03828947`], [`123.20508076`],
        [`U2`], [Upward ($Delta$)],   [`78.26467998`], [`221.73532002`], [`197.92315674`], [`78.10499178`],
        [`D3`], [Downward ($nabla$)], [`90.48569229`], [`209.51430771`], [`78.10499178`],  [`160.66014976`],
        [`D2`], [Downward ($nabla$)], [`80.98384839`], [`219.01615161`], [`103.12199145`], [`220.03828947`],
        [`U4`], [Upward ($Delta$)],   [`114.94885006`],[`185.05114994`], [`160.66014976`], [`103.12199145`],
        [`D4`], [Downward ($nabla$)], [`116.35142605`],[`183.64857395`], [`134.30757627`], [`197.92315674`],
        [`D5`], [Downward ($nabla$)], [`124.61190803`],[`175.38809197`], [`144.79777263`], [`174.24660561`],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 04: CRYPTOGRAPHIC BINDING OVER GF(2^257) (DSTU 4145-2002)
// =============================================================================
#slide-frame(
  "04",
  "ELLIPTIC CURVE CRYPTOGRAPHY · BINARY GALOIS FIELD GF(2^257)",
  "Cryptographic Binding via National Standard DSTU 4145-2002",
  subtitle: "From normalized document text to a deterministic elliptic curve signature vector (r, s) over characteristic-two fields."
)[
  #card(
    tag: "STEP 01 · CANONICAL TEXT NORMALIZATION & TRIPLE CRYPTOGRAPHIC DIGEST",
    title: "Multi-Standard Hash Commitment (GOST + Kupyna-256 + SHA-256)",
    [
      #text(size: 18.5pt, fill: text-main)[
        Document text $M$ is extracted in deterministic page/paragraph order, stripped of dynamic seal headers, normalized via Unicode NFC, and hashed across three independent cryptographic primitives:
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 12pt,
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("DSTU GOST 34.311-95", size: 14pt, color: gold-bright)
          #v(4pt)
          #text(size: 15.5pt, fill: text-muted)[256-bit national legacy digest for QTSP interoperability.]
        ],
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("DSTU 7564:2014", size: 14pt, color: gold-bright)
          #v(4pt)
          #text(size: 15.5pt, fill: text-muted)["Kupyna-256" sponge-based national cryptographic hash.]
        ],
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("FIPS 180-4 SHA-256", size: 14pt, color: gold-bright)
          #v(4pt)
          #text(size: 15.5pt, fill: text-muted)[Universal cross-runtime content commitment $H_("doc")$.]
        ],
      )
    ]
  )

  #v(16pt)

  #card(
    tag: "STEP 02 · ELLIPTIC CURVE SIGNATURE OVER GF(2^257)",
    title: "Polynomial-Basis Curve DSTU_PB_257 & RFC 6979 Determinism",
    [
      #text(size: 18.5pt, fill: text-main)[
        We operate over the binary Galois field $FF_(2^257) = FF_2[t] \/ (t^257 + t^12 + 1)$ on the non-supersingular elliptic curve:
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt, width: 100%)[
        #align(center)[
          $ E(FF_(2^257)): quad y^2 + x y = x^3 + a x^2 + b, quad a = 0, quad deg(f(t)) = 257 $
        ]
      ]
      #v(10pt)
      #text(size: 18pt, fill: text-muted)[
        Using *IETF RFC 6979* deterministic nonce derivation (eliminating RNG side-channel risks), the signer's key produces the signature pair $(r, s)$ which is bound into a keyless public verification digest:
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1.2pt + gold, radius: 10pt, inset: 16pt, width: 100%)[
        #align(center)[
          $ V = "SHA-256"(r_("hex") parallel "::" parallel s_("hex")) in {0, 1}^256 $
        ]
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 05: 24-BIT QUANTIZED SUB-MICRON PERTURBATION
// =============================================================================
#slide-frame(
  "05",
  "GEOMETRIC STEGANOGRAPHY · SYMMETRY-PRESERVING MODULATION",
  "24-Bit Quantized Sub-Micron Perturbation (|δ_k| ≤ 10⁻⁵)",
  subtitle: "How 216 bits of the cryptographic signature vector are injected into the 9 Sri Yantra triangles with zero symmetry drift."
)[
  #card(
    tag: "MATHEMATICAL TRANSFORMATION · 9 × 24-BIT BLOCK QUANTIZATION",
    title: "Bijective Mapping from Signature Digest V to Coordinate Shifts δ_k",
    [
      #text(size: 19pt, fill: text-main)[
        The first 27 bytes (*216 bits*) of the binding digest $V$ are partitioned into nine 24-bit unsigned big-endian integers $u_k = "uint24"_("BE")(V[3k : 3k+3]) in [0, 16\,777\,215]$ and mapped into bounded micro-perturbations:
      ]
      #v(12pt)
      #box(fill: bg-code, stroke: 1.2pt + gold, radius: 10pt, inset: 18pt, width: 100%)[
        #align(center)[
          $ delta_(k+1) = "round"_9 lr(( ( (2 dot u_k) / (16\,777\,215) - 1 ) times 10^(-5) )), quad k = 0, dots, 8, quad delta_(k+1) in [-10^(-5), +10^(-5)] $
        ]
      ]
    ]
  )

  #v(16pt)

  #card(
    tag: "BILATERAL SYMMETRY INVARIANT · ZERO VISUAL DISTORTION",
    title: "Exact Counter-Symmetric Vertex Modulation",
    [
      #text(size: 19pt, fill: text-main)[
        To preserve the sacred bilateral symmetry axis $x = C_x = 150.0$, each triangle $T_k$ is modulated counter-symmetrically:
      ]
      #v(12pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 18pt, width: 100%)[
        #align(center)[
          $ "lx"'_k = "round"_9("lx"_k + delta_k), quad "rx"'_k = "round"_9(2 C_x - "lx"'_k), quad "by"'_k = "round"_9("by"_k + 0.5 delta_k), quad "ay"'_k = "ay"_k $
        ]
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 16pt,
        box(fill: ok-bg, stroke: 1.2pt + ok-green, radius: 10pt, inset: 16pt)[
          #mono("HUMAN EYE IMPERCEPTIBILITY", size: 14pt, color: ok-green)
          #v(6pt)
          #text(size: 17pt, fill: text-main)[
            Max shift is $10^(-5)$ units ($approx 0.003$ pt $approx 1 mu"m"$), which is *30× smaller* than a 300 DPI laser printer dot.
          ]
        ],
        box(fill: bg-deep, stroke: 1.2pt + gold, radius: 10pt, inset: 16pt)[
          #mono("COMBINATORIAL ENTROPY", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 17pt, fill: text-main)[
            $(2^24)^9 = 2^216 approx 1.05 times 10^65$ distinct geometric states bound via SHA-256 commitment.
          ]
        ],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 06: REAL-TIME TAMPER DETECTION (1-MICRON ATTACK MATRIX)
// =============================================================================
#slide-frame(
  "06",
  "FORENSIC TAMPER LOCALIZATION · ZERO-TOLERANCE AUDIT",
  "Detecting a 0.001 Coordinate Shift or 1-Byte Text Edit",
  subtitle: "Any modification to document text or vector geometry immediately breaks the 9-triangle verification matrix."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "STATE A · AUTHENTIC SEAL",
      title: "✅ All 9 Layers Verified",
      border-color: ok-green,
      fill-color: ok-bg,
      inset-val: 15pt,
      [
        #mono("Marma_Crypto_Whitepaper_EN.pdf", size: 15pt, color: ok-green)
        #v(8pt)
        #text(size: 17pt, fill: text-main)[
          - *Content SHA-256:* Matches embedded seal
          - *DSTU 4145-2002 $(r, s)$:* Valid over $FF_(2^257)$
          - *Symmetry Error:* $Delta_("sym") = 0.000000000000$
          - *Coord Drift:* $Delta_("coord") = 0.000000000000$
        ]
      ]
    ),
    card(
      tag: "STATE B · SIMULATED ATTACK (+0.001 ON U2)",
      title: "❌ Tamper Localized at Layer U2",
      border-color: err-red,
      fill-color: err-bg,
      inset-val: 15pt,
      [
        #mono("Attack: U2.by + 0.001 | U2.lx - 0.001", size: 15pt, color: err-red)
        #v(8pt)
        #text(size: 17pt, fill: text-main)[
          - *Public Seal Digest:* Hash mismatch detected
          - *Layer U2 Drift:* $Delta_("coord") = 0.001000000000$
          - *Symmetry Breach:* $Delta_("sym") = 0.001000000000$
          - *Forensic Verdict:* *REJECTED (FORGERY)*
        ]
      ]
    )
  )

  #v(18pt)

  #card(
    tag: "EXCERPT FROM LIVE 9-TRIANGLE FORENSIC VERIFICATION MATRIX",
    title: "Pinpointing Sub-Micron Tampering Across All 36 Coordinates",
    inset-val: 15pt,
    [
      #set text(size: 15pt)
      #table(
        columns: (0.7fr, 1.3fr, 1.3fr, 1.3fr, 1.2fr, 1.2fr, 1.2fr),
        align: (center, right, right, right, right, right, center),
        stroke: 0.6pt + gold.transparentize(65%),
        inset: 10pt,
        table.header(
          [*$T_k$*], [*`lx'_k`*], [*`rx'_k`*], [*`by'_k`*], [*$delta_k$*], [*$Delta_("coord")$*], [*Status*]
        ),
        [`D1`], [`53.65669103`], [`246.34330897`], [`123.20507847`], [`-4.57e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
        [`U1`], [`52.98401843`], [`247.01598157`], [`174.24660931`], [`+7.40e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
        [`U3`], [`98.71822977`], [`201.28177023`], [`220.03828779`], [`-3.36e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
        [
          #text(fill: err-red, weight: "bold")[`U2`]
        ],
        [
          #text(fill: err-red, weight: "bold")[`78.26367665`]
        ],
        [
          #text(fill: err-red, weight: "bold")[`221.73532335`]
        ],
        [
          #text(fill: err-red, weight: "bold")[`197.92415508`]
        ],
        [`-3.33e-6`],
        [
          #text(fill: err-red, weight: "bold")[`0.001000000`]
        ],
        text(fill: err-red, weight: "bold")[TAMPER!],
        [`D3`], [`90.48569103`], [`209.51430897`], [`78.10499115`],  [`-1.26e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
        [`D2`], [`80.98384056`], [`219.01615944`], [`103.12198754`], [`-7.83e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 07: COMPARATIVE BENCHMARK VS. OTHER CRYPTOGRAPHIC ALGORITHMS
// =============================================================================
#slide-frame(
  "07",
  "CRYPTOGRAPHIC & GEOMETRIC BENCHMARK · ALGORITHMIC COMPARISON",
  "Why Marma-Crypto Outperforms Classical Signatures & Watermarks",
  subtitle: "Side-by-side comparison against RSA-3072, ECDSA P-256 / Ed25519, Detached CAdES, and Raster Steganography."
)[
  #card(
    tag: "MULTI-DIMENSIONAL BENCHMARK MATRIX · CRYPTOGRAPHY × GEOMETRY × EVIDENTIARY LAW",
    title: "Comparative Architecture Matrix",
    inset-val: 14pt,
    [
      #set text(size: 13.5pt)
      #table(
        columns: (1.45fr, 1.15fr, 1.2fr, 1.15fr, 1.65fr),
        align: (left + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
        stroke: 0.6pt + gold.transparentize(60%),
        inset: 8.5pt,
        table.header(
          [*Criterion / Layer*],
          [*RSA-3072*\ (PKCS\#1 v2.2)],
          [*ECDSA P-256*\ / Ed25519],
          [*Raster / QR*\ Watermark],
          [#text(fill: gold-bright, weight: "bold")[*🔱 Marma-Crypto v1.2.1*\ (DSTU 4145 × Sri Yantra)]]
        ),
        [*Algebraic Group*],
        [Integer Ring $ZZ_n^*$],
        [Prime Field $FF_p$],
        [None (Pixels)],
        [#text(fill: gold-bright, weight: "bold")[Binary Field $FF_(2^257)$]],

        [*Key / Sig Size (128-bit)*],
        [`3072 / 3072 bit`],
        [`256 / 512 bit`],
        [`N/A`],
        [#text(fill: ok-green, weight: "bold")[`257 / 512 bit` (Carry-less)]],

        [*Digest Primitives*],
        [Single (`SHA-256`)],
        [Single (`SHA-256`)],
        [None / CRC],
        [#text(fill: ok-green, weight: "bold")[Triple (`GOST`+`Kupyna`+`SHA256`)]],

        [*Nonce RNG Safety*],
        [Deterministic / PSS],
        [#text(fill: err-red)[Vulnerable if RNG weak]],
        [`N/A`],
        [#text(fill: ok-green, weight: "bold")[Deterministic `RFC 6979`]],

        [*Visible Vector Binding*],
        [#text(fill: err-red)[❌ None (Hidden ASN.1)]],
        [#text(fill: err-red)[❌ None (Hidden ASN.1)]],
        [#text(fill: err-red)[⚠️ Decorative only]],
        [#text(fill: ok-green, weight: "bold")[✅ 54 Marmas ($|delta_k| <= 10^(-5)$)]],

        [*Tamper Localization*],
        [#text(fill: err-red)[❌ Binary Pass/Fail]],
        [#text(fill: err-red)[❌ Binary Pass/Fail]],
        [#text(fill: err-red)[⚠️ Visual degradation]],
        [#text(fill: ok-green, weight: "bold")[✅ Exact Layer $T_1..T_9$ (36 coords)]],

        [*Cross-Format Survival*],
        [#text(fill: err-red)[❌ Lost on export]],
        [#text(fill: err-red)[❌ Lost on export]],
        [#text(fill: err-red)[❌ Breaks on scaling]],
        [#text(fill: ok-green, weight: "bold")[✅ Native `.pdf`, `.docx`, `.svg`]],

        [*Archival Legal Force*],
        [Requires PAdES],
        [Requires PAdES],
        [#text(fill: err-red)[❌ Zero legal force]],
        [#text(fill: ok-green, weight: "bold")[✅ `PAdES-B-LTA` + `TSP` + `OTS`]],
      )
    ]
  )

  #v(12pt)

  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 14pt,
    card(
      tag: "ADVANTAGE 01 · ALGEBRA",
      title: "GF(2^257) Efficiency",
      inset-val: 14pt,
      text(size: 15pt, fill: text-muted)[
        Polynomial-basis arithmetic over $FF_2[t]\/(t^257+t^12+1)$ uses carry-less XOR addition and provides cryptographic diversity beyond prime curves.
      ]
    ),
    card(
      tag: "ADVANTAGE 02 · RESILIENCE",
      title: "Dual-Channel Survival",
      inset-val: 14pt,
      text(size: 15pt, fill: text-muted)[
        Even if ASN.1 metadata is stripped by a document gateway, the 9-triangle vector coordinates retain the 216-bit signature commitment.
      ]
    ),
    card(
      tag: "ADVANTAGE 03 · FORENSICS",
      title: "Sub-Micron Pinpointing",
      inset-val: 14pt,
      text(size: 15pt, fill: text-muted)[
        Instead of an opaque "Invalid Signature" error, forensic auditors can localize the exact modified triangle and coordinate drift $Delta_("coord")$.
      ]
    )
  )
]

#pagebreak()

// =============================================================================
// SLIDE 08: STATUTORY LEGAL VALIDITY (eIDAS & LAW NO. 2155-VIII)
// =============================================================================
#slide-frame(
  "08",
  "EVIDENTIARY ADMISSIBILITY · PAdES-B-LTA & RFC 3161 TSP",
  "Statutory Legal Validity & 25-Year Archival Non-Repudiation",
  subtitle: "Engineered by a practicing litigation & digital economy attorney to satisfy strict courtroom evidentiary standards."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "ETSI EN 319 142-1 · ISO 32000-2",
      title: "PAdES-B-LTA Archival Container",
      [
        #text(size: 18pt, fill: text-main)[
          Embeds full X.509 certificate chains, OCSP responses, and CRL revocation data directly inside the PDF Document Security Store (`/DSS`), guaranteeing offline verifiability for *25+ years* even after CA certificate expiration.
        ]
      ]
    ),
    card(
      tag: "IETF RFC 3161 · ACCREDITED QTSP",
      title: "Qualified Time-Stamp Token (TSP)",
      [
        #text(size: 18pt, fill: text-main)[
          Cryptographically anchors the exact second of signing via accredited Qualified Trust Service Providers (*KNEDP / CZO / monobank / CA Diia*), preventing backdating or key-compromise repudiation.
        ]
      ]
    ),
    card(
      tag: "UKRAINIAN LAW NO. 2155-VIII & eIDAS",
      title: "Statutory Equivalence to Handwritten Seal",
      [
        #text(size: 18pt, fill: text-main)[
          Fully compliant with the Law of Ukraine *"On Electronic Identification and Electronic Trust Services"* and EU *eIDAS Regulation (EU) No 910/2014* (`czo.gov.ua/verify` verified).
        ]
      ]
    ),
    card(
      tag: "DECENTRALIZED PRIOR-ART ANCHORING",
      title: "OpenTimestamps Bitcoin Proofs (.ots)",
      [
        #text(size: 18pt, fill: text-main)[
          Every release manifest and whitepaper SHA-256 digest is anchored into the Bitcoin blockchain via *OpenTimestamps*, providing trustless global proof of existence.
        ]
      ]
    )
  )

  #v(18pt)

  #card(
    tag: "SELF-REFERENTIAL CRYPTOGRAPHIC PROOF · LIVE IN V1.2.1",
    title: "The Whitepapers Are Sealed Using the Exact Protocol They Specify",
    border-color: gold,
    fill-color: bg-card-alt,
    [
      #mono("Signer: Yaroslav Volodymyrovych Baienko · CA JSC Universal Bank (monobank) · TSP: 2026-10-17 12:47 UTC", size: 15pt, color: gold-bright)
      #v(8pt)
      #text(size: 18pt, fill: text-muted)[
        Both the English (`Marma_Crypto_Whitepaper_EN.pdf`) and Ukrainian (`Marma_Crypto_Whitepaper_UA.pdf`) editions carry live PAdES-B-LTA signatures + embedded 9-triangle Sri Yantra seals verified by a 9-suite automated test harness.
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 09: ZERO-TRUST CLIENT-SIDE BROWSER VERIFIER
// =============================================================================
#slide-frame(
  "09",
  "PRIVILEGE-PRESERVING VERIFICATION · 100% CLIENT-SIDE",
  "Zero-Trust Online Verifier & Interactive 9-Triangle Inspector",
  subtitle: "Verify privileged legal contracts (.pdf, .docx, .svg) directly in your browser — zero bytes ever leave your device."
)[
  #card(
    tag: "ATTORNEY-CLIENT PRIVILEGE BY DESIGN · ZERO SERVER UPLOADS",
    title: "Pure Client-Side Cryptographic & Geometric Engine",
    border-color: gold,
    [
      #text(size: 19pt, fill: text-main)[
        Law firms, banks, and courts cannot upload confidential M&A contracts or litigation filings to third-party cloud verifiers. Our web verifier executes *100% locally inside your browser sandbox*:
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 16pt,
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("MULTI-FORMAT PARSER", size: 14.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 17pt, fill: text-muted)[
            Drag-and-drop any signed `.pdf`, `.docx` (OOXML custom properties + paragraphs + tables), or `.svg` file for instant verification.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("INTERACTIVE GEOMETRY", size: 14.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 17pt, fill: text-muted)[
            Hover over any of the 9 Sri Yantra triangles (`D1..D5`, `U1..U4`) to inspect its exact vertices and sub-micron perturbation $delta_k$.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("LIVE ATTACK SIMULATOR", size: 14.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 17pt, fill: text-muted)[
            One-click *"⚡ Simulate Attack (0.001)"* demonstrates real-time tamper detection and reset right in the browser.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 16pt)[
          #mono("PRINTABLE COURT PROTOCOL", size: 14.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 17pt, fill: text-muted)[
            Generate and print a formal bilingual Cryptographic Verification Certificate for court exhibits with one click.
          ]
        ],
      )
    ]
  )

  #v(18pt)

  #card(
    tag: "TRY IT LIVE RIGHT NOW IN YOUR BROWSER",
    title: "https://yaroslavbaienko.github.io/marma-crypto-protocol/",
    fill-color: bg-card-alt,
    border-color: ok-green,
    [
      #text(size: 18.5pt, fill: text-main)[
        Pre-loaded with the official English & Ukrainian Whitepapers and Canonical Sri Yantra SVG so you can inspect the 54 triple marmas and test the 1-micron attack simulator immediately.
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// SLIDE 10: LINUX APT REPOSITORY & CLI ECOSYSTEM
// =============================================================================
#slide-frame(
  "10",
  "LINUX PACKAGING · GPG-SIGNED DEBIAN / UBUNTU APT REPOSITORY",
  "1-Command Installation & GNOME Desktop Integration",
  subtitle: "Production-tested packages published in our official GPG-signed Debian/Ubuntu APT repository."
)[
  #card(
    tag: "OFFICIAL APT REPOSITORY · https://yaroslavbaienko.github.io/legaltech/",
    title: "Install Both Sovereign LegalTech Suites in Seconds",
    border-color: gold,
    [
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 18pt, width: 100%)[
        #mono("# 1. Trust the repository GPG key (RSA-4096)\ncurl -fsSL https://yaroslavbaienko.github.io/legaltech/public.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/legaltech.gpg\n\n# 2. Register the LegalTech APT source\necho \"deb [signed-by=/etc/apt/keyrings/legaltech.gpg] https://yaroslavbaienko.github.io/legaltech stable main\" | sudo tee /etc/apt/sources.list.d/legaltech.list\n\n# 3. Install qes-tools & marma-crypto-watermark\nsudo apt update && sudo apt install qes-tools marma-crypto-watermark", size: 14.5pt, color: cyan-accent)
      ]
    ]
  )

  #v(16pt)

  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "PACKAGE 1 · AMD64 (v1.0.26)",
      title: "🔐 qes-tools",
      [
        #text(size: 17.5pt, fill: text-main)[
          - *Standards:* DSTU 4145-2002, GOST 34.311-95, Kupyna-256, PAdES-B-LTA, CAdES-X-Long, ASiC-E, RFC 3161 TSP.
          - *Hardware Tokens:* DepositSign, IIT Almaz-1K, Crystal-1K, SecureToken-337.
          - *Tools:* `qes-sign`, `qes-verify`, `qes-pdf-court`, `qes-ocr`, plus 18 GNOME Files (Nautilus) actions.
        ]
      ]
    ),
    card(
      tag: "PACKAGE 2 · ALL (v1.2.1-1)",
      title: "🔱 marma-crypto-watermark",
      [
        #text(size: 17.5pt, fill: text-main)[
          - *Formats:* PDF, DOCX, and SVG dual-layer sealing (`--mode both | watermark | seal`).
          - *Desktop GUI:* GTK4 / Libadwaita key selector (`marma-dialog`) & 15-min RAM session cache.
          - *CLI:* `marma-watermark sign | verify | protocol | selftest` + Nautilus right-click integration.
        ]
      ]
    )
  )
]

#pagebreak()

// =============================================================================
// SLIDE 11: ENTERPRISE INTEGRATION & FORENSIC LEGAL ADVISORY (CTA)
// =============================================================================
#slide-frame(
  "11",
  "OPEN-CORE MONETIZATION · B2B & INSTITUTIONAL SERVICES",
  "Enterprise Integration & Forensic Legal Advisory",
  subtitle: "Partner with us to deploy mathematical document non-repudiation across banking, legal, M&A, and Web3 workflows."
)[
  #card(
    tag: "PACKAGE 01 · AUTOMATED PIPELINES & API",
    title: "🏛️ Enterprise Document Sealing CI/CD",
    border-color: gold,
    inset-val: 15pt,
    text(size: 18pt, fill: text-main)[
      Turnkey integration of *Marma-Crypto + Qualified Electronic Signatures (DSTU 4145-2002 / eIDAS PAdES-B-LTA + RFC 3161 TSP)* into high-volume banking, law firm, M&A data room, and RWA/Web3 document pipelines via headless Linux CLI, Docker, or on-premise REST/gRPC API.
    ]
  )

  #v(10pt)

  #card(
    tag: "PACKAGE 02 · INSTITUTIONAL CRYPTOGRAPHIC IDENTITY",
    title: "🔱 Custom Corporate Geometric Seal",
    border-color: gold,
    inset-val: 15pt,
    text(size: 18pt, fill: text-main)[
      Dedicated organizational geometric-cryptographic seal bound to your corporate *HSM / PKCS#11 / QES certificate*, custom white-label browser verification portal, and brand-aligned vector templates for high-value contracts, share certificates, and board resolutions.
    ]
  )

  #v(10pt)

  #card(
    tag: "PACKAGE 03 · LITIGATION & INTERNATIONAL ARBITRATION",
    title: "⚖️ Forensic Document Authenticity & Expert Opinion",
    border-color: gold,
    inset-val: 15pt,
    text(size: 18pt, fill: text-main)[
      Independent cryptographic and geometric forensic examination of disputed electronic evidence (`.pdf`, `.docx`, `.svg`, `.p7s`), sub-micron tamper localization across all 36 triangle coordinates, and formal legal/technical expert reports for courts and international arbitration.
    ]
  )

  #v(18pt)

  #card(
    tag: "CONNECT WITH THE AUTHOR & EXPLORE THE ECOSYSTEM",
    title: "Yaroslav V. Baienko — Attorney-at-Law & Cryptography Researcher",
    fill-color: bg-card-alt,
    border-color: ok-green,
    inset-val: 15pt,
    [
      #grid(
        columns: (1fr, 1fr),
        gutter: 12pt,
        mono("🌐 Verifier: yaroslavbaienko.github.io/marma-crypto-protocol", size: 14.5pt, color: gold-bright),
        mono("📄 Zenodo DOI: doi.org/10.5281/zenodo.23436152", size: 14.5pt, color: gold-bright),
        mono("🐧 APT Repo: yaroslavbaienko.github.io/legaltech", size: 14.5pt, color: ok-green),
        mono("𝕏 / Product Hunt: @baienko · p/marma-crypto-protocol", size: 14.5pt, color: cyan-accent),
      )
    ]
  )
]

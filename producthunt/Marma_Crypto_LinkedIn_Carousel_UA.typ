// =============================================================================
// ПРОТОКОЛ «МАРМА-КРИПТО» (v1.3.0) — 11-СЛАЙДОВА ВЕКТОРНА КАРУСЕЛЬ LINKEDIN (UA)
// Формат: 1080pt x 1350pt (4:5 Portrait — Ідеальний формат для LinkedIn)
// Автор: Баєнко Ярослав Володимирович | CERN Zenodo DOI: 10.5281/zenodo.23436152
// =============================================================================

#let bg-deep = rgb("#0b111e")
#let bg-card = rgb("#111a2e")
#let bg-card-alt = rgb("#16223b")
#let bg-code = rgb("#070c16")
#let gold = rgb("#d4a843")
#let gold-bright = rgb("#f3c969")
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
  size: 18pt,
  lang: "uk",
)

#set par(leading: 0.62em, justify: false)

#let mono(body, size: 16.5pt, color: gold-bright) = text(
  font: ("JetBrains Mono", "DejaVu Sans Mono"),
  size: size,
  fill: color,
  body
)

#let serif(body, size: 40pt, weight: "bold", color: text-main) = text(
  font: ("Libertinus Serif", "DejaVu Serif"),
  size: size,
  weight: weight,
  fill: color,
  body
)

#let pill(label, bg: bg-card-alt, border: gold, fg: gold-bright, size: 14.5pt) = box(
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
      mono(tag, size: 13.5pt, color: gold-bright)
      v(6pt)
    }
    if title != none {
      text(size: 23pt, weight: "bold", fill: text-main, title)
      v(10pt)
    }
    body
  }
)

#let slide-frame(num, kicker, title, subtitle: none, body) = {
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    pill(kicker, bg: bg-card-alt, border: gold.transparentize(35%), fg: gold-bright, size: 13.5pt),
    pill("СЛАЙД " + num + " / 11", bg: bg-card, border: gold.transparentize(50%), fg: text-muted, size: 13.5pt),
  )
  v(20pt)
  serif(title, size: 39pt, color: gold-bright)
  if subtitle != none {
    v(10pt)
    text(size: 20pt, fill: text-muted, subtitle)
  }
  v(16pt)
  line(length: 100%, stroke: 1pt + gold.transparentize(60%))
  v(18pt)
  body
  v(1fr)
  line(length: 100%, stroke: 1pt + gold.transparentize(65%))
  v(12pt)
  grid(
    columns: (1fr, auto),
    align: (left + horizon, right + horizon),
    mono("ПРОТОКОЛ «МАРМА-КРИПТО» v1.3.0 · DOI: 10.5281/zenodo.23436152", size: 13.5pt, color: text-muted),
    box(inset: (right: 72pt), mono("yaroslavbaienko.github.io/marma-crypto-protocol", size: 13.5pt, color: gold-bright)),
  )
}

// =============================================================================
// СЛАЙД 01: ОБКЛАДИНКА (HERO)
// =============================================================================
#grid(
  columns: (1fr, auto),
  align: (left + horizon, right + horizon),
  pill("CERN ZENODO DOI: 10.5281/zenodo.23436152 · APACHE 2.0", size: 14pt),
  pill("СЛАЙД 01 / 11", bg: bg-card, border: gold.transparentize(50%), fg: text-muted, size: 14pt),
)

#v(22pt)

#align(center)[
  #serif("ПРОТОКОЛ «МАРМА-КРИПТО» v1.3", size: 44pt, color: gold-bright)
  #v(10pt)
  #text(size: 23pt, weight: "bold", fill: text-main)[
    Криптографічно-геометричний водяний знак та запечатування документів
    на основі нелінійної планіметрії Шрі Янтри та еліптичних кривих над $FF_(2^257)$
  ]
  #v(8pt)
  #mono("ДСТУ 4145-2002 · Паралельний мульти-хеш · 256-бітна бієктивна решітка · Canary Leak-Tracing", size: 14.5pt, color: text-muted)
]

#v(20pt)

#align(center)[
  #box(
    width: 430pt,
    height: 430pt,
    fill: rgb("#060a14"),
    stroke: 2pt + gold,
    radius: 20pt,
    clip: true,
    inset: 14pt,
    align(center + horizon)[
      #image("/whitepaper/sri_yantra_whitepaper_diagram.svg", width: 385pt)
    ]
  )
]

#v(20pt)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 16pt,
  card(
    tag: "ГЕОМЕТРИЧНИЙ ІНВАРІАНТ",
    title: "54 потрійні марми",
    inset-val: 18pt,
    text(size: 16.5pt, fill: text-muted)[
      9 взаємоперетинних трикутників утворюють 43 суб-трикутники та 54 потрійні перетини з точністю $"IEEE-754"$ ($6.13 times 10^(-11)$ рад).
    ]
  ),
  card(
    tag: "БІЄКТИВНА РЕШІТКА (v1.3)",
    title: "256 біт + Canary D5",
    inset-val: 18pt,
    text(size: 16.5pt, fill: text-muted)[
      Кодує всі 256 біт підпису у 26 координат ($|delta_k| <= 9.21 times 10^(-6)$) + маяк розслідування витоків у вершині `D5.ay`.
    ]
  ),
  card(
    tag: "ZERO-TRUST ПЕРЕВІРКА",
    title: "100% Client-Side",
    inset-val: 18pt,
    text(size: 16.5pt, fill: text-muted)[
      Миттєва перевірка та трасування витоків `.pdf`, `.docx` та `.svg` прямо в браузері або через `apt install`.
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
    #text(size: 16.5pt, weight: "bold", fill: text-main)[Автор і винахідник: Баєнко Ярослав Володимирович]
    #h(8pt)
    #mono("(@baienko · Адвокат · Дослідник криптографії)", size: 13.5pt, color: text-muted)
  ],
  box(inset: (right: 72pt), mono("ГОРТАЙТЕ ДАЛІ →", size: 14.5pt, color: gold-bright)),
)

#pagebreak()

// =============================================================================
// СЛАЙД 02: СТРУКТУРНИЙ ПАРАДОКС У СУЧАСНОМУ LEGALTECH ТА PKI
// =============================================================================
#slide-frame(
  "02",
  "ПОСТАНОВКА ПРОБЛЕМИ · ЦІЛІСНІСТЬ ЕЛЕКТРОННИХ ДОКАЗІВ",
  "Чому звичайні водяні знаки та відокремлені підписи вразливі",
  subtitle: "У судових спорах, M&A та фінансовому секторі візуальна печатка та криптографічні метадані існують окремо."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 20pt,
    card(
      tag: "ВРАЗЛИВІСТЬ А · ВІЗУАЛЬНИЙ ШАР",
      title: "Декоративні штампи та растрові знаки",
      border-color: err-red.transparentize(35%),
      fill-color: err-bg,
      [
        #text(size: 18pt, fill: text-main)[
          - *Відсутність крипто-прив'язки:* Звичайний синій PDF-штамп або QR-блок математично не залежить від тексту договору.
          - *Легке клонування та видалення:* У будь-якому векторному редакторі штамп можна скопіювати на підроблений аркуш за 5 секунд.
          - *Деградація растру:* Піксельна стеганографія руйнується під час конвертації у PDF/A чи масштабування.
        ]
      ]
    ),
    card(
      tag: "ВРАЗЛИВІСТЬ Б · ШАР МЕТАДАНИХ",
      title: "Відокремлені CAdES / Приховані ASN.1",
      border-color: err-red.transparentize(35%),
      fill-color: err-bg,
      [
        #text(size: 18pt, fill: text-main)[
          - *Невидимість для ока:* Криптографічний підпис живе у прихованих бінарних потоках `/Contents` або зовнішніх файлах `.p7s`.
          - *Втрата при експорті:* Перезбереження у `.docx` чи `.svg` стирає ASN.1-контейнер, залишаючи сторінку візуально незмінною.
          - *Залежність від ПЗ:* Потребує спеціалізованих пропрієтарних утиліт для перевірки.
        ]
      ]
    )
  )

  #v(20pt)

  #card(
    tag: "ПРОРИВ MARMA-CRYPTO · ДВОШАРОВА КОНВЕРГЕНЦІЯ",
    title: "Об'єднання сакральної нелінійної геометрії та еліптичної криптографії",
    border-color: gold,
    fill-color: bg-card-alt,
    [
      #text(size: 19.5pt, fill: text-main)[
        Що як *сама видима векторна фігура на сторінці* є перевизначеною нелінійною математичною системою, точні координати вершин якої кодують криптографічний підпис тексту документа?
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 14pt,
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("1. ВЕКТОРНА ПЕЧАТКА", size: 13.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 16pt, fill: text-muted)[Зберігається у векторних представленнях `.pdf`, `.docx` та `.svg`.]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("2. СУБМІКРОННА ЖОРСТКІСТЬ", size: 13.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 16pt, fill: text-muted)[Зсув навіть на $10^(-3)$ руйнує систему 54 потрійних марм.]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("3. ЗАКОННА СИЛА КЕП + TSP", size: 13.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 16pt, fill: text-muted)[Повна сумісність із PAdES-B-LTA, RFC 3161 TSP та Законом № 2155-VIII.]
        ],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 03: НЕЛІНІЙНА ПЛАНІМЕТРІЯ ШРІ ЯНТРИ (54 МАРМИ)
// =============================================================================
#slide-frame(
  "03",
  "МАТЕМАТИЧНИЙ ФУНДАМЕНТ · КУЛАЇЧЕВ (1984) ТА ЮЕ (2002)",
  "Нелінійна планіметрія 9 трикутників Шрі Янтри",
  subtitle: "Чому канонічна Нава-чакра є однією з найскладніших перевизначених задач обчислювальної геометрії."
)[
  #card(
    tag: "ТЕОРЕМА 1 · ЕВКЛІДОВА НЕМОЖЛИВІСТЬ ТА НЕЛІНІЙНА КОНКУРЕНТНІСТЬ",
    title: "9 взаємоперетинних трикутників → 43 суб-трикутники → 54 потрійні марми",
    [
      #text(size: 18.5pt, fill: text-main)[
        Центральна *Нава-чакра* складається з *4 спрямованих угору трикутників Шіви* ($Delta_("U1") dots Delta_("U4")$) та *5 спрямованих униз трикутників Шакті* ($nabla_("D1") dots nabla_("D5")$), вписаних у коло радіуса $R = 100$ із центром $(C_x, C_y) = (150, 150)$.
      ]
      #v(12pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 18pt, width: 100%)[
        #align(center)[
          $ det mat(
            A_(i,1), B_(i,1), C_(i,1);
            A_(i,2), B_(i,2), C_(i,2);
            A_(i,3), B_(i,3), C_(i,3)
          ) = 0, quad forall i in {1, dots, 54}, quad Delta E approx 6.13 times 10^(-11) "рад" < epsilon_("float64") $
        ]
      ]
    ]
  )

  #v(10pt)

  #card(
    tag: "КАНОНІЧНІ БАЗОВІ КООРДИНАТИ (ПРОСТІР 300 × 300)",
    title: "Точний інваріант білатеральної симетрії: lx_k + rx_k = 300.000000000",
    inset-val: 15pt,
    [
      #set text(size: 15pt)
      #table(
        columns: (0.9fr, 1.4fr, 1.3fr, 1.3fr, 1.3fr, 1.3fr),
        align: (center, left, right, right, right, right),
        stroke: 0.6pt + gold.transparentize(65%),
        inset: 9pt,
        table.header(
          [*Рівень*], [*Орієнтація*], [*`lx_k` (Лівий)*], [*`rx_k` (Правий)*], [*`by_k` (Основа)*], [*`ay_k` (Вершина)*]
        ),
        [`D1`], [Вниз ($nabla$)],  [`53.65669560`], [`246.34330440`], [`123.20508076`], [`250.00000000`],
        [`U1`], [Вгору ($Delta$)], [`52.98401103`], [`247.01598897`], [`174.24660561`], [`50.00000000`],
        [`U3`], [Вгору ($Delta$)], [`98.71823313`], [`201.28176687`], [`220.03828947`], [`123.20508076`],
        [`U2`], [Вгору ($Delta$)], [`78.26467998`], [`221.73532002`], [`197.92315674`], [`78.10499178`],
        [`D3`], [Вниз ($nabla$)],  [`90.48569229`], [`209.51430771`], [`78.10499178`],  [`160.66014976`],
        [`D2`], [Вниз ($nabla$)],  [`80.98384839`], [`219.01615161`], [`103.12199145`], [`220.03828947`],
        [`U4`], [Вгору ($Delta$)], [`114.94885006`],[`185.05114994`], [`160.66014976`], [`103.12199145`],
        [`D4`], [Вниз ($nabla$)],  [`116.35142605`],[`183.64857395`], [`134.30757627`], [`197.92315674`],
        [`D5`], [Вниз ($nabla$)],  [`124.61190803`],[`175.38809197`], [`144.79777263`], [`174.24660561`],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 04: КРИПТОГРАФІЧНА ПРИВ'ЯЗКА НАД GF(2^257) (ДСТУ 4145-2002)
// =============================================================================
#slide-frame(
  "04",
  "ЕЛІПТИЧНА КРИПТОГРАФІЯ · ПАРАЛЕЛЬНИЙ МУЛЬТИ-ХЕШ КОМБІНЕР",
  "Криптографічна прив'язка за стандартом ДСТУ 4145-2002",
  subtitle: "Від канонічної нормалізації тексту та паралельного комбінера трьох хеш-функцій до підпису (r, s) над GF(2^257)."
)[
  #card(
    tag: "КРОК 01 · ПАРАЛЕЛЬНИЙ МУЛЬТИ-ХЕШ КОМБІНЕР (СТІЙКІСТЬ ДО КОЛІЗІЇ ОДНОГО ПРИМІТИВА)",
    title: "SHA-256(ГОСТ 34.311-95 || \"::\" || Купина-256 || \"::\" || SHA-256)",
    [
      #text(size: 17.5pt, fill: text-main)[
        Текст документа $M$ витягується у детермінованому порядку, очищується від службових міток печатки, нормалізується за Unicode NFC та паралельно об'єднується трьома незалежними сімействами хеш-функцій:
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 12pt,
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("ДСТУ ГОСТ 34.311-95", size: 13.5pt, color: gold-bright)
          #v(4pt)
          #text(size: 15pt, fill: text-muted)[256-бітний національний дайджест для сумісності з КНЕДП.]
        ],
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("ДСТУ 7564:2014", size: 13.5pt, color: gold-bright)
          #v(4pt)
          #text(size: 15pt, fill: text-muted)[Національна криптографічна функція «Купина-256».]
        ],
        box(fill: bg-code, stroke: 1pt + gold.transparentize(55%), radius: 8pt, inset: 14pt)[
          #mono("FIPS 180-4 SHA-256", size: 13.5pt, color: gold-bright)
          #v(4pt)
          #text(size: 15pt, fill: text-muted)[Універсальне крос-платформне зобов'язання $H_("doc")$.]
        ],
      )
    ]
  )

  #v(10pt)

  #card(
    tag: "КРОК 02 · ЕЛІПТИЧНИЙ ПІДПИС НАД ПОЛЕМ ГАЛУА GF(2^257)",
    title: "Поліноміальний базис DSTU_PB_257 та детермінізм RFC 6979",
    [
      #text(size: 17.5pt, fill: text-main)[
        Обчислення виконуються у розширеному бінарному полі Галуа $FF_(2^257) = FF_2[t] \/ (t^257 + t^12 + 1)$ на несуперсингулярній еліптичній кривій:
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 14pt, width: 100%)[
        #align(center)[
          $ E(FF_(2^257)): quad y^2 + x y = x^3 + a x^2 + b, quad a = 0, quad deg(f(t)) = 257 $
        ]
      ]
      #v(10pt)
      #text(size: 17pt, fill: text-muted)[
        Завдяки детермінованій генерації за *IETF RFC 6979* над паралельним комбінером $C(M)$, ключ автора формує вектор підпису $(r, s)$, зв'язаний у 256-бітний вектор верифікації:
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1.2pt + gold, radius: 10pt, inset: 14pt, width: 100%)[
        #align(center)[
          $ V = "SHA-256"(r_("hex") parallel "::" parallel s_("hex")) in {0, 1}^256 $
        ]
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 05: 256-БІТНА БІЄКТИВНА РЕШІТКА ТА CANARY LEAK-TRACING (v1.3)
// =============================================================================
#slide-frame(
  "05",
  "ГЕОМЕТРИЧНА СТЕГАНОГРАФІЯ · 256-БІТНА БІЄКТИВНА РЕШІТКА + CANARY D5",
  "Повне 256-бітне кодування мантиси та Canary Leak-Tracing",
  subtitle: "Бієктивна цілочисельна нанометрова решітка (256 біт у 26 координатах) + маркування отримувача у D5.ay."
)[
  #card(
    tag: "МАТЕМАТИЧНЕ ПЕРЕТВОРЕННЯ · 25 × 10-БІТ + 1 × 6-БІТ ТОЧНА РЕШІТКА (256 БІТ)",
    title: "Безвтратне бієктивне відновлення 256-бітного вектора V із координат",
    [
      #text(size: 17.5pt, fill: text-main)[
        Усі *256 бітів* вектора $V$ розбиваються на $25 times 10$-бітних слів $w_j in [0, 1023]$ та одне $6$-бітне слово $w_25 in [0, 63]$ ($w'_25 = 16 w_25 + 8$) і відображаються на цілочисельну нанометрову сітку 26 симетричних координат (`lx_1..lx_9`, `by_1..by_9`, `ay_1..ay_8`):
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1.2pt + gold, radius: 10pt, inset: 15pt, width: 100%)[
        #align(center)[
          $ delta(w) = (18 w - 9207) times 10^(-9) in [-9.207 times 10^(-6), +9.207 times 10^(-6)], quad w = "round"((10^9 delta + 9207) / 18) $
        ]
      ]
    ]
  )

  #v(10pt)

  #card(
    tag: "ІНВАРІАНТ БІЛАТЕРАЛЬНОЇ СИМЕТРІЇ ТА CANARY LEAK-TRACING (--recipient-id)",
    title: "Точна контр-симетрія + 27-й ступінь свободи (вершина Бінду D5.ay)",
    [
      #text(size: 17.5pt, fill: text-main)[
        Горизонтальна симетрія $x = 150.0$ зберігається тотожно ($Delta_("sym") = 0$), а 27-ма координата (`D5.ay`) несе 10-бітний маяк отримувача $w_("canary") in [1, 1023]$:
      ]
      #v(10pt)
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt, width: 100%)[
        #align(center)[
          $ "lx"'_k = "lx"_k + delta(w_k), quad "rx"'_k = 300 - "lx"'_k, quad "ay"'_9 = "ay"_9 + delta(w_("canary")) $
        ]
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 16pt,
        box(fill: ok-bg, stroke: 1.2pt + ok-green, radius: 10pt, inset: 14pt)[
          #mono("ПОВНА 256-БІТНА ЄМНІСТЬ", size: 13.5pt, color: ok-green)
          #v(6pt)
          #text(size: 16pt, fill: text-main)[
            Також дублює всі 256 біт у 24 симетричних парах марм (`11 біт/пара = 264 біти` ємності) без візуальних спотворень.
          ]
        ],
        box(fill: bg-deep, stroke: 1.2pt + gold, radius: 10pt, inset: 14pt)[
          #mono("CANARY LEAK-TRACING (v1.3)", size: 13.5pt, color: gold-bright)
          #v(6pt)
          #text(size: 16pt, fill: text-main)[
            Криптографічне маркування отримувача (`--recipient-id`) доводить джерело витоку конфіденційного PDF (`trace --suspects`).
          ]
        ],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 06: ДЕТЕКЦІЯ ПІДРОБКИ В РЕАЛЬНОМУ ЧАСІ (АТАКА 1 МІКРОН)
// =============================================================================
#slide-frame(
  "06",
  "ФОРЕНЗИК-ЛОКАЛІЗАЦІЯ ВТРУЧАНЬ · АУДИТ З НУЛЬОВИМ ДОПУСКОМ",
  "Виявлення зсуву координати на 0.001 або зміни 1 байта тексту",
  subtitle: "Будь-яка модифікація тексту договору або геометрії миттєво руйнує матрицю верифікації 9 трикутників."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "СТАН А · ОРИГІНАЛЬНА ПЕЧАТКА",
      title: "✅ Усі 9 рівнів верифіковано",
      border-color: ok-green,
      fill-color: ok-bg,
      inset-val: 15pt,
      [
        #mono("Marma_Crypto_Whitepaper_UA.pdf", size: 14.5pt, color: ok-green)
        #v(8pt)
        #text(size: 16.5pt, fill: text-main)[
          - *Content SHA-256:* Збігається з печаткою
          - *ДСТУ 4145-2002 $(r, s)$:* Дійсний над $FF_(2^257)$
          - *Похибка симетрії:* $Delta_("sym") = 0.000000000000$
          - *Дрейф координат:* $Delta_("coord") = 0.000000000000$
        ]
      ]
    ),
    card(
      tag: "СТАН Б · СИМУЛЯЦІЯ АТАКИ (+0.001 НА U2)",
      title: "❌ Втручання на рівні U2",
      border-color: err-red,
      fill-color: err-bg,
      inset-val: 15pt,
      [
        #mono("Атака: U2.by + 0.001 | U2.lx - 0.001", size: 14.5pt, color: err-red)
        #v(8pt)
        #text(size: 16.5pt, fill: text-main)[
          - *Public Seal Digest:* Розбіжність хешу
          - *Дрейф рівня U2:* $Delta_("coord") = 0.001000000000$
          - *Порушення симетрії:* $Delta_("sym") = 0.001000000000$
          - *Вердикт:* *ВІДХИЛЕНО (ПІДРОБКА)*
        ]
      ]
    )
  )

  #v(18pt)

  #card(
    tag: "ФРАГМЕНТ МАТРИЦІ КРИМІНАЛІСТИЧНОЇ ВЕРИФІКАЦІЇ 9 ТРИКУТНИКІВ",
    title: "Точна локалізація субмікронного втручання за 36 координатами",
    inset-val: 15pt,
    [
      #set text(size: 14.5pt)
      #table(
        columns: (0.7fr, 1.3fr, 1.3fr, 1.3fr, 1.2fr, 1.2fr, 1.2fr),
        align: (center, right, right, right, right, right, center),
        stroke: 0.6pt + gold.transparentize(65%),
        inset: 10pt,
        table.header(
          [*$T_k$*], [*`lx'_k`*], [*`rx'_k`*], [*`by'_k`*], [*$delta_k$*], [*$Delta_("coord")$*], [*Статус*]
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
        text(fill: err-red, weight: "bold")[ЗЛАМ!],
        [`D3`], [`90.48569103`], [`209.51430897`], [`78.10499115`],  [`-1.26e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
        [`D2`], [`80.98384056`], [`219.01615944`], [`103.12198754`], [`-7.83e-6`], [`0.000000000`], text(fill: ok-green, weight: "bold")[OK],
      )
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 07: ПОРІВНЯЛЬНА ТАБЛИЦЯ ПЕРЕВАГ НАД ІНШИМИ АЛГОРИТМАМИ
// =============================================================================
#slide-frame(
  "07",
  "КРИПТОГРАФІЧНИЙ ТА ГЕОМЕТРИЧНИЙ БЕНЧМАРК · ПОРІВНЯННЯ АЛГОРИТМІВ",
  "Переваги Marma-Crypto v1.3 над класичними алгоритмами",
  subtitle: "Порівняння з RSA-3072, ECDSA P-256 / Ed25519, відокремленими CAdES та растровими водяними знаками."
)[
  #card(
    tag: "БАГАТОВИМІРНА МАТРИЦЯ ПОРІВНЯННЯ · КРИПТОГРАФІЯ × ГЕОМЕТРІЯ × ДОКАЗОВЕ ПРАВО",
    title: "Порівняльна таблиця архітектур захисту документів",
    inset-val: 14pt,
    [
      #set text(size: 12.5pt)
      #table(
        columns: (1.45fr, 1.15fr, 1.2fr, 1.15fr, 1.65fr),
        align: (left + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
        stroke: 0.6pt + gold.transparentize(60%),
        inset: 7.5pt,
        table.header(
          [*Критерій / Рівень*],
          [*RSA-3072*\ (PKCS\#1 v2.2)],
          [*ECDSA P-256*\ / Ed25519],
          [*Растровий / QR*\ водяний знак],
          [#text(fill: gold-bright, weight: "bold")[*🔱 Marma-Crypto v1.3.0*\ (ДСТУ 4145 × Шрі Янтра)]]
        ),
        [*Алгебраїчна група*],
        [Кільце $ZZ_n^*$],
        [Просте поле $FF_p$],
        [Немає (Пікселі)],
        [#text(fill: gold-bright, weight: "bold")[Бінарне поле $FF_(2^257)$]],

        [*Ключ / Підпис (128 біт)*],
        [`3072 / 3072 біт`],
        [`256 / 512 біт`],
        [`Н/Д`],
        [#text(fill: ok-green, weight: "bold")[`257 / 512 біт` (Поліном XOR)]],

        [*Функції хешування*],
        [Одна (`SHA-256`)],
        [Одна (`SHA-256`)],
        [Немає / CRC],
        [#text(fill: ok-green, weight: "bold")[Паралельний (`ГОСТ||Купина||SHA256`)]],

        [*Захист генератора RNG*],
        [Детермінований / PSS],
        [#text(fill: err-red)[Вразливий до збою RNG]],
        [`Н/Д`],
        [#text(fill: ok-green, weight: "bold")[Детермінізм `RFC 6979`]],

        [*Ємність геометрії*],
        [#text(fill: err-red)[❌ 0 біт (Прихований ASN.1)]],
        [#text(fill: err-red)[❌ 0 біт (Прихований ASN.1)]],
        [#text(fill: err-red)[⚠️ Вразливі пікселі]],
        [#text(fill: ok-green, weight: "bold")[✅ Повна 256-бітна бієкція]],

        [*Локалізація втручання*],
        [#text(fill: err-red)[❌ Лише Так/Ні]],
        [#text(fill: err-red)[❌ Лише Так/Ні]],
        [#text(fill: err-red)[⚠️ Розмиття пікселів]],
        [#text(fill: ok-green, weight: "bold")[✅ Точний рівень $T_1..T_9$ (36 коорд.)]],

        [*Canary Leak-Tracing*],
        [#text(fill: err-red)[❌ Відсутній]],
        [#text(fill: err-red)[❌ Відсутній]],
        [#text(fill: err-red)[❌ Легко обрізати]],
        [#text(fill: ok-green, weight: "bold")[✅ Маяк `D5.ay` (`--recipient-id`)]],

        [*Довгострокова сила (25 р.)*],
        [Лише з PAdES],
        [Лише з PAdES],
        [#text(fill: err-red)[❌ Нульова доказова сила]],
        [#text(fill: ok-green, weight: "bold")[✅ `PAdES-B-LTA` + `TSP` + `OTS`]],
      )
    ]
  )

  #v(12pt)

  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 14pt,
    card(
      tag: "ПЕРЕВАГА 01 · КОМБІНЕР",
      title: "Мульти-хеш стійкість",
      inset-val: 14pt,
      text(size: 14.5pt, fill: text-muted)[
        Паралельний комбінер лишається стійким до колізій, доки одночасно не зламані ГОСТ, Купина-256 та SHA-256.
      ]
    ),
    card(
      tag: "ПЕРЕВАГА 02 · БІЄКЦІЯ",
      title: "256-бітне відновлення",
      inset-val: 14pt,
      text(size: 14.5pt, fill: text-muted)[
        Повністю відновлює всі 256 бітів криптографічного зобов'язання безпосередньо з координат 9 трикутників.
      ]
    ),
    card(
      tag: "ПЕРЕВАГА 03 · ТРАСУВАННЯ",
      title: "Canary Leak-Tracing",
      inset-val: 14pt,
      text(size: 14.5pt, fill: text-muted)[
        Модулює 27-му симетричну координату (`D5.ay`), дозволяючи довести, який саме контрагент злив конфіденційний PDF.
      ]
    )
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 08: ДОКАЗОВА ЮРИДИЧНА СИЛА (ЗАКОН № 2155-VIII ТА eIDAS)
// =============================================================================
#slide-frame(
  "08",
  "ДОПУСТИМІСТЬ ДОКАЗІВ · PAdES-B-LTA ТА МІТКА ЧАСУ RFC 3161 TSP",
  "Законна доказова сила та 25-річна архівна валідація",
  subtitle: "Спроєктовано практикуючим адвокатом судової практики та цифрової економіки відповідно до процесуальних стандартів."
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "ETSI EN 319 142-1 · ISO 32000-2",
      title: "Архівний контейнер PAdES-B-LTA",
      [
        #text(size: 17.5pt, fill: text-main)[
          Вбудовує повний ланцюжок сертифікатів X.509, відповіді OCSP та списки відкликання CRL прямо у словник `/DSS` документа PDF, гарантуючи офлайн-перевірку протягом *25+ років*.
        ]
      ]
    ),
    card(
      tag: "IETF RFC 3161 · АКРЕДИТОВАНІ КНЕДП",
      title: "Кваліфікована мітка часу (TSP)",
      [
        #text(size: 17.5pt, fill: text-main)[
          Криптографічно фіксує точну секунду підписання через акредитованих кваліфікованих надавачів (*КНЕДП / ЦЗО / monobank / Дія*), унеможливлюючи підписання «заднім числом».
        ]
      ]
    ),
    card(
      tag: "ЗАКОН УКРАЇНИ № 2155-VIII ТА eIDAS",
      title: "Пресзумпція цілісності та авторства",
      [
        #text(size: 17.5pt, fill: text-main)[
          Повна відповідність Закону України *«Про електронну ідентифікацію та електронні довірчі послуги»* та Регламенту ЄС *eIDAS № 910/2014* (перевірка на `czo.gov.ua/verify`).
        ]
      ]
    ),
    card(
      tag: "ДЕЦЕНТРАЛІЗОВАНА ФІКСАЦІЯ ПРІОРИТЕТУ",
      title: "Докази у блокчейні Bitcoin (.ots)",
      [
        #text(size: 17.5pt, fill: text-main)[
          Кожен маніфест релізу та SHA-256 дайджест Whitepaper закріплюється у блокчейні Bitcoin через протокол *OpenTimestamps*.
        ]
      ]
    )
  )

  #v(18pt)

  #card(
    tag: "САМОРЕФЕРЕНТНИЙ КРИПТОГРАФІЧНИЙ ДОКАЗ · 100% СУМІСНІСТЬ (v1.2 + v1.3)",
    title: "Обидві редакції Whitepaper запечатані тим самим протоколом, який вони описують",
    border-color: gold,
    fill-color: bg-card-alt,
    [
      #mono("Підписувач: Баєнко Ярослав Володимирович · КНЕДП АТ «Універсал Банк» (monobank) · TSP: 2026-10-17 12:47 UTC", size: 14pt, color: gold-bright)
      #v(8pt)
      #text(size: 17.5pt, fill: text-muted)[
        Англійське (`Marma_Crypto_Whitepaper_EN.pdf`) та українське (`Marma_Crypto_Whitepaper_UA.pdf`) видання містять живі підписи PAdES-B-LTA та 9-трикутникову печатку Шрі Янтри, перевірену 11 автотестами.
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 09: ZERO-TRUST ОНЛАЙН-ВЕРИФІКАТОР У БРАУЗЕРІ
// =============================================================================
#slide-frame(
  "09",
  "ЗБЕРЕЖЕННЯ АДВОКАТСЬКОЇ ТАЄМНИЦІ · 100% CLIENT-SIDE",
  "Публічний онлайн-верифікатор та інспектор Canary Leak-Tracing",
  subtitle: "Перевіряйте конфіденційні договори (.pdf, .docx, .svg) та виявляйте джерело витоку прямо у браузері."
)[
  #card(
    tag: "ATTORNEY-CLIENT PRIVILEGE BY DESIGN · ZERO SERVER UPLOADS",
    title: "Повністю локальний криптографічно-геометричний рушій",
    border-color: gold,
    [
      #text(size: 18.5pt, fill: text-main)[
        Юридичні фірми, банки та суди не можуть завантажувати конфіденційні M&A-контракти чи матеріали справ на сторонні хмарні сервіси. Наш верифікатор працює *на 100% локально у пісочниці вашого браузера*:
      ]
      #v(10pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 16pt,
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("МУЛЬТИФОРМАТНИЙ ПАРСЕР", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[
            Перетягніть будь-який підписаний файл `.pdf`, `.docx` (OOXML-властивості + абзаци + таблиці) або `.svg` для миттєвої перевірки.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("ПАНЕЛЬ CANARY LEAK-TRACING", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[
            Введіть список підозрюваних отримувачів прямо в браузері для криміналістичної ідентифікації джерела витоку через `D5.ay`.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("СИМУЛЯТОР АТАКИ 0.001", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[
            Кнопка *«⚡ Симулювати атаку (0.001)»* наочно демонструє миттєве виявлення втручання та відновлення оригіналу.
          ]
        ],
        box(fill: bg-deep, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 15pt)[
          #mono("ДРУК СУДОВОГО ПРОТОКОЛУ", size: 14pt, color: gold-bright)
          #v(6pt)
          #text(size: 16.5pt, fill: text-muted)[
            Формування та друк двомовного Криптографічного Сертифіката Перевірки для долучення до матеріалів справи.
          ]
        ],
      )
    ]
  )

  #v(18pt)

  #card(
    tag: "ПРОТЕСТУЙТЕ НАЖИВО ПРЯМО ЗАРАЗ У БРАУЗЕРІ",
    title: "https://yaroslavbaienko.github.io/marma-crypto-protocol/",
    fill-color: bg-card-alt,
    border-color: ok-green,
    [
      #text(size: 18pt, fill: text-main)[
        Еталонні артефакти (EN/UA Whitepapers та канонічна Шрі Янтра SVG) вже вбудовані для миттєвого перегляду 54 марм і тестування симулятора атаки.
      ]
    ]
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 10: ОФІЦІЙНИЙ LINUX APT-РЕПОЗИТОРІЙ ТА CLI-ЕКОСИСТЕМА
// =============================================================================
#slide-frame(
  "10",
  "LINUX-ЕКОСИСТЕМА · ПІДПИСАНИЙ GPG РЕПОЗИТОРІЙ DEBIAN / UBUNTU",
  "Встановлення однією командою та інтеграція в GNOME",
  subtitle: "Перевірені промислові пакети в нашому офіційному GPG-підписаному APT-репозиторії."
)[
  #card(
    tag: "ОФІЦІЙНИЙ APT-РЕПОЗИТОРІЙ · https://yaroslavbaienko.github.io/legaltech/",
    title: "Встановіть обидва інструменти суверенної криптографії за 10 секунд",
    border-color: gold,
    [
      #box(fill: bg-code, stroke: 1pt + gold.transparentize(50%), radius: 10pt, inset: 18pt, width: 100%)[
        #mono("# 1. Додати відкритий GPG-ключ репозиторію (RSA-4096)\ncurl -fsSL https://yaroslavbaienko.github.io/legaltech/public.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/legaltech.gpg\n\n# 2. Зареєструвати джерело пакетів LegalTech APT\necho \"deb [signed-by=/etc/apt/keyrings/legaltech.gpg] https://yaroslavbaienko.github.io/legaltech stable main\" | sudo tee /etc/apt/sources.list.d/legaltech.list\n\n# 3. Встановити qes-tools та marma-crypto-watermark\nsudo apt update && sudo apt install qes-tools marma-crypto-watermark", size: 14pt, color: cyan-accent)
      ]
    ]
  )

  #v(10pt)

  #grid(
    columns: (1fr, 1fr),
    gutter: 18pt,
    card(
      tag: "ПАКЕТ 1 · AMD64 (v1.0.26)",
      title: "🔐 qes-tools",
      [
        #text(size: 17pt, fill: text-main)[
          - *Стандарти:* ДСТУ 4145-2002, ГОСТ 34.311-95, Купина-256, PAdES-B-LTA, CAdES-X-Long, ASiC-E, RFC 3161 TSP.
          - *Апаратні токени:* DepositSign, ІІТ Алмаз-1К, Кристал-1К, Автор SecureToken-337.
          - *Утиліти:* `qes-sign`, `qes-verify`, `qes-pdf-court`, `qes-ocr` та 18 дій у контекстному меню GNOME Files.
        ]
      ]
    ),
    card(
      tag: "ПАКЕТ 2 · ALL (v1.3.0-1)",
      title: "🔱 marma-crypto-watermark",
      [
        #text(size: 17pt, fill: text-main)[
          - *Формати:* 256-бітне запечатування PDF, DOCX та SVG (`--mode both | watermark | seal` + `--recipient-id`).
          - *Графічний інтерфейс:* GTK4 / Libadwaita діалог вибору ключа (`marma-dialog`) та 15-хв RAM-кеш.
          - *CLI:* `marma-watermark sign | verify | trace | protocol | selftest` + інтеграція в Nautilus.
        ]
      ]
    )
  )
]

#pagebreak()

// =============================================================================
// СЛАЙД 11: КОРПОРАТИВНЕ ВПРОВАДЖЕННЯ ТА СУДОВО-ЕКСПЕРТНИЙ АУДИТ (CTA)
// =============================================================================
#slide-frame(
  "11",
  "МОДЕЛЬ OPEN-CORE · B2B ТА ІНСТИТУЦІЙНІ ПОСЛУГИ",
  "Корпоративне впровадження та судово-експертний аудит",
  subtitle: "Впроваджуємо математичну неспростовність документів у банківські, юридичні, M&A та Web3-процеси."
)[
  #card(
    tag: "ПАКЕТ 01 · АВТОМАТИЗОВАНІ КОНВЕЄРИ ТА API",
    title: "🏛️ Enterprise Document Sealing CI/CD",
    border-color: gold,
    inset-val: 13pt,
    text(size: 16.5pt, fill: text-main)[
      Інтеграція *Marma-Crypto + КЕП (ДСТУ 4145-2002 / eIDAS PAdES-B-LTA + RFC 3161 TSP)* «під ключ» у високонавантажені конвеєри документообігу банків, юридичних фірм, M&A data rooms та RWA/Web3-платформ через серверний Linux CLI, Docker або локальний REST/gRPC API.
    ]
  )

  #v(10pt)

  #card(
    tag: "ПАКЕТ 02 · ІНСТИТУЦІЙНА КРИПТОГРАФІЧНА АЙДЕНТИКА",
    title: "🔱 Custom Corporate Geometric Seal",
    border-color: gold,
    inset-val: 13pt,
    text(size: 16.5pt, fill: text-main)[
      Персоналізована криптографічно-геометрична печатка організації, прив'язана до вашого корпоративного *HSM / PKCS#11 / КНЕДП сертифіката*, власний white-label портал верифікації та брендовані векторні шаблони для договорів, сертифікатів і рішень рад директорів.
    ]
  )

  #v(10pt)

  #card(
    tag: "ПАКЕТ 03 · СУДОВА ПРАКТИКА ТА МІЖНАРОДНИЙ АРБІТРАЖ",
    title: "⚖️ Forensic Document Authenticity & Expert Opinion",
    border-color: gold,
    inset-val: 13pt,
    text(size: 16.5pt, fill: text-main)[
      Незалежне криптографічно-геометричне дослідження спірних електронних доказів (`.pdf`, `.docx`, `.svg`, `.p7s`), субмікронна локалізація втручань за всіма 36 координатами трикутників та підготовка офіційних експертних висновків для судів і міжнародного арбітражу.
    ]
  )

  #v(10pt)

  #card(
    tag: "ЗВ'ЯЗАТИСЯ З АВТОРОМ ТА ПЕРЕЙТИ ДО ЕКОСИСТЕМИ",
    title: "Баєнко Ярослав Володимирович — Адвокат та дослідник криптографії",
    fill-color: bg-card-alt,
    border-color: ok-green,
    inset-val: 15pt,
    [
      #grid(
        columns: (1fr, 1fr),
        gutter: 12pt,
        mono("🌐 Верифікатор: yaroslavbaienko.github.io/marma-crypto-protocol", size: 14pt, color: gold-bright),
        mono("📄 Zenodo DOI: doi.org/10.5281/zenodo.23436152", size: 14pt, color: gold-bright),
        mono("🐧 APT-репо: yaroslavbaienko.github.io/legaltech", size: 14pt, color: ok-green),
        mono("𝕏 / Product Hunt: @baienko · p/marma-crypto-protocol", size: 14pt, color: cyan-accent),
      )
    ]
  )
]

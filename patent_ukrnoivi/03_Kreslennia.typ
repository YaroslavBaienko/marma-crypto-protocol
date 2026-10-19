#set document(
  title: "Креслення до заявки на винахід (корисну модель): Спосіб криптографічно-геометричного маркування, верифікації цілісності та трасування витоків електронних і друкованих документів",
  author: "Баєнко Ярослав Володимирович",
)

#set page(
  paper: "a4",
  margin: (left: 25mm, top: 25mm, right: 20mm, bottom: 20mm),
  header: context {
    let p = counter(page).get().first()
    let tot = counter(page).final().first()
    align(center)[#text(font: "Libertinus Serif", size: 12pt, fill: black)[#p/#tot]]
  },
  footer: none,
)

#set text(
  font: "Libertinus Serif",
  size: 12pt,
  lang: "uk",
  region: "UA",
  fill: black,
)

#let draw_tri(p1, p2, p3, st: 1.0pt + black) = {
  let (x1, y1) = p1
  let (x2, y2) = p2
  let (x3, y3) = p3
  let mx = calc.min(x1, x2, x3)
  let my = calc.min(y1, y2, y3)
  place(top + left, dx: mx * 1mm, dy: my * 1mm)[
    #polygon(
      stroke: st,
      fill: none,
      ((x1 - mx) * 1mm, (y1 - my) * 1mm),
      ((x2 - mx) * 1mm, (y2 - my) * 1mm),
      ((x3 - mx) * 1mm, (y3 - my) * 1mm),
    )
  ]
}

// ============================================================================
// АРКУШ 1/3 — ФІГ. 1 (СТРУКТУРНА БЛОК-СХЕМА СПОСОБУ, ПОЗИЦІЇ 1–10)
// ============================================================================
#align(center)[
  #v(6mm)
  #let bbox(num, label) = block(
    width: 132mm,
    inset: (x: 4mm, y: 3.2mm),
    stroke: 1.1pt + black,
    fill: white,
  )[
    #set par(justify: false, leading: 0.55em)
    #grid(
      columns: (14mm, 1fr),
      align: (center + horizon, left + horizon),
      [#box(stroke: 1pt + black, inset: 2mm)[#text(size: 13pt, weight: "bold")[#num]]],
      [#text(size: 11.5pt)[#label]]
    )
  ]
  #let arrow_down = block(above: 0pt, below: 0pt, height: 6.5mm)[
    #line(start: (0pt, 0pt), end: (0pt, 4.5mm), stroke: 1.1pt + black)
    #place(center + bottom)[#polygon(fill: black, (0mm, 0mm), (-1.6mm, -2.2mm), (1.6mm, -2.2mm))]
  ]

  #bbox("1", [Вхідний електронний документ та канонічна нормалізація потоку $M$])
  #arrow_down
  #bbox("2", [Паралельний мульти-геш комбінатор $H_("comb")$ (ГОСТ 34.311-95 $||$ ДСТУ 7564:2014 $||$ SHA-256)])
  #arrow_down
  #bbox("3", [Генерація підпису $(r, s)$ за ДСТУ 4145-2002 над $G F(2^(257))$ та вектора $V$])
  #arrow_down
  #grid(
    columns: (76mm, 8mm, 48mm),
    align: center + horizon,
    block(width: 76mm, inset: 3mm, stroke: 1.1pt + black)[
      #text(size: 12.5pt, weight: "bold")[(4)] Демультиплексор 256 бітів у 26 слів $w_0..w_(25)$ (по 10 бітів)
    ],
    [#text(size: 14pt, weight: "bold")[+]],
    block(width: 48mm, inset: 3mm, stroke: 1.1pt + black)[
      #text(size: 12.5pt, weight: "bold")[(5)] Ввід 16-бітного коду отримувача $"ID"_"rec"$
    ]
  )
  #arrow_down
  #bbox("6", [Блок симетричної модуляції 26+1 каналів решітки 9 трикутників ($Delta_("sym") = 0$)])
  #arrow_down
  #bbox("7", [Інжекція векторних операторів PDF/SVG у потік сторінки документа])
  #arrow_down
  #bbox("8", [Скріплення довгостроковим контейнером PAdES-B-LTA (`/ByteRange`, RFC 3161 TSP, `/DSS`)])
  #arrow_down
  #bbox("9", [Парсинг векторного потоку сторінки та перевірка симетрії $Delta_("sym") < 10^(-7)$])
  #arrow_down
  #bbox("10", [Бієктивна інверсія 256 бітів $hat(V)$, верифікація ДСТУ 4145-2002 та трасування $hat("ID")_"rec"$])

  #v(8mm)
  #text(size: 14pt, weight: "bold")[Фіг. 1]
]

#pagebreak()

// ============================================================================
// АРКУШ 2/3 — ФІГ. 2 (ПЛАНІМЕТРИЧНА РЕШІТКА 9 ТРИКУТНИКІВ, ПОЗИЦІЇ 11–17)
// ============================================================================
#align(center)[
  #v(8mm)
  #box(width: 155mm, height: 185mm, stroke: 1.1pt + black)[
    // Координатна сітка у мм відносно лівого верхнього кута боксу (центр у (77.5mm, 92.5mm))
    #let cx = 77.5
    #let cy = 92.5
    #let r = 56.0

    // Позиція 12 — Центральна вертикальна вісь симетрії x = C_x
    #place(top + left, dx: 77.5mm, dy: 10mm)[
      #line(start: (0mm, 0mm), end: (0mm, 165mm), stroke: (paint: black, thickness: 0.9pt, dash: "dashed"))
    ]

    // Позиція 11 — Обмежувальне коло R_0
    #place(top + left, dx: (cx - r) * 1mm, dy: (cy - r) * 1mm)[
      #circle(radius: r * 1mm, stroke: 1.2pt + black, fill: none)
    ]

    // 4 висхідні трикутники U1..U4 (Позиція 13) — усі строго вписані в коло R_0
    #draw_tri((77.5, 36.5), (30.5, 122.0), (124.5, 122.0), st: 1.0pt + black)
    #draw_tri((77.5, 49.0), (26.0, 108.0), (129.0, 108.0), st: 1.0pt + black)
    #draw_tri((77.5, 62.5), (39.5, 134.5), (115.5, 134.5), st: 1.0pt + black)
    #draw_tri((77.5, 75.5), (54.0, 115.0), (101.0, 115.0), st: 1.0pt + black)

    // 5 низхідних трикутників D1..D5 (Позиція 14 та внутрішній D5 — Позиція 15)
    #draw_tri((77.5, 148.5), (30.5, 63.0), (124.5, 63.0), st: 1.0pt + black)
    #draw_tri((77.5, 136.0), (26.0, 77.0), (129.0, 77.0), st: 1.0pt + black)
    #draw_tri((77.5, 122.5), (39.5, 50.5), (115.5, 50.5), st: 1.0pt + black)
    #draw_tri((77.5, 111.0), (51.0, 69.0), (104.0, 69.0), st: 1.0pt + black)
    // Внутрішній трикутник Бінду D5 (Позиція 15) — потовщений контур
    #draw_tri((77.5, 101.5), (65.5, 84.5), (89.5, 84.5), st: 1.6pt + black)

    // Центральна точка Бінду (Позиція 16)
    #place(top + left, dx: 76.2mm, dy: 91.2mm)[
      #circle(radius: 1.3mm, fill: black)
    ]

    // Позначки потрійних марма-перетинів (Позиція 17)
    #place(top + left, dx: 53.0mm, dy: 83.2mm)[#circle(radius: 1.2mm, stroke: 1pt + black, fill: white)]
    #place(top + left, dx: 99.6mm, dy: 83.2mm)[#circle(radius: 1.2mm, stroke: 1pt + black, fill: white)]
    #place(top + left, dx: 64.3mm, dy: 106.8mm)[#circle(radius: 1.2mm, stroke: 1pt + black, fill: white)]
    #place(top + left, dx: 88.3mm, dy: 106.8mm)[#circle(radius: 1.2mm, stroke: 1pt + black, fill: white)]

    // Цифрові виноски (висота шрифту 13pt >= 3.2 мм, усі поза контуром зображення з лініями-виносками)
    #place(top + left, dx: 80mm, dy: 11mm)[#text(size: 13pt, weight: "bold")[12 ($x = C_x$)]]
    #place(top + left, dx: 121mm, dy: 34mm)[#text(size: 13pt, weight: "bold")[11 ($R_0$)]]
    #place(top + left, dx: 112.5mm, dy: 50.5mm)[#line(start: (0mm, 0mm), end: (10mm, -10.5mm), stroke: 0.75pt + black)]

    #place(top + left, dx: 7mm, dy: 14mm)[#text(size: 13pt, weight: "bold")[13 ($Delta_("U1")..Delta_("U4")$)]]
    #place(top + left, dx: 41mm, dy: 18mm)[#line(start: (0mm, 0mm), end: (36.5mm, 18.5mm), stroke: 0.75pt + black)]

    #place(top + left, dx: 7mm, dy: 32mm)[#text(size: 12.5pt, weight: "bold")[17 (марма-вузли)]]
    #place(top + left, dx: 26mm, dy: 39mm)[#line(start: (0mm, 0mm), end: (27.5mm, 44.5mm), stroke: 0.75pt + black)]

    #place(top + left, dx: 7mm, dy: 152mm)[#text(size: 13pt, weight: "bold")[14 ($nabla_("D1")..nabla_("D5")$)]]
    #place(top + left, dx: 42mm, dy: 155mm)[#line(start: (0mm, 0mm), end: (35.5mm, -6.5mm), stroke: 0.75pt + black)]

    #place(top + left, dx: 116mm, dy: 136mm)[#text(size: 13pt, weight: "bold")[16 (Бінду)]]
    #place(top + left, dx: 78.5mm, dy: 93mm)[#line(start: (0mm, 0mm), end: (36mm, 45mm), stroke: 0.75pt + black)]

    #place(top + left, dx: 116mm, dy: 154mm)[#text(size: 13pt, weight: "bold")[15 ($nabla_("D5")$)]]
    #place(top + left, dx: 83.5mm, dy: 96.5mm)[#line(start: (0mm, 0mm), end: (31mm, 59.5mm), stroke: 0.75pt + black)]
  ]

  #v(8mm)
  #text(size: 14pt, weight: "bold")[Фіг. 2]
]

#pagebreak()

// ============================================================================
// АРКУШ 3/3 — ФІГ. 3 (СХЕМА 26+1 КАНАЛІВ МОДУЛЯЦІЇ ТА КАНАЛУ ТРАСУВАННЯ 18–22)
// ============================================================================
#align(center)[
  #v(6mm)
  #box(width: 155mm, height: 185mm, stroke: 1.1pt + black)[
    // Вісь симетрії 12
    #place(top + left, dx: 77.5mm, dy: 8mm)[
      #line(start: (0mm, 0mm), end: (0mm, 122mm), stroke: (paint: black, thickness: 0.9pt, dash: "dashed"))
    ]
    #place(top + left, dx: 80mm, dy: 9mm)[#text(size: 13pt, weight: "bold")[12 ($x = C_x$)]]

    // Модульований контур трикутника k (Позиції 18, 19, 20)
    #draw_tri((77.5, 28.0), (28.0, 98.0), (127.0, 98.0), st: 1.4pt + black)

    // Позиція 20 — Модульована ордината гострої вершини ay_k (канали w_18..w_25)
    #place(top + left, dx: 76mm, dy: 26.5mm)[#circle(radius: 1.5mm, fill: black)]
    #place(top + left, dx: 12mm, dy: 18mm)[
      #text(size: 13pt, weight: "bold")[20 ($tilde(a y)_k = a y_k + lambda delta_(17+k)$)]
    ]
    #place(top + left, dx: 62mm, dy: 23mm)[#line(start: (0mm, 0mm), end: (14mm, 4.5mm), stroke: 0.9pt + black)]

    // Позиція 18 — Антисиметричні бічні вершини (lx_k, rx_k) (канали w_0..w_8)
    #place(top + left, dx: 26.5mm, dy: 96.5mm)[#circle(radius: 1.5mm, fill: black)]
    #place(top + left, dx: 125.5mm, dy: 96.5mm)[#circle(radius: 1.5mm, fill: black)]
    #place(top + left, dx: 6mm, dy: 103mm)[
      #text(size: 12pt, weight: "bold")[18 ($tilde(l x)_k = l x_k + lambda delta_k$)]
    ]
    #place(top + left, dx: 96mm, dy: 103mm)[
      #text(size: 12pt, weight: "bold")[18 ($tilde(r x)_k = 2 C_x - tilde(l x)_k$)]
    ]

    // Позиція 19 — Модульована горизонтальна основа by_k (канали w_9..w_17)
    #place(top + left, dx: 48mm, dy: 114mm)[
      #box(fill: white, inset: 1.5pt)[#text(size: 12.5pt, weight: "bold")[19 ($tilde(b y)_k = b y_k + lambda delta_(9+k)$)]]
    ]
    #place(top + left, dx: 63mm, dy: 98mm)[#line(start: (0mm, 0mm), end: (0mm, 15mm), stroke: 0.8pt + black)]

    // Внутрішній трикутник Бінду D5 (Позиція 15) та вершина 27-го каналу (Позиція 21)
    #draw_tri((77.5, 82.0), (58.0, 54.0), (97.0, 54.0), st: 1.6pt + black)

    #place(top + left, dx: 75.8mm, dy: 80.3mm)[#rect(width: 3.4mm, height: 3.4mm, fill: black)]
    #place(top + left, dx: 98mm, dy: 44mm)[
      #box(fill: white, inset: 1.5pt)[#text(size: 12pt, weight: "bold")[21 (27-й канал $tilde(a y)_9$: $"ID"_"rec"$)]]
    ]
    #place(top + left, dx: 78.5mm, dy: 81.5mm)[#line(start: (0mm, 0mm), end: (25mm, -31mm), stroke: 0.8pt + black)]

    // Позиція 22 — Блок бієктивного декодера та звіту атрибуції витоку
    #place(top + left, dx: 14mm, dy: 132mm)[
      #block(width: 127mm, inset: 4mm, stroke: 1.2pt + black, fill: white)[
        #set par(justify: false, leading: 0.6em)
        #text(size: 13pt, weight: "bold")[(22) Блок бієктивного декодера та атрибуції копії:]\
        1. Відновлення 26 слів (260 бітів): $hat(w)_m = "round"(((tilde(z)_m - z_m) / (lambda dot 10^(-7)) + 1023) / 2) in [0, 1023] arrow.r hat(V)$\
        2. Трасування 27-го каналу: $hat("ID")_"rec" = "round"(((tilde(a y)_9 - a y_9) / (lambda dot 10^(-7)) + 65535) / 2) in [0, 65535]$
      ]
    ]
    #place(top + left, dx: 77.5mm, dy: 114mm)[
      #line(start: (0mm, 0mm), end: (0mm, 16mm), stroke: 1.1pt + black)
    ]
  ]

  #v(8mm)
  #text(size: 14pt, weight: "bold")[Фіг. 3]
]

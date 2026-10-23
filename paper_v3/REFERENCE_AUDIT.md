# Reference audit — v2.1 manuscript vs. resolvable records

**Date:** 2026-10-23 · **Method:** every DOI was resolved through `api.crossref.org/works/<DOI>`;
every title without a DOI was searched on Crossref (`query.bibliographic`) and OpenAlex
(`/works?search=`). A reference counts as **verified** only if a record with matching
title/authors/venue was returned. Standards and books are accepted from their issuing body.

## Verdict

**The v2.1 bibliography cannot be reused as-is.** Of 42 entries, at least **8 are unverifiable**
(no record in Crossref or OpenAlex under the claimed title/authors/venue), **1 DOI points to a
different record** (Huet), and **2 have the wrong venue** (Ohbuchi; Mladenov). Several "recent
SOTA" claims in Related Work are built on those unverifiable entries, so the novelty framing
must be rewritten together with the bibliography, not patched.

## Entry-by-entry status

| v2.1 | Claimed reference | Status | Action for v3 |
|---|---|---|---|
| [1] | eIDAS 910/2014 + 2024/1183 | OK | keep |
| [2] | UA Law 2155-VIII | OK | keep |
| [3] | ETSI EN 319 142-1 | OK | keep |
| [4] | ISO 32000-2:2020 | OK | keep |
| [5] | ETSI EN 319 122-1 | OK | keep |
| [6] | RFC 3161 | OK | keep |
| [7] | Kulaichev, IJHS 19(3):279–292 (1984) | **verified** (INSA PDF) | keep |
| [8] | Huet, TCS 281:609–628 (2002), DOI `10.1016/S0304-3975(02)00029-4` | **wrong DOI**: that DOI is an author index; the paper is `10.1016/S0304-3975(02)00028-2` | fix DOI |
| [9]–[13] | GOST 34.311, DSTU 7564, FIPS 180-4, RFC 6979, DSTU 4145 | OK | keep |
| [14] | Rao, IJHS 33(3):203–227 (1998) | **unverified** — no matching record found | remove unless a scan is produced |
| [15] | Ohbuchi et al., SMI **2002**, pp. 216–225 | wrong year/venue; real record is **SMI 2003**, DOI `10.1109/SMI.2003.1199619` | fix |
| [16]–[21] | Cox et al. book; Catalano–Fiore; Boneh–Franklin; Cox–Little–O'Shea; Richter-Gebert; Sturmfels | OK | keep |
| [22] | Mladenov et al., *1 Trillion Dollar Refund*, **NDSS 2019** | wrong venue: it is **CCS 2019**, DOI `10.1145/3319535.3339812` | fix |
| [23] | Mainka et al., *Shadow Attacks*, NDSS 2021 | OK (`10.14722/ndss.2021.24117`) | keep |
| [24] | Müller et al., CCS 2019 | OK (`10.1145/3319535.3354214`) | keep |
| [25] | Michon, *Construction of the Sri Yantra by Concurrency Optimization*, J. Recreational Mathematics and Computational Geometry 42(2), 2015 | **not found** in Crossref or OpenAlex; journal not traceable | **remove** |
| [26] | Bolt, Kay, Lu, *On the Geometric Rigidity…*, DCG 64(3), 2020 | **not found** | **remove** |
| [27] | Sturmfels, *Algorithms in Invariant Theory* | OK | keep |
| [28] | Peng, Long, Lin, TIFS 16:2400–2413 (2021), DOI `10.1109/TIFS.2021.3054531` | **DOI 404**, title not found; the real Peng/Lin/Zhang/Long paper is TIFS 2019, DOI `10.1109/TIFS.2019.2899520` (different title) | replace with `peng2019` |
| [29] | Peng, Zhang, Lin, Long, TDSC 20(4), 2023 | **not found** | **remove** |
| [30] | Wang, Peng, Long, JISA 68:103242, 2022 | **not found** | **remove** |
| [31] | Li, Ren, Zhu, Kes, JISA 75:103504, 2023 | **not found** | **remove** |
| [32] | Oliynykov et al., Kupyna, ePrint 2015/885 | OK (IACR ePrint) | keep |
| [33] | Zhang, Cao, Yin, Zhang, TMM 26, 2024 | **not found** | **remove** |
| [34] | Luo, Wang, Chang, Pattern Recognition 148, 2024 | **not found** | **remove** |
| [35] | Libert, Ramanna, Yung, ICALP 2016 | **real**; DOI `10.4230/LIPIcs.ICALP.2016.30` (add) | fix |
| [36] | Boneh, Drake, Fisch, Gabizon, CRYPTO 2021 | OK (`10.1007/978-3-030-84242-0_23`) | keep |
| [37] | Rohlmann et al., IEEE S&P 2021 | OK (`10.1109/SP40001.2021.00110`) | fix DOI |
| [38] | Gorbenko, *Applied Cryptology* (UA textbook) | accepted (book, no DOI) | keep |
| [39] | Hankerson, Menezes, Vanstone, *Guide to ECC* | OK | keep |
| [40] | Tardos, JACM 55(2):10 (2008) | OK (`10.1145/1346330.1346335`) | keep |
| [41] | Isobe, J. Cryptology 26(1):172–189 | OK (`10.1007/s00145-012-9118-5`) | fix year 2012/2013 |
| [42] | Muller et al., *Handbook of Floating-Point Arithmetic* | OK (book) | keep |

## Rules for v3 (enforced)

1. **No reference without a resolvable identifier** — DOI, ISBN, RFC/NIST/ETSI/ISO number, or an
   archived scan URL. Books and standards are the only exception to the DOI rule.
2. Every DOI is resolved programmatically before a draft is compiled; the audit script output is
   committed next to the bibliography.
3. **Related Work is rebuilt from the verified list** (`references.bib`, 44 entries): QIM/dither
   (Chen–Wornell 2001; Eggers 2003; Pérez-González 2004), spread-spectrum (Cox 1997),
   data hiding (Bender 1996), RDH (Tian 2003; Ni 2006; Thodi 2007), 2D vector graphics/maps
   (Wang 2014; Peng 2019; Doncel 2007; Li–Xu 2003; Hou 2014; Mouhamed 2012; Ohbuchi 1998/2003),
   PDF watermarking (Hatoum 2018), print-scan (He–Sun 2005), security (Cayre 2005; Yang 2018),
   PDF signature attacks (Mladenov 2019; Mainka 2021; Rohlmann 2021; Müller 2019), commitments /
   traitor tracing (Catalano–Fiore 2013; Boneh–Franklin 1999; Tardos 2008; Libert 2016; Boneh 2021),
   geometry (Kulaichev 1984 verified; Huet 2002 correct DOI), standards.
4. **Novelty statements must not depend on removed entries.** Any sentence of the form
   "unlike [28]-[34]…" is deleted; comparisons are phrased against verified baselines actually
   implemented in the evaluation.
5. **Residual risk:** references [14], [25], [26], [29]–[34] must never reappear; if a future
   draft cites them, it fails the audit gate.

## Consequence for the target-journal history

JISA's "superficial" verdict and SIGPRO's "clear from the references" are consistent with a
reference list that mixed verified classics with unverifiable "recent SOTA" claims. The v3
bibliography is therefore a **correctness prerequisite**, not a stylistic preference: no
submission before `references.bib` passes the audit gate.

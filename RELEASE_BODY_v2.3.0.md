# marma-crypto-watermark v2.3.0

Major mathematical & operational release of **Marma-Crypto** (`v2.3.0`, Debian revision `2.3.0-1`): integrates **Stealth (0% Visible) Stamping** (`--mode stealth` / `--seal-pages none`) across PDF, DOCX, Deal-Room batch distribution, and GNOME Files (Nautilus), together with the **Subhash Kak 41-Paper Vedic Cryptographic Synthesis (`kak_synthesis_v23.py`, 15 mathematical invariants)**.

## Highlights
- **Stealth / Covert Stamping (`--mode stealth`, `--seal-pages none`)** — 100% visually invisible stamping for **PDF** (`stroke_opacity=0.0` vector carrier + cryptographic metadata + PAdES) and **DOCX** (zero visible images, hidden 1pt `MARMA_SEAL_PACKET` + CAdES), preserving full 256-bit `DSTU 4145-2002` verification, 54-Marma non-linear parity checks, and Canary recipient leak-tracing (`D5.ay`).
- **Nautilus Right-Click Action (`1e_stamp_stealth.sh`)** — new `🕵️ Підписати скрито (Stealth · 0% видимості + Canary)` / `🕵️ Sign Stealth (0% Visible Marks + Canary)` menu item and root quick action (`🕵️ Швидко: скритий підпис (Stealth)`), plus `"none"` option in `12_seal_pages.sh`.
- **Triadic Recursion (`INV_THREE_BODIES_NINE_CIRCUITS` / `INV_KAK_LMH_27`)** — implements Prof. Subhash Kak's (2024) *Three Bodies, Seven Centres, and Nine Circuits* triadic partition of the 9 *Śrī Yantra* triangles:
  - $L = (B_1, C_1, B_2) \equiv (D_1, U_1, D_2)$ (9 QIM slots),
  - $M = (B_3, B_4, C_2) \equiv (D_3, D_4, U_2)$ (9 QIM slots),
  - $H = (B_5, C_3, C_4) \equiv (D_5, U_3, U_4)$ (9 QIM slots, with $B_5 = D_5$ around the *Bindu* carrying the 27th Forensic Canary channel `D5.ay`).
- **Subhash Kak Synthesis Engine (`marma_crypto.kak_synthesis_v23`)** — 54-Marma non-linear Tanner graph parity check (`verify_sri_yantra_54_marma_concurrency`), Fermat prime $p = 257$ $d$-sequence QIM permutation & dither (`derive_kak_dsequence_qim_schedule_v23`), Parakh–Kak 23-bit zero-distortion recursive attribution (`embed_recursive_attribution_23bit_v23`), Penumarthi–Kak dual-layer public/forensic watermarking (`/v2.3/augmented-stamp`, `/v2.3/augmented-verify`), 64 Primitive Pythagorean Triples on the rational unit circle, and Nārāyaṇa universal prefix coding.

## Verification
- **Unit & Cross-Verification Suite:** **83/83 PASS** (`unittest discover -s tests -v`), including all **15/15** Subhash Kak mathematical invariants and **41/41** corpus cross-verification checks.
- **Debian Package & Nautilus Deploy (`./build.sh --test`):** **PASS** (`marma-crypto-watermark_2.3.0-1_all.deb`, 52 files, isolated self-test + `doctor` preflight + Nautilus menu refresh).

## Install
```bash
sudo dpkg -i marma-crypto-watermark_2.3.0-1_all.deb
marma-config --refresh
marma-watermark --version   # marma-watermark 2.3.0
```

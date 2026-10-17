# 🔱 Marma-Crypto Protocol (`v1.2.0`)

**Cryptographic Geometric Watermarking and Sovereign Document Sealing via Sri Yantra Nonlinear Concurrency and Elliptic Curves over $\mathbb{F}_{2^{257}}$ (DSTU 4145-2002)**

*Криптографічно-геометричний водяний знак та суверенне запечатування документів на основі нелінійної планіметрії Шрі Янтри та еліптичних кривих ДСТУ 4145-2002*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23429018.svg)](https://doi.org/10.5281/zenodo.23429018)
[![Zenodo Record](https://img.shields.io/badge/CERN_Zenodo-23429018-024289.svg)](https://zenodo.org/records/23429018)
[![License: Apache 2.0](https://img.shields.io/badge/Code_License-Apache_2.0-blue.svg)](LICENSE)
[![Whitepaper: CC BY 4.0](https://img.shields.io/badge/Whitepaper-CC_BY_4.0-DCA900.svg)](whitepaper/Marma_Crypto_Whitepaper_EN.pdf)
[![Standard: DSTU 4145-2002](https://img.shields.io/badge/Crypto-DSTU_4145--2002_%7C_GF(2%5E257)-1b2a4a.svg)](src/dstu4145_bridge.js)
[![Platform: Debian / GNOME](https://img.shields.io/badge/Platform-Debian_Linux_%7C_GTK4_Adwaita-8a6206.svg)](build.sh)

---

## 📄 Official Whitepapers & Self-Referential Cryptographic Proofs

Both editions of the Whitepaper are sealed using the **Marma-Crypto v1.2.0** protocol they specify, and anchored in the Bitcoin blockchain via OpenTimestamps:

| Artifact | Link | Content SHA-256 |
| :--- | :--- | :--- |
| **English Whitepaper (PDF)** | [`whitepaper/Marma_Crypto_Whitepaper_EN.pdf`](whitepaper/Marma_Crypto_Whitepaper_EN.pdf) | `4b2168534e10449a892a551278b404814fddb01bfb03c446f84dc014fa8c96cd` |
| **Ukrainian Whitepaper (PDF)** | [`whitepaper/Marma_Crypto_Whitepaper_UA.pdf`](whitepaper/Marma_Crypto_Whitepaper_UA.pdf) | `c36cb1d8792286c46193cbb5e3eea61d3bc669f983258869b5e7a8b93fd17ff5` |
| **EN Verification Protocol (PDF)** | [`whitepaper/Marma_Crypto_Whitepaper_EN_PROTOCOL.pdf`](whitepaper/Marma_Crypto_Whitepaper_EN_PROTOCOL.pdf) | Zero-tolerance 9-triangle audit report |
| **UA Verification Protocol (PDF)** | [`whitepaper/Marma_Crypto_Whitepaper_UA_PROTOCOL.pdf`](whitepaper/Marma_Crypto_Whitepaper_UA_PROTOCOL.pdf) | Офіційний протокол перевірки 9 трикутників |
| **Signed Reference Sri Yantra (SVG)** | [`whitepaper/sri_yantra_whitepaper_diagram.svg`](whitepaper/sri_yantra_whitepaper_diagram.svg) | `1dfebfa9a7154973512e3933d6a0c7a556319c6b7b3900dcce1f0f6eef01bbce` |
| **Authorship Manifest & OTS Proofs** | [`whitepaper/AUTHORSHIP_MANIFEST.txt`](whitepaper/AUTHORSHIP_MANIFEST.txt) | Anchored via `a.pool.opentimestamps.org` (`.ots`) |

---

## 🧮 Mathematical & Cryptographic Overview

Conventional digital signatures detach the binary PKCS#7 container from the visual rendering of a page, whereas raster watermarks degrade under scaling and vector conversion. **Marma-Crypto** solves this by uniting two mathematical domains:

1. **Nonlinear 9-Triangle Concurrency of the Sri Yantra (*Nava-Cakra*, Kulaichev 1984):**
   Four upward-pointing *Śiva* triangles ($\Delta_{\text{U1}}\dots\Delta_{\text{U4}}$) and five downward-pointing *Śakti* triangles ($\nabla_{\text{D1}}\dots\nabla_{\text{D5}}$) intersect to form **43 sub-triangles** and **54 triple concurrency nodes (*marmas*)** governed by $\det[A_i, B_i, C_i] = 0$.
2. **Elliptic Curve Signature Mapping over $\mathbb{F}_{2^{257}}$ (DSTU 4145-2002):**
   The document content $M$ is hashed via **GOST 34.311-95**, **DSTU 7564:2014 ("Kupyna-256")**, and **SHA-256**. A deterministic signature vector $(r, s)$ is computed on the polynomial-basis elliptic curve `DSTU_PB_257` ($y^2 + xy = x^3 + b$ over $\mathbb{F}_{2^{257}} = \mathbb{F}_2[t]/(t^{257}+t^{12}+1)$) using RFC 6979 nonce derivation.
3. **Bilateral Symmetry-Preserving Micro-Coordinate Modulation ($\pm 10^{-5}$):**
   The signature $(r, s)$ is bijectively quantized into a 9-dimensional perturbation vector $\vec{\delta} = (\delta_1, \dots, \delta_9) \in [-10^{-5}, +10^{-5}]^9$ applied to the 9 triangles:
   $$\tilde{y}_{k,\text{base}} = y_{k,\text{base}} + \delta_k, \quad \tilde{y}_{k,\text{apex}} = y_{k,\text{apex}} - \delta_k, \quad \tilde{lx}_k = lx_k - \frac{\delta_k}{2}, \quad \tilde{rx}_k = rx_k + \frac{\delta_k}{2}$$
   This identically preserves the bilateral symmetry invariant $\tilde{lx}_k + \tilde{rx}_k = 2 C_x = 600.000000000000$ ($\Delta_{\text{sym}} < 10^{-12}$) while enabling instantaneous detection of any single-byte text edit or geometric displacement exceeding $10^{-7}$ coordinate units.

---

## 🚀 Quick Start & Independent Verification

### 1. Verify the Signed Whitepapers Right Now
```bash
python3 src/marma_watermark.py verify whitepaper/Marma_Crypto_Whitepaper_EN.pdf
python3 src/marma_watermark.py verify whitepaper/Marma_Crypto_Whitepaper_UA.pdf
```

### 2. Run the Full Cryptographic Self-Test Suite (`.svg`, `.pdf`, `.docx`, Tamper Rejection)
```bash
python3 src/marma_watermark.py selftest
```

### 3. Build and Install the Debian Package (`.deb`) with GNOME Files (Nautilus) Integration
```bash
./build.sh --test
sudo dpkg -i dist/marma-crypto-watermark_1.2.0-1_all.deb
```

---

## 📜 Author & Citation

* **Author:** **Yaroslav V. Baienko** (*Баєнко Ярослав Володимирович*)
* **Affiliation:** Attorney-at-Law, Legal Engineer & Applied Cryptography Researcher (Ukraine)
* **GPG Fingerprint (RSA-4096):** `3D5A ACFD E32C 98FE 8819 9D47 D2A2 C1C4 9164 673B`
* **Qualified Certificate Serial (КНЕДП):** `10FF6F932221FA00CB4407000000000130616768`

```bibtex
@techreport{baienko2026marmacrypto,
  author      = {Baienko, Yaroslav V.},
  title       = {Marma-Crypto: A Cryptographic Geometric Watermarking and Sovereign Document Sealing Protocol via Sri Yantra Nonlinear Concurrency and Elliptic Curves over GF(2\^{}257) (DSTU 4145-2002)},
  year        = {2026},
  institution = {Independent Legal Engineering \& Applied Cryptography Research},
  number      = {EDU-VEDI-WP-2026-01},
  doi         = {10.5281/zenodo.23429018},
  url         = {https://zenodo.org/records/23429018}
}
```

## ⚖️ License

* **Software & Source Code (`src/`, `bin/`, `nautilus-scripts/`):** Licensed under the **Apache License, Version 2.0** (including Explicit Patent Grant & Attribution Clauses).
* **Whitepapers & Mathematical Specification (`whitepaper/`):** Licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

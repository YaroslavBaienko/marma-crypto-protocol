# 🔱 Marma-Crypto Protocol — Strategic Roadmap & EU Grant Plan (`RES-MARMA-CRYPTO`)

> **Current Production Release:** `v2.1.0` (`marma-crypto-watermark_2.1.0-1_all.deb` · Python SDK `marma_crypto v2.1.0`)
> **Patent Status:** **`Patent Pending — UKRNOIVI Invention Application No. a 2026 06266`** (`Вх-72320/2026` · Fee Receipt `Вх-72403/2026`)
> **Peer-Review Status:** **Elsevier *Signal Processing* (`SIGPRO-D-26-04464`)** · **SSRN eJournal `Vol. 11, No. 189` (`10.2139/ssrn.7631458`)**
> **CERN Zenodo DOI:** [`10.5281/zenodo.23560975`](https://doi.org/10.5281/zenodo.23560975) (`v5` · Concept DOI: `10.5281/zenodo.23429017`)
> **Software Heritage (ISO/IEC 18670 SWHID):** `swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1` (`swh:1:rev:9101009d6e995adf56cd1a85c71291484d89d18c`)
> **Live Client-Side Deal-Room Studio & Verifier:** [`https://yaroslavbaienko.github.io/marma-crypto-protocol/`](https://yaroslavbaienko.github.io/marma-crypto-protocol/)

---

## ✅ Phase 1, 2 & 2.1 — Completed (Core Protocol, `v2.1.0` Universal/Optical/API Suite & Patent Pending)

1. **Mathematical & Cryptographic Core (`v1.0.0` $\rightarrow$ `v2.1.0`):**
   - Dual-layer binding between the 54 triple-intersection concurrency equations of the 9-triangle Sri Yantra (Kulaichev 1984 / Huet 2002) and Ukrainian National Standard **DSTU 4145-2002** over $GF(2^{257})$ (`PAdES-B-LTA` / `CAdES-X-Long` + `RFC 3161 TSP`).
   - **Full 266-Bit Keyed Dithered QIM $(d_K, \pi_K)$:** 26 independent 10-bit symmetric coordinate channels + 27th 10-bit canary channel (`D5.ay`, $18\text{ nm}$ step) with exact bilateral symmetry preservation ($lx_k + rx_k = 2 C_x$, $\Delta_{\text{sym}} = 0.0$) and zero Kullback–Leibler divergence ($D_{\text{KL}}=0$, Theorem 5).
   - **Parallel Multi-Hash Combiner:** $H_{\text{comb}} = \text{SHA-256}(\text{GOST 34.311-95} \parallel \text{DSTU 7564:2014 Kupyna-256} \parallel \text{FIPS 180-4 SHA-256})$.
   - **`Marma-Universal` (`src/marma_crypto/universal_qim.py`):** Generalized 27-DOF Keyed Dithered QIM for arbitrary vector contours ($\ge 14$ vertices) and built-in sovereign/enterprise templates (`sri-yantra`, `tryzub` Ukrainian State Trident, `corporate-shield`, `cad-polygon`).
   - **`Marma-Optical` (`src/marma_crypto/optical_ecc.py`):** 32-sector Optical Lotus Ring (`[32, 16, d_min=8]` extended Reed–Muller/BCH block code + Soft-Decision ML Pearson correlation decoder) surviving 216 DPI screen-capture, Gaussian blur, sensor noise, and JPEG compression (`0.0% BER`).
   - **Deal-Room Batch SDK & REST API (`src/marma_crypto/api_server.py`):** $O(1)$-amortized deal-room batch sealing (`1..1,024` recipients) and zero-dependency HTTP JSON microservice (`marma-watermark serve-api`).
2. **Dual-Runtime Execution (Client-Side Browser Studio + Debian Linux CLI/GUI):**
   - Zero-server WebCrypto/JS Document Sealer, Deal-Room Canary Studio & Verifier (`docs/index.html`) with **1-Click Deal-Room Leak Simulation**.
   - Production Debian/Ubuntu `.deb` package (`marma-crypto-watermark_2.1.0-1_all.deb`) with 12 GNOME Nautilus actions (`0_help.sh` – `11_trace_leak_optical.sh`) and **40 automated tests (`OK`)** across 4 test suites.
3. **Institutional Archival, Patent Filing & Peer Review:**
   - **UKRNOIVI 20-Year Invention Patent Application `No. a 2026 06266`** (`Вх-72320/2026`, filed 2026-10-19; fee receipt `Вх-72403/2026` registered 2026-10-20).
   - **Elsevier *Signal Processing* (`SIGPRO-D-26-04464`)** formal peer-review submission (`21 pp.`, Theorems 1–5) + **SSRN eJournal `Vol. 11, No. 189` (`10.2139/ssrn.7631458`)** + **CERN Zenodo `v5` (`10.5281/zenodo.23560975`)**.

---

## 🇪🇺 Phase 3 — EU Open-Source Cryptography Grants Roadmap (€25,000 – €50,000)

### 1. Primary Target: NLnet Foundation — NGI0 Entrust & NGI0 Commons Fund
- **Portal:** `https://nlnet.nl/entrust/` / `https://nlnet.nl/commonsfund/`
- **Funding Range:** €5,000 – €50,000 (non-dilutive EU Next Generation Internet grant for Apache 2.0 open-source privacy & document trustworthiness tools; target request: **€27,000** across 4 milestones).
- **Grant Proposal Title:**
  *“Marma-Crypto: Sovereign Zero-Server Cryptographic Document Sealing, Bijective Vector Watermarking, and Sub-Micron Canary Leak-Tracing for Public-Interest Documents”*
- **Deliverable Milestones (Pay-per-Milestone Structure):**
  - **Milestone 1 (€8,000) — Print-Scan Resistant Projective Invariant Recovery:**
    Implement projective cross-ratio & Crofton–Chasles invariant recovery from rasterized/photographed paper scans of sealed Sri Yantra watermarks (`marma-watermark scan-verify`).
  - **Milestone 2 (€8,000) — Multi-Standard eIDAS (ECDSA P-256 / Ed25519) + DSTU 4145-2002 WebAssembly SDK & Browser Extension:**
    Universal WebAssembly library (`@marma-crypto/wasm`) and Manifest V3 browser extension for automatic inline verification of sealed PDFs and SVGs across European eIDAS and Ukrainian QES standards.
  - **Milestone 3 (€6,000) — Self-Hosted Nextcloud, LibreOffice & Thunderbird Plugins:**
    Turnkey open-source plugins enabling journalists, NGOs, law clinics, and researchers to automatically seal outgoing PDFs/DOCX with recipient-specific Canary tags.
  - **Milestone 4 (€5,000) — Formal Security Audit, IETF Internet-Draft & Upstream Debian Packaging:**
    Publish formal specification as an IETF Informational Internet-Draft (`draft-baienko-marma-crypto-00`), complete external cryptographic review, and submit `marma-crypto-watermark` to upstream Debian `unstable/testing`.

### 2. Secondary Targets:
- **Open Technology Fund (OTF — FOSS Sustainability & Security Lab):** Zero-egress browser canary leak-tracing for investigative journalism and human rights documentation.
- **Horizon Europe / EIC & OpenAIRE CoARA Open Science Pilots:** Cryptographic integrity verification for open-access scientific preprints and datasets.

---

## 🚀 Phase 4 — Distribution, Thought Leadership & Enterprise B2B Adoption

1. **Flagship Case-Study Publication (LinkedIn EN & Facebook UA):**
   - Showcase the **1-Click Deal-Room Leak Simulation** for M&A counsel, investment bankers, and Web3/RWA founders alongside CERN Zenodo first-day traction (257+ views / 44+ downloads).
2. **Engineering Community Launch (`Show HN` & Technical Subreddits):**
   - Launch `Show HN` on Hacker News during US East Coast morning peak (16:00 Kyiv / 09:00 EST) and engage in technical discussions on `r/SideProject`, `r/LegalTech`, and `r/cryptography`.
3. **Enterprise & LegalTech B2B Pilots (GOLAW Digital Economy & Litigation):**
   - Deploy custom corporate geometric seals and Deal-Room Canary protection for high-stakes M&A transactions, RWA tokenization certificates (MiCA), and forensic electronic evidence reports.

---

## 🛡️ Phase 5 — Sovereign Patent & International Priority Plan (`docs/PATENT_STRATEGY_UA_US.md`)

> **Canonical Strategy Document:** [`docs/PATENT_STRATEGY_UA_US.md`](docs/PATENT_STRATEGY_UA_US.md) · **Calendar (`.ics`):** [`docs/marma_ukrnoivi_patent_schedule.ics`](docs/marma_ukrnoivi_patent_schedule.ics)
> **First Public Disclosure Date (Prior Art Anchor):** `2026-10-17` (CERN Zenodo `10.5281/zenodo.23429018`)
> **STATUS UPDATE (2026-10-22) — the application is already filed; milestones P1/P2 below are historical:**
> Invention application `a 2026 06266` (`Вх-72320/2026`) was filed **2026-10-19** (fee receipt `Вх-72403/2026`, 2026-10-20).
> Recomputed deadlines: Art. 37 state-secrecy clearance ≈ **2027-01-19**; Paris/PCT priority **2027-10-19** (12 months from the filing);
> 6-month inventor's grace for the *filed* subject matter — **2027-04-17**.
> **Unprotected `v2.1.0` delta** (Keyed Dithered QIM / Theorem 5, `Marma-Universal` emblems, `Marma-Optical` ECC, Deal-Room REST API) was first publicly disclosed **2026-10-21** and is **not described** in the filed application, so the patent does not cover it.
> Decision on a separate application is required by **2027-04-21** (UA 6-month grace) / **2027-10-21** (US, `35 U.S.C. § 102(b)(1)(A)`); the EPO has no general grace period, so those features are already unpatentable there unless they are supported by the pending application (they are not).
> Until that decision, do not publish further technical details of the `v2.1.0` delta.
>
> **Why UKRNOIVI First (Mandatory & Optimal):**
> 1. **Ukrainian Mandatory First-Filing Rule (`Art. 37 of Law No. 3687-XII`):** Inventions created in Ukraine by Ukrainian citizens must first be filed in UKRNOIVI (followed by a 3-month state-secrecy clearance window) before any foreign patent filing.
> 2. **USPTO Foreign Domicile Rule (`37 CFR § 1.31(a)(2)`, effective July 20, 2026):** Foreign-domiciled applicants can no longer sign Micro Entity certifications (`Form PTO/SB/15A`) or ADS forms *pro se* in the USPTO without hiring a US patent attorney ($350–$600).
> 3. **Paris Convention & AIA Effective Filing Date Synergy (`Paris Convention Art. 4` + `35 U.S.C. §§ 100(i)(1)(B), 102(b)(1)(A), 119(a)`):** Filing the Ukrainian invention application in **UKRNOIVI** (self-filed via QES at `sis.nipo.gov.ua` for **64 UAH / ~$1.50** under CMU Resolution No. 1716, 5% individual inventor rate + 20% e-filing discount) automatically establishes the **Effective Filing Date for the United States**, locks in the US 1-year grace period against the `2026-10-17` Zenodo disclosure, grants **12 months of international priority worldwide (until `2027-10-19`)**, and immediately confers legal **`Patent Pending (Paris Convention Art. 4 / 35 U.S.C. § 119)`** status at zero attorney cost.

| Date | Milestone / Deadline | Jurisdiction, Fee & Legal Effect |
| :--- | :--- | :--- |
| **`2026-10-19`** ✅ | **Filed (done)** | Invention application `a 2026 06266` filed with UKRNOIVI via SEV ZES (`Вх-72320/2026`); filing-fee receipt `Вх-72403/2026` registered 2026-10-20. Paris Convention priority date established. |
| **`2027-01-19`** | **Art. 37 clearance (T+90 days)** | Completion of the 3-month state-secrecy review under Art. 37 of Law No. 3687-XII — foreign / PCT filings become lawful. |
| **`2027-04-17`** | **🚨 6-month inventor grace (filed subject matter)** | Final day of the 6-month novelty grace under Art. 6(6) of Law No. 3687-XII, counted from the 2026-10-17 disclosure. |
| **`2027-04-21`** | **🚨 Decision: separate application for the `v2.1.0` delta** | Keyed Dithered QIM (Theorem 5), `Marma-Universal`, `Marma-Optical` and the Deal-Room API were first disclosed 2026-10-21 and are **not covered** by the filed claims; a separate Ukrainian application must be filed by this date (6-month grace). |
| **`2027-10-19`** | **🚨 Paris / PCT priority deadline** | 12 months from the 2026-10-19 UKRNOIVI filing (`Paris Convention Art. 4`, `35 U.S.C. §§ 100(i)(1)(B), 119(a)`) for USPTO / PCT entry, limited to subject matter disclosed in the filed application. |
| **`2027-10-21`** | **⚠️ US grace deadline for the `v2.1.0` delta** | 1-year inventor grace under `35 U.S.C. § 102(b)(1)(A)` for features first disclosed 2026-10-21 (the EPO has no general grace — those features are already unpatentable there). |



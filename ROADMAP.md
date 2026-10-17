# 🔱 Marma-Crypto Protocol — Strategic Roadmap & EU Grant Plan (`RES-MARMA-CRYPTO`)

> **Current Production Release:** `v1.3.0` (`marma-crypto-watermark_1.3.0-1_all.deb`)
> **CERN Zenodo DOI:** [`10.5281/zenodo.23436152`](https://doi.org/10.5281/zenodo.23436152) (Concept DOI: `10.5281/zenodo.23429017`)
> **Software Heritage (ISO/IEC 18670 SWHID):** `swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1` (`swh:1:rev:9101009d6e995adf56cd1a85c71291484d89d18c`)
> **Live Client-Side Deal-Room Studio & Verifier:** [`https://yaroslavbaienko.github.io/marma-crypto-protocol/`](https://yaroslavbaienko.github.io/marma-crypto-protocol/)

---

## ✅ Phase 1 & 2 — Completed (Core Protocol, `v1.3.0` Studio & Prior Art Triad)

1. **Mathematical & Cryptographic Core (`v1.0.0` $\rightarrow$ `v1.3.0`):**
   - Dual-layer binding between the 54 triple-intersection concurrency equations of the 9-triangle Sri Yantra (Kulaichev 1984 / Huet 2002) and Ukrainian National Standard **DSTU 4145-2002** over $GF(2^{257})$ (`PAdES-B-LTA` / `CAdES-X-Long` + `RFC 3161 TSP`).
   - **Full 256-Bit Bijective Coordinate Inversion:** 26 independent 10-bit symmetric coordinate channels ($260\text{ bits} \ge 256\text{ bits}$) with exact bilateral symmetry preservation ($lx_k + rx_k = 2 C_x$, $\Delta_{\text{sym}} = 0.0$).
   - **Parallel Multi-Hash Combiner:** $H_{\text{comb}} = \text{SHA-256}(\text{GOST 34.311-95} \parallel \text{DSTU 7564:2014 Kupyna-256} \parallel \text{FIPS 180-4 SHA-256})$.
   - **27th Symmetric Channel — Steganographic Canary Leak-Tracing (`D5.ay`, $18\text{ nm}$ step):** Recipient-specific copy tagging (`--recipient-id`) and deterministic leak attribution (`marma-watermark trace`).
2. **Dual-Runtime Execution (Client-Side Browser Studio + Debian Linux CLI/GUI):**
   - Zero-server WebCrypto/JS Document Sealer, Deal-Room Canary Studio & Verifier (`docs/index.html`) with **1-Click Deal-Room Leak Simulation**.
   - Production Debian/Ubuntu `.deb` package (`marma-crypto-watermark_1.3.0-1_all.deb`) with GNOME Nautilus integration and 12 cross-runtime automated test suites (`tests/test_marma_cross_verification.py`).
3. **Institutional Archival & Prior Art Triad:**
   - Self-referential hardware QES (`PAdES-LTA`) on both EN and UA Whitepapers.
   - CERN Zenodo deposition (`10.5281/zenodo.23436152`) + OpenAIRE Research Graph indexing.
   - UNESCO / Inria Software Heritage permanent Merkle DAG snapshot (`swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1`).

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

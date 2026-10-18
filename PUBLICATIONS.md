# Marma-Crypto Protocol — Canonical Registry of Versions, Archival Identifiers & Publications

**Author:** Yaroslav V. Baienko (Advocate, Master of Laws, M.Sc. in Computer Science)  
**ORCID:** [`0009-0006-7498-2133`](https://orcid.org/0009-0006-7498-2133)  
**OpenPGP Fingerprint (RSA-4096):** `3D5A ACFD E32C 98FE 8819 9D47 D2A2 C1C4 9164 673B`  
**Qualified X.509 Certificate Serial (DSTU 4145-2002 / KNEDP DIIA):** `10FF6F932221FA00CB4407000000000130616768`

---

## 1. Release Versions & Evolution Matrix

| Version | Release Date | Edition Title | Key Mathematical & Engineering Additions | Package / Tag |
|---|---|---|---|---|
| **v1.0.0 – v1.2.0** | 2026-10-17 | Initial Specification & Debian Package | 9-triangle Sri Yantra geometric generator, 24-bit quantizer $K=(k_0,k_1,k_2,k_3)$, DSTU 4145-2002 / PAdES-B-LTA / CAdES-X-Long integration, initial `.deb` package. | `v1.0.0` / `v1.2.0` · [`10.5281/zenodo.23429018`](https://doi.org/10.5281/zenodo.23429018) |
| **v1.2.1** | 2026-10-17 | Universal Academic Edition | Formal proof of **Theorem 1 (Impossibility of Classical Euclidean Sri Yantra in PDF)**, 54-marma Kulaichev–Yue non-linear coupled ensemble ($4,096$ states, $\Delta E \approx 6.13 \times 10^{-11}\text{ rad} < \varepsilon_{\text{float64}}$), 9-suite cross-verification harness (`euscp.so` + `pdfs.so`). | [`v1.2.1`](https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/v1.2.1) · [`10.5281/zenodo.23436152`](https://doi.org/10.5281/zenodo.23436152) |
| **v1.3.0** | 2026-10-17 | 256-Bit Bijective Marma Edition & Canary Studio | Full **256-bit bijective vertex micro-perturbation codec** (`24 × 10-bit + 2 × 8-bit = 256 bits`), parallel cryptographic combiner $\text{SHA256}(\text{GOST} \parallel \text{Kupyna} \parallel \text{SHA256})$, **27th forensic canary channel (`D5.ay`, $18\text{ nm}$ step)** for deal-room leak attribution (`recipient_id 0..1023`), client-side browser PDF/SVG Sealer & Verifier. | [`v1.3.0`](https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/tag/v1.3.0) · [`swh:1:snp:dcae02ea...`](https://archive.softwareheritage.org/swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1;origin=https://github.com/YaroslavBaienko/marma-crypto-protocol) |
| **v1.3.0-1** | 2026-10-18 | Edge-Case Hardening & 12-Suite Bidirectional Release | Full XML entity escaping (`&`, `"`, `<`, `>`, `'`), UTF-8 Cyrillic manifest support, **12-suite cross-verification test harness** (`test_12_browser_sealer_to_python_cli_bidirectional_parity`), `CITATION.cff`, `codemeta.json`, and EU Grant Roadmap (`ROADMAP.md`). | [`marma-crypto-watermark_1.3.0-1_all.deb`](https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/download/v1.3.0/marma-crypto-watermark_1.3.0-1_all.deb) |

---

## 2. Scientific & Institutional Archival Identifiers (Prior Art)

| Institution / Registry | Identifier / Record | Direct URL | Role / Standard |
|---|---|---|---|
| **CERN Zenodo (Concept DOI — All Versions)** | `10.5281/zenodo.23429017` | https://doi.org/10.5281/zenodo.23429017 | Always resolves to the latest version of the specification (334+ views, 59+ downloads) |
| **CERN Zenodo — Version 1 (`v1.2.0`)** | `10.5281/zenodo.23429018` | https://doi.org/10.5281/zenodo.23429018 | Initial Defensive Prior Art deposit (2026-10-17) |
| **CERN Zenodo — Version 2 (`v1.2.1` + `v1.3.0` SWHID link)** | `10.5281/zenodo.23436152` | https://doi.org/10.5281/zenodo.23436152 | Universal Academic Edition (EN + UA PDFs + CAdES `.p7s` + OpenTimestamps `.ots` + Software Heritage SWHID; submitted to Zenodo Communities: *CiphIR — Bridging Cryptography and Information Security* & *CyberSafeNet*) |
| **UNESCO / Inria Software Heritage (`marma-crypto-protocol` Snapshot)** | `swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1` | https://archive.softwareheritage.org/swh:1:snp:dcae02ea5d13bb6aa6a72b2624184c961e44c3a1;origin=https://github.com/YaroslavBaienko/marma-crypto-protocol | ISO/IEC 18670 Merkle DAG repository snapshot |
| **UNESCO / Inria Software Heritage (`marma-crypto-protocol` Revision)** | `swh:1:rev:9101009d6e995adf56cd1a85c71291484d89d18c` | https://archive.softwareheritage.org/swh:1:rev:9101009d6e995adf56cd1a85c71291484d89d18c | ISO/IEC 18670 immutable commit revision |
| **UNESCO / Inria Software Heritage (`marma-crypto-protocol` Directory)** | `swh:1:dir:42b5547ee94691ccb541e10df453c2997e5cb302` | https://archive.softwareheritage.org/swh:1:dir:42b5547ee94691ccb541e10df453c2997e5cb302 | ISO/IEC 18670 root source tree |
| **UNESCO / Inria Software Heritage (`legaltech` APT Repo Snapshot)** | `swh:1:snp:2c6f70446da45cc2a48e64327d772577f29d01e1` | https://archive.softwareheritage.org/swh:1:snp:2c6f70446da45cc2a48e64327d772577f29d01e1;origin=https://github.com/YaroslavBaienko/legaltech | ISO/IEC 18670 snapshot of Debian APT ecosystem |
| **IACR Cryptology ePrint Archive** | Submission `xxxx/112645` (Category: *Cryptographic protocols*) | https://eprint.iacr.org | International Association for Cryptologic Research preprint registry (submitted 2026-10-19, awaiting editorial review) |
| **Elsevier SSRN (Legal & Computer Science Research Networks)** | `SSRN Abstract ID: 7631458` | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7631458 | Law & Technology / Computer Science eJournals (submitted 2026-10-19, `Public View: Yes`, `CC BY 4.0`) |
| **ResearchGate** | Researcher Profile & Preprint Onboarding | https://www.researchgate.net | Submitted 2026-10-19 (linked with ORCID `0009-0006-7498-2133`, Zenodo DOI `10.5281/zenodo.23436152`, SSRN `7631458`; awaiting account approval) |
| **Academia.edu** | Published Paper (`Yaroslav Baienko`) | https://www.academia.edu | Published 2026-10-19 (*2026 • CERN Zenodo / IACR Cryptology ePrint / Elsevier SSRN*, DOI `10.5281/zenodo.23436152`) |
| **European Commission OpenAIRE Research Graph** | Indexed via Zenodo / ORCID `0009-0006-7498-2133` | https://explore.openaire.eu/search/find?fv0=0009-0006-7498-2133&f0=relpersonid | European Open Science Cloud (EOSC) publication + software graph |
| **Bitcoin Blockchain OpenTimestamps** | `.ots` Proofs (`whitepaper/*.ots`) | [`whitepaper/AUTHORSHIP_MANIFEST.txt.ots`](whitepaper/AUTHORSHIP_MANIFEST.txt.ots) | Decentralized cryptographic timestamp proof of EN/UA Whitepapers & Manifest |

---

## 3. Live Applications, Code Repositories & Package Distribution

| Resource | URL | Description |
|---|---|---|
| **Interactive Client-Side Web Studio (EN)** | https://yaroslavbaienko.github.io/marma-crypto-protocol/ | Zero-backend HTML5 Canvas generator, PDF/SVG Canary Sealer (`pdf-lib`), and Tamper Detector (`pdf.js`) |
| **Interactive Client-Side Web Page (UA)** | https://yaroslavbaienko.github.io/marma-crypto-protocol/ua.html | Ukrainian overview and specification portal |
| **Primary GitHub Repository** | https://github.com/YaroslavBaienko/marma-crypto-protocol | Source code, bilingual Typst/PDF whitepapers, 12-suite verification harness |
| **Debian / Ubuntu APT Repository (`legaltech`)** | https://github.com/YaroslavBaienko/legaltech | Hosts `marma-crypto-watermark` (`1.3.0-1`) and `qes-tools` (`1.0.26`) |
| **One-Line APT Installer** | `curl -fsSL https://yaroslavbaienko.github.io/legaltech/install.sh \| sudo bash` | Configures GPG key and `/etc/apt/sources.list.d/legaltech.list` |

---

## 4. Public Announcements, Community & Media Channels

| Platform | Date | Status / Details |
|---|---|---|
| **Hacker News (`news.ycombinator.com`)** | 2026-10-18 | Published (`Show HN: Marma-Crypto`) |
| **LinkedIn** | 2026-10-18 | Published (Announcement + 11-slide vector PDF carousel `Marma_Crypto_LinkedIn_Carousel_EN/UA.pdf`) |
| **Reddit (`r/cryptography` / tech communities)** | 2026-10-18 | Published technical deep-dive post |
| **X (Twitter) & Facebook** | 2026-10-17 / 18 | Published bilingual visual cards & hero posters (`facebook_hero_poster_en/ua.png`) |
| **DOU.ua (Українська ІТ-спільнота)** | 2026-10-19 | Submitted to Forum («Оцініть проєкт» / DOU Tech, awaiting moderator approval) |
| **Dev.to (Global Developer Community)** | 2026-10-19 | Published technical deep-dive: https://dev.to/yaroslavbaienko/how-we-bound-512-bit-cryptographic-signatures-to-non-linear-sri-yantra-vector-geometry-inside-raw-2k72 |
| **Medium** | 2026-10-19 | Published technical deep-dive (imported from Dev.to with canonical link, topics: `Cryptography`, `Cybersecurity`, `Mathematics`, `Open Source`, `Legaltech`) |

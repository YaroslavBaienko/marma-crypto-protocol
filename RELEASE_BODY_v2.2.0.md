# marma-crypto-watermark v2.2.0

Software release of the Marma-Crypto signer/verifier (protocol `v2.1.0` unchanged).

## Highlights
- **Seal placement policy** — `--seal-pages last|first|first-last|all` (env `MARMA_SEAL_PAGES`),
  default **`last`** (signature page). Applies to PDF, universal/API PDF and DOCX (`all` via a
  repeating header image); SVG carries one seal with `data-seal-pages="last"`.
- **Visible-seal verification** — verification fails closed when the visible seal is missing on a
  declared page; legacy documents without the field keep verifying.
- **Nautilus UX** — new `⚙️ Розміщення печатки (last, first-last, all, ask)` settings action,
  per-signing `ask` dialog, and a fix for the URI-only selection regression that opened a
  redundant file chooser.
- **Seal-only rendering** — no visible captions/signatures under the seal in PDF/DOCX/universal
  output; cryptographic metadata remains embedded.
- **Keyless PDF verification** — ordinary PDF verification uses the embedded DSTU EC signature,
  no owner key vault required; universal-SVG verification falls back to the active session key.
- **Packaging** — Debian revision `2.2.0-5`, menu refresh, `--seal-pages` completion.

## Verification
- Production tests: **73/73 PASS** (PyMuPDF >= 1.28.2).
- Controlled seal run: **PASS** (seal-path coverage 85%, deterministic matrix).
- Nautilus scenario matrix: **16 scenarios**, 11 real signing/verify paths verified, **0 redundant
  file-chooser calls**.
- Package build + isolated package test: **PASS** (self-test 45/45, Nautilus menu deploy).
- Physical print-scan experiment (earlier build): 5/5 fail-closed / 5/5 digital valid.

## Install
```bash
sudo dpkg -i marma-crypto-watermark_2.2.0-5_all.deb
marma-config
marma-watermark --version   # 2.2.0
```
The GitHub release attaches `marma-crypto-watermark_2.2.0-5_all.deb`
(SHA256 `ab3b871d9ba126a9968c1c8778072d7c1c8f2b89bb7e3f3e20160c3c95c6626b`).

## Archived paper
The archived paper/package DOI remains the `v2.1.0` line; this software release adds the seal
placement/UI/packaging changes without changing the protocol or its archived citation.

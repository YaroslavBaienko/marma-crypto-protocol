# Release test record — marma-crypto-watermark 2.2.0-6 (2026-10-25)

**Artifact:** `dist/marma-crypto-watermark_2.2.0-6_all.deb`
**SHA-256:** `5150f1e7168d378757bb0d1bab21044e48737629496b5aea7a297bcddcbd1101`
**Size:** 90 KB (Installed-Size ~?; see `dpkg-deb -I`)

## Package-level tests (host)

- `bash build.sh --test` → **PASS**
  - package extracts;
  - Nautilus menu deploys to an isolated `HOME`;
  - 3 root quick actions seal/verify/report + 3 category folders;
  - `marma-watermark selftest` → PASS (SVG/PDF/DOCX/DSTU/canary/protocol);
  - `marma-watermark doctor --json-out` → status `ok`;
  - 73 pytest tests → 73 passed (after restoring a frozen submission snapshot that a global
    ORCID edit had touched; the snapshot is immutable and now matches its SHA256SUMS manifest).

## Clean Debian 13 container test

Image: `debian:13` (container on Hetzner Docker context; package copied into container).
`apt-get update && apt-get install ./marma-crypto-watermark_2.2.0-6_all.deb` → **success**.

| Check | Result |
|---|---|
| `marma-watermark --version` | `2.2.0` |
| `marma-watermark selftest` | **PASS** (all 6 checks) |
| `marma-watermark doctor` | `status: error` because Debian 13 ships **PyMuPDF 1.25.4**; PAdES needs **>=1.28.2** |
| Nautilus menu | not deployed in the headless root container (expected; no desktop session) |

**Known packaging gap:** the `python3-pymupdf` dependency resolves to 1.25.4 on Debian 13. Basic
sealing/selftest works, but PAdES-LTA whitepaper hashing needs 1.28.2+. `doctor` reports this
explicitly. Fix options are tracked in `docs/PRODUCT_ROADMAP_2026-10-25.md` (versioned dependency,
documented venv/pipx path, or vendored wheel in a future package revision).

## Install / upgrade commands used

```bash
# host build
bash build.sh --test
sha256sum dist/marma-crypto-watermark_2.2.0-6_all.deb

# clean container (Docker context = hetzner)
docker create --name marma-test debian:13 sleep infinity
docker cp dist/marma-crypto-watermark_2.2.0-6_all.deb marma-test:/tmp/marma.deb
docker start marma-test
docker exec marma-test bash -lc 'apt-get update && apt-get install -y /tmp/marma.deb && marma-watermark doctor || true && marma-watermark selftest'
docker rm -f marma-test
```

## Install from release

```bash
curl -LO https://github.com/YaroslavBaienko/marma-crypto-protocol/releases/download/v2.2.0/marma-crypto-watermark_2.2.0-6_all.deb
sudo apt install ./marma-crypto-watermark_2.2.0-6_all.deb
marma-watermark doctor
marma-watermark protocol document.pdf --json-out report.json -o report.pdf
```

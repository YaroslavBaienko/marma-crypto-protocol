# marma-crypto-watermark v2.2.0 — release candidate notes

**RC revision: `2.2.0-2`** (seal-only visual contract).

**Status: RELEASE CANDIDATE — built and package-tested, NOT installed system-wide and NOT tagged.**
The installed system package is still `2.1.0-1`; the new `.deb` is in `dist/`.

## What changed
- **Seal profile P2 `v2-round42`** (`src/marma_seal_profiles.py`): 42 mm round branded technical
  seal; the canonical nine-triangle carrier geometry is unchanged (no coordinate rescale), so the
  payload/DSTU/public-seal path is untouched. The profile id, size and brand are persisted in the
  SVG metadata (`data-profile`, `data-profile-mm`, `data-profile-version`, `data-profile-brand`).
- **CLI `--profile {v1-geometric,v2-round42}`**: SVG signing with P2, verification fails closed on a
  wrong/unknown profile or tampered geometry. `verify` without `--profile` accepts the profile stored
  in the SVG; an explicit `--profile` acts as a requirement.
- **Nautilus menu**: new action `🪙 Згенерувати круглу технічну печатку 42 мм (v2-round42)`
  (`nautilus-scripts/1d_sign_seal_v2.sh`), installed through `marma-config`; verification action
  works for P1 and P2 because the CLI now auto-detects the stored profile.
- **Packaging**: version `2.2.0-1`; `marma_seal_profiles.py` is included in the package; bash
  completion knows `--profile`; package test refreshes the isolated Nautilus menu.
- **Seal-only visual contract:** removed the human-visible caption under the seal in every signing path
  (PDF stamping, universal/API PDF stamping, DOCX stamping). SVG seals already had no text. The
  cryptographic packet remains embedded (PDF keywords, hidden DOCX paragraph, SVG metadata), so
  verification is unchanged; legacy stamped files with the old caption still verify (the verifier
  normalises that line out). New tests: `tests/test_seal_visual_contract.py`.
- P1 `v1-geometric` behavior is unchanged.

## Verification evidence
| Check | Result |
|---|---|
| Controlled seal run (`paper_v3/tests/run_controlled.py`) | **PASS**, 43 tests, seal-path coverage 85.0% |
| Package build + isolated test (`bash build.sh --test`) | **PASS** (includes Nautilus menu deploy + selftest) |
| Packaged CLI P2 sign→verify (extracted .deb) | **PASS** (`verified=true`, `profile=v2-round42`, 42.0 mm) |
| Packaged PDF/DOCX seal-only check (extracted .deb) | **PASS** (verified, no visible caption, hidden packet retained) |
| Full production pytest suite (`tests/`) | **45 passed** with `pymupdf>=1.28.2` (40 + 5 seal-only visual-contract tests). The earlier 1 failure was an environment artifact: `PYTHONPATH=/usr/lib/python3/dist-packages` shadowed PyMuPDF 1.28.2 with 1.25.4, whose text extraction does not reproduce the whitepapers' sealed content hash. With the correct environment the PAdES-LTA/whitepaper audit passes; see `tests/README.md` and `requirements-dev.txt`. |
| Nautilus P2 script wiring (headless, fake CLI) | **PASS** (args: `--sign-svg`, `--profile v2-round42`, `--gui`) |
| Manual GUI click-through in Nautilus | **NOT DONE** (owner action) |
| System deployment / installation | **NOT DONE** (requires sudo: `sudo dpkg -i dist/marma-crypto-watermark_2.2.0-1_all.deb`) |
| Git tag / GitHub release | **NOT DONE** (latest tag is `v2.1.0`) |

Artifact: `dist/marma-crypto-watermark_2.2.0-2_all.deb`
SHA256: `9e103b79b142c32c9889ad8ff4c5c940790d9f400f7e9259642f711437328b14`
Visual evidence: `docs/visual_contract/` (P2 42 mm seal and a stamped page; no caption).

## Install / rollout (owner)
```
sudo dpkg -i dist/marma-crypto-watermark_2.2.0-1_all.deb
marma-config            # refresh the Nautilus menu for the current user
marma-watermark --version
```
Then do a manual Nautilus click-through: right-click a folder → Scripts → 🔱 Шрі Янтра · Marma-Crypto
→ `🪙 Згенерувати круглу технічну печатку 42 мм (v2-round42)`, and verify the result with the
`🔍 Перевірити підпис та геометрію Шрі Янтри` action.

## Known issues before tagging a release
- PyMuPDF >= 1.28.2 is required by the verifier for the sealed whitepapers; Debian's
  `python3-pymupdf` may be older. Document/pin this dependency or re-seal the whitepapers with a
  version-stable canonicalisation before distributing the package widely.
- Manual GUI verification in Nautilus is still required.
- Legal review of the technical seal vs company/notary seal is pending (see
  `paper_v3/drafts/tifs/LEGAL_REVIEW_CHECKLIST.md`).

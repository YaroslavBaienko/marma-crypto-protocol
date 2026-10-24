# marma-crypto-watermark v2.2.0 — release candidate notes

**RC revision: `2.2.0-5`** (Nautilus seal-placement dialog, seal placement policy, selection fix, seal-only visual contract).

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
- **Packaging**: version `2.2.0-5`; `marma_seal_profiles.py` is included in the package; bash
  completion knows `--profile`; package test refreshes the isolated Nautilus menu.
- **Seal-only visual contract:** removed the human-visible caption under the seal in every signing path
  (PDF stamping, universal/API PDF stamping, DOCX stamping). SVG seals already had no text. The
  cryptographic packet remains embedded (PDF keywords, hidden DOCX paragraph, SVG metadata), so
  verification is unchanged; legacy stamped files with the old caption still verify (the verifier
  normalises that line out). New tests: `tests/test_seal_visual_contract.py`.
- **Nautilus selection fix (2026-10-24):** all document actions now resolve the selection from
  `NAUTILUS_SCRIPT_SELECTED_FILE_PATHS`, `NAUTILUS_SCRIPT_SELECTED_URIS` (file:// URIs are decoded,
  including spaces/percent-encoding), paths that themselves contain URIs, and the split-view
  fallback. Previously, a view/version that exposed only URIs made the list empty and the action
  opened a fallback zenity file chooser even though a file was selected.
- **Visible error dialogs:** signing/verify/protocol actions now show a warning dialog with the CLI
  error instead of failing silently (`marma_run_or_warn`).
- **Headless mode:** `MARMA_HEADLESS=1` skips GUI dialogs/`--gui` so the same scripts can be
  exercised end-to-end in CI and manual scripted runs.
- **Manual/scripted scenario matrix:** `tests/manual_scenarios.py` runs 15 menu scenarios with a
  simulated Nautilus selection; 10 signing/verify/batch/protocol scenarios executed with the real
  CLI (10 outputs verified, 0 zenity chooser calls), 4 interactive-only actions listed with the
  reason they cannot be automated. Evidence: `docs/manual_test/2026-10-24/` (report, JSON, contact
  sheet, per-scenario page screenshots).
- **Seal placement policy (2026-10-24):** `--seal-pages {last|first|first-last|all}` (env
  `MARMA_SEAL_PAGES`). Default is now **`last`** (the signature page). PDF and universal/API PDF
  honor the policy; DOCX supports `last`/`first`/`first-last` body placement and `all` via a
  repeating header image; SVG stores `data-seal-pages="last"` (one seal). The metadata carries
  `seal_pages`, and the verifier now **fails if the visible seal is missing on a declared page**
  ("Visible seal missing on page(s) …"), while legacy documents without the field keep verifying.
- **Keyless PDF verification:** `marma-watermark verify` no longer requires the owner's private
  key vault for ordinary PDFs (the embedded DSTU EC signature is checked); universal-SVG
  verification falls back to the active session key.
- **Nautilus seal-placement UI (2026-10-24):** new menu action
  `⚙️ Розміщення печатки (last, first-last, all, ask)` under Keys/Session/Help saves the policy
  to `~/.config/marma-crypto/config.json` (`seal_pages`). Signing actions read the saved policy;
  `ask` opens a per-signing radio dialog (default last), and `MARMA_SEAL_PAGES` overrides the file.
  Dialog screenshot: `docs/visual_contract/seal_placement_dialog.png`.
- P1 `v1-geometric` behavior is unchanged.

## Verification evidence
| Check | Result |
|---|---|
| Controlled seal run (`paper_v3/tests/run_controlled.py`) | **PASS**, 43 tests, seal-path coverage 85.0% |
| Package build + isolated test (`bash build.sh --test`) | **PASS** (includes Nautilus menu deploy + selftest) |
| Packaged CLI P2 sign→verify (extracted .deb) | **PASS** (`verified=true`, `profile=v2-round42`, 42.0 mm) |
| Packaged PDF/DOCX seal-only check (extracted .deb) | **PASS** (verified, no visible caption, hidden packet retained) |
| Packaged seal-pages check (extracted .deb) | **PASS** (`last` and `all` verified, `seal_pages`/`visible_seal_ok` reported) |
| Full production pytest suite (`tests/`) | **73 passed** with `pymupdf>=1.28.2` (40 core + 5 seal-only visual + 6 Nautilus selection + 14 seal-placement + 8 Nautilus placement-dialog/config). The earlier 1 failure was an environment artifact: `PYTHONPATH=/usr/lib/python3/dist-packages` shadowed PyMuPDF 1.28.2 with 1.25.4, whose text extraction does not reproduce the whitepapers' sealed content hash. With the correct environment the PAdES-LTA/whitepaper audit passes; see `tests/README.md` and `requirements-dev.txt`. |
| Nautilus P2 script wiring (headless, fake CLI) | **PASS** (args: `--sign-svg`, `--profile v2-round42`, `--gui`) |
| Manual GUI click-through in Nautilus | **NOT DONE** (owner action) |
| System deployment / installation | **NOT DONE** (requires sudo: `sudo dpkg -i dist/marma-crypto-watermark_2.2.0-5_all.deb`) |
| Git tag / GitHub release | **NOT DONE** (latest tag is `v2.1.0`) |

Artifact: `dist/marma-crypto-watermark_2.2.0-5_all.deb`
SHA256: `ab3b871d9ba126a9968c1c8778072d7c1c8f2b89bb7e3f3e20160c3c95c6626b`
Visual evidence: `docs/visual_contract/` (P2 42 mm seal and a stamped page; no caption).

## Install / rollout (owner)
```
sudo dpkg -i dist/marma-crypto-watermark_2.2.0-5_all.deb
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

# Real GUI evidence — Nautilus action (2026-10-24, Wayland)

## What was exercised
- Nautilus 48.3 on GNOME Wayland; a real context-menu script action was invoked via keyboard
  automation on the focused Nautilus window (no headless harness for this step).
- The action completed with the normal Nautilus success notification
  “✅ Накладено печатку … / signed 1 document”.
- The selected source document belonged to an existing Nautilus window
  (`/home/attor/Documents/00_sample.pdf`); the new test window's selection was not the one picked
  up because two Nautilus windows were open. This is an important UX observation: the script gets
  the selection of the window from which the menu was invoked, not necessarily the front-most one.

## Result (files are not copied into the repo)
- Output: `/home/attor/Documents/00_sample_marma_signed.pdf`
- Size: 245,836 bytes · pages: 7
- SHA-256: `0c09f8fd025ca6443bdee3b1d404f6b376b6489f37c1f25f9b1c63cab534586f`
- Verification via CLI: `verified=true`, `reason=OK`, `seal_pages=last`,
  `visible_seal_ok=true`, emblem `sri-yantra`
- Visible caption check: **no** `MARMA-CRYPTO-SEAL` text in the rendered text layer
- Seal placement: visible only on the last page (default policy), as configured.

## Other real-GUI artefact
- Seal-placement settings dialog was opened for real and screenshotted:
  `docs/visual_contract/seal_placement_dialog.png` (all five options visible: last, all,
  first+last, first, ask).

## Not exercised manually
- Each menu item one-by-one (keygen, strict-key, help, lock, optical trace).
- A second signing on the new test window to confirm the multi-window selection observation;
  the headless 16-scenario matrix covers all script wirings.

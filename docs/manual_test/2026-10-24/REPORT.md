# Nautilus scenarios — headless end-to-end run

Generated: 2026-10-24 20:41 · contact sheet: `contact_sheet.png`

Environment: Nautilus selection simulated with **URIs only** (the regression case) or paths;
`MARMA_HEADLESS=1`; real `marma-watermark` from `~/.local/bin`; fake `zenity` logs any chooser call.

| Scenario | Selection | Exit | Verified | Visible caption | Zenity chooser | Screenshot |
|---|---|---|---|---|---|---|
| 1_stamp_both_uris | uris | 0 | True | False | 0 | runs/1_stamp_both_uris/screenshot.png |
| 1b_watermark_paths | paths | 0 | True | False | 0 | runs/1b_watermark_paths/screenshot.png |
| 1c_seal_uris | uris | 0 | True | False | 0 | runs/1c_seal_uris/screenshot.png |
| 1c_seal_all_pages | uris | 0 | True | False | 0 | runs/1c_seal_all_pages/screenshot.png |
| 1_stamp_both_docx | uris | 0 | True | False | 0 | runs/1_stamp_both_docx/screenshot.png |
| 1d_seal_v2 | none | 0 | True | False | 0 | runs/1d_seal_v2/screenshot.png |
| 2_sign_svg | none | 0 | True | False | 0 | runs/2_sign_svg/screenshot.png |
| 8_tryzub | uris | 0 | True | False | 0 | runs/8_tryzub/screenshot.png |
| 9_cad_svg | uris | 0 | True | False | 0 | runs/9_cad_svg/screenshot.png |
| 10_batch_dealroom | uris | 0 | True | False | 0 | runs/10_batch_dealroom/screenshot.png |
| 3_verify | uris | 0 | True | False | 0 | — |
| 4_protocol | uris | 0 | None | False | 0 | — |
| 5_strict_key | n/a | None | None | None | 0 | — |
| 6_keygen | n/a | None | None | None | 0 | — |
| 7_lock_session | n/a | None | None | None | 0 | — |
| 0_help | n/a | None | None | None | 0 | — |

## Findings
- URI-only selections are now resolved; no script opened a zenity file chooser (0 calls in every non-skipped scenario).
- All signed outputs carry no visible `MARMA-CRYPTO-SEAL` caption; hidden metadata remains embedded.
- Interactive actions (keygen, strict-key, help, lock) cannot be exercised headlessly; their scripts pass syntax and wiring tests.

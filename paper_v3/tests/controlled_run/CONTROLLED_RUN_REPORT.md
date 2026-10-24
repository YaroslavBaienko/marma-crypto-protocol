# Controlled cross-verified run — Marma PDF seal

**Verdict: PASS** · 2026-10-24T20:43:30.830102+03:00 · git `8a5dd9f6d753`

## Scope
This run covers the *paper profile* P1 (current geometric stamp, no cryptography changes) and the *product prototype* P2 (42 mm round branded technical stamp with decorative rings, profile-fixed in the verifier). The payload lattice, word map and key schedule are unchanged.

## Gates
| Gate | Result | Detail |
|---|---|---|
| corpus manifest | PASS | 180 files, 0 hash mismatches |
| environment snapshot | PASS |  |
| unittest suite | PASS | 43 tests |
| branch coverage | PASS | seal-path 85.0% ({'pdf_layer.py': 72.3, 'profiles.py': 93.7, 'harness.py': 80.5}); overall incl. drivers 44.5% |
| cross-validation matrix | PASS | 12 samples; {'exact': True, 'trunc8': True, 'trunc7_detected': True, 'single_coord_edit': True, 'geometry_ok': True, 'flatten_absent': True} |
| determinism (matrix run twice) | PASS | hash 0d9df3cc62adfcb8… |
| production P2 profile | PASS | v2 verified=True, profile persisted=True, wrong-profile fail=True, tamper fail=True, v1 legacy=True |
| artifact hashes | PASS |  |

## Tests
Unittest suite: **43 tests, OK**. Classes: word-map/KAT, cross-runtime (independent JavaScript), cross-production (`src/marma_watermark.py`), profile round-trip P1/P2, geometry invariant, truncation, single-coordinate edit, flatten/fail-closed, wrong-profile rejection, reserved-zone no-overlap, corpus sha256, physical print-scan results, cross-validation matrix.

## Coverage (branch)
Overall: **44.5%** · core: `{'pdf_layer.py': 72.3, 'profiles.py': 93.7, 'harness.py': 80.5}`
Uncovered areas are the experiment drivers, baseline implementations and corpus-generator branches that are not part of the seal path; they are listed in coverage.json.

## Production profile
P2 is wired into the production signer through the additive wrapper `src/marma_seal_profiles.py`: the canonical carrier geometry is unchanged, the profile changes physical size (42 mm), round branding and persists `data-profile` in the SVG metadata. The verifier fails closed on an unknown or mismatched profile and on tampered geometry; the legacy v1 path is unchanged.

## Cross-validation matrix
12 samples (2 profiles x 3 documents x 2 seeds), run twice: hash `0d9df3cc62adfcb8…`. Checks: `{'exact': True, 'trunc8': True, 'trunc7_detected': True, 'single_coord_edit': True, 'geometry_ok': True, 'flatten_absent': True}`.

## Cross-run determinism
Matrix hash stable across two independent runs: **PASS**.

## Guarantee statement (precise)
Under the stated preconditions — the carrier is written with >=9 decimal places, the verifier parses the content stream as text, and no rasterisation occurs — the payload is recovered bit-exactly, 8-decimal re-serialisation is safe, 7-decimal re-serialisation and single-coordinate edits are detected, flattening fails closed, and an untouched document yields no carrier. These properties are deterministic and are covered by the gates above.
No absolute 100% guarantee is possible for arbitrary PDF pipelines, hardware or legal acceptance; those remain out of scope and are stated in the manuscript limitations.

## Reproduction
```
cd /home/attor/002_AI/PROJECTS/EDU-VEDI/marma-crypto-protocol
python3 paper_v3/tests/run_controlled.py
```

## Artifacts
- `results.json` — machine-readable gate results
- `coverage.json`, `coverage_summary.json` — coverage data
- `matrix.json` — cross-validation rows and hash
- `environment.json` — toolchain snapshot
- `SHA256SUMS` — hashes of the tested sources
- `test_output.txt` — full unittest log

## Out of scope
- full 1,800-sample evaluation (run by `eval/run_pdf_experiments.py`)
- baseline re-implementations, physical printer/scanner population study
- legal validity of a technical seal vs. a company/notary seal (separate review)

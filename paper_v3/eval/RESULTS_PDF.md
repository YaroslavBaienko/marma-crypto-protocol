# PDF-level results (v0)

Samples: 2880


## Main (60 native docs, keyed QIM, Sri Yantra carrier)

| metric | mean | 95% CI | count |
|---|---|---|---|
| exact | 1.0000 | ±0.0000 | 1800/1800 |
| exact_trunc8 | 1.0000 | ±0.0000 | 1800/1800 |
| exact_trunc7 | 0.0000 | ±0.0000 | 0/1800 |
| exact_edit | 0.0000 | ±0.0000 | 0/1800 |
| flatten_carrier_present | 0.0000 | ±0.0000 | 0/1800 |

## Variants (flattened / print-scan PDFs, carrier stamped on top)

| metric | mean | 95% CI | count |
|---|---|---|---|
| exact | 1.0000 | ±0.0000 | 360/360 |
| exact_trunc8 | 1.0000 | ±0.0000 | 360/360 |
| exact_trunc7 | 0.0000 | ±0.0000 | 0/360 |
| exact_edit | 0.0000 | ±0.0000 | 0/360 |
| flatten_carrier_present | 0.0000 | ±0.0000 | 0/360 |

## Ablation: carrier × keying

| carrier | keyed | exact | exact_trunc8 | exact_edit | centre edit detected by geometry |
|---|---|---|---|---|---|
| sri-yantra | True | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| sri-yantra | False | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| generic-polyline | True | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| generic-polyline | False | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| grid | True | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| grid | False | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

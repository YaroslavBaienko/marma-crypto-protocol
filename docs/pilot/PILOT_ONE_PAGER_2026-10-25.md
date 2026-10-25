# Marma-Crypto — paid pilot one-pager (legal & M&A evidence)

**Status:** internal sales asset, 2026-10-25. Do not publish prices/case studies before the first
pilot is signed. External one-pager should be a PDF generated from this text.

## The problem

A valid PDF signature proves *bytes*, not the page a lawyer or deal-team member is looking at.
When a signed document is re-rendered, flattened, screenshotted or leaked from a data room, the
signature can remain valid while the visible document changes or the copy loses its origin.

## What Marma-Crypto adds

- **Visible seal** bound to an exact cryptographic digest; the seal is checked on the rendered page.
- **Client-side verification** — the document never has to be uploaded.
- **Verification report** (PDF + JSON) for an evidence memo or deal file.
- **Complement to PAdES/eIDAS/DSTU 4145**: qualified signature stays the legal identity layer;
  Marma-Crypto is the visible tamper-evidence layer.
- **Recipient canary** for vector-preserved copies; we explicitly do **not** claim tracing of
  screenshots, photos or printouts — those need a robust companion layer.

## Ideal pilot customer

- Boutique law firm / M&A counsel / arbitration team (10–50 lawyers), or
- Forensic document examiner / notary office handling signed evidence, or
- A VDR/DMS product team evaluating a tamper-evidence add-on (partner track).

Not a fit yet: a buyer looking for a full VDR, an e-signature replacement, or universal leak
attribution from screenshots.

## Pilot package (2 weeks)

| Item | Scope |
|---|---|
| Discovery | 45-min workflow call; one document set; threat model |
| Setup | Linux CLI + verification report; optional Nautilus/desktop demo |
| Evidence set | Up to 10 signed PDF/DOCX documents (real or anonymised) |
| Deliverables | Sealed copies + verification report + short fit/limitations memo |
| Support | Email/Telegram support during the pilot; 30-day follow-up |
| Decision | Go/no-go call; no automatic enterprise commitment |

**Commercial:** fixed fee agreed after scoping; recommended range **€2,500–€5,000** for the pilot
(proposed, not yet validated). Enterprise deployment/support quoted separately.

## Success criteria (agree before start)

1. A lawyer can verify a sealed document in ≤3 minutes without CLI knowledge.
2. The verification report contains the document hash, seal status, PAdES/QES status and limitations.
3. At least one real workflow (deal room, evidence bundle or notarisation) is tested end-to-end.
4. Buyer states a clear next step: enterprise quote, integration, or no-fit.

## What we do not promise

- Court admissibility without a legal opinion.
- Traceability of screenshots/photos/printouts with the fragile vector seal.
- Replacement of QES/PAdES, DocuSign/Adobe or a VDR.
- Any guarantee that a leaked copy will be attributed.

## Next step

**15-minute evidence audit** → `mailto:zerhug@gmail.com?subject=Marma-Crypto%20pilot%20request`.
Bring one anonymised signed document and describe the last time a copy or rendered page was in doubt.

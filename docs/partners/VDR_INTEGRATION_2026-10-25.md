# VDR/DMS integration brief — Marma-Crypto (2026-10-25)

**Goal:** let a VDR/DMS or e-signature platform add a visible tamper-evidence layer without building
a VDR or replacing its signature workflow. This is a partner brief, not a commitment to a specific
vendor.

## Why a VDR would care

- Differentiator vs commodity data rooms: "visible seal + verification report" for high-stakes
  documents.
- Supports legal/M&A evidence and leak-investigation workflows.
- Complements existing permissions, audit trails, dynamic watermarking and QES.

## Existing API surface (v2.1.0)

`marma_crypto/api_server.py` already exposes a local HTTP service:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/v1/health` | Service/version check |
| `POST` | `/v1/seal-batch` | Batch-seal N recipient copies (PDF) |
| `POST` | `/v1/verify` | Verify a sealed document |
| `POST` | `/v1/trace-leak` | Trace a vector PDF/DOCX/SVG or raster screen photo (optical ring) |

The current server binds localhost by default and has **no authentication, tenant context, rate
limiting or persistent audit log**. Those are integration prerequisites, not features to hand-wave.

## Proposed partner architecture

```
VDR/DMS ──(signed webhook / API)──> Marma integration service
                                      │
                                      ├─ seal job (document + recipient id)
                                      ├─ verify job (document + optional report)
                                      ├─ evidence store (hash, job id, report)
                                      └─ callback/webhook → VDR audit log
```

- **Auth:** mTLS or OAuth2 client credentials; no anonymous access.
- **Tenant isolation:** `tenant_id`/`project_id` on every job; no cross-tenant report access.
- **Data minimization:** default local/on-prem processing; no document retention unless agreed.
- **Async jobs:** seal batch can take seconds/minutes; return `job_id`, poll or webhook.
- **Evidence:** JSON + PDF report with document hash, seal status, PAdES/QES status, tool version,
  timestamp and limitations.
- **Idempotency:** `Idempotency-Key` per document/recipient; safe retries.
- **Audit:** append-only log of who requested what, when, with which tool version.
- **Failure:** fail closed; never mark a document verified on transport/parse error.

## Minimum API additions for a partner pilot

1. `POST /v1/jobs/seal` → `{job_id, status}`; `GET /v1/jobs/{id}`.
2. `POST /v1/jobs/verify` + `GET /v1/jobs/{id}/report` (PDF/JSON).
3. `POST /v1/webhooks` (signed HMAC) or polling contract.
4. Auth + tenant header; request size limits; rate limits.
5. OpenAPI 3.1 document and a sandbox tenant.

## Integration sequence

1. **Discovery:** which document type/flow; who verifies; what report format; data residency.
2. **Sandbox:** 10 documents, one recipient canary, one report; no production credentials.
3. **Pilot:** one deal/evidence set; measure time-to-verify and support load.
4. **Production:** SSO/RBAC, audit retention, monitoring, DPA/security review.

## Honest limitations to document in the partner UI

- The fragile vector seal does **not** survive screenshots, photos or print-to-image; show a clear
  status, not a false "leak traced".
- It is not a QES/PAdES replacement; display the existing signature status alongside.
- A robust invisible layer (own or partner) is required for photo/screenshot leak attribution.

## Next step

Send this brief + one-page pilot offer to 2–3 VDR/DMS product leads; ask for a 30-minute integration
call and a sandbox deal. Do not build a generic VDR connector before one partner commits.

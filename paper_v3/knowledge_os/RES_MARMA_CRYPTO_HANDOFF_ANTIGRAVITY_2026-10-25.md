# RES-MARMA-CRYPTO — handoff to Antigravity (writer stays `antigravity`)

**Decision (owner, 2026-10-25):** keep the tenant writer as **`antigravity`**. Do not change
`marma_spec.py`; dsh must not write HOT rows under an `antigravity` stamp. The five HOT-only rows,
model reconciliation and the new-document ingest are therefore owner/Antigravity actions.

## Audit baseline (read-only, 2026-10-25)

- Spec validation: `OK RES-MARMA-CRYPTO prefix=MARMA tier=PUBLIC labels=4 strategy=static extractor=pymupdf core>=0.3`
- local manifest: 49
- HOT `project_documents`: 54
- Qdrant points: 692 (all PUBLIC)
- writers: `antigravity: 687`, `claude_code: 5`
- embedding models: `deepinfra-bge-m3: 684`, `BAAI/bge-m3: 3`, `bge-m3: 5`
- findings: 5 HOT-only rows; writer mismatch (`claude_code`); mixed models
- ingest dry-run: candidates=0 (inbox empty)
- no writes: confirmed

## Five HOT-only rows — mapping to local corpus

These are **old aliases** of documents that already exist locally under other doc codes. Re-register
or retire them; do not duplicate the files.

| HOT doc_code | Existing local manifest key / doc_code | Local file |
|---|---|---|
| `MARMA-PUBLICATIONS-REGISTRY` | `PUBLICATIONS.md` → `MARMA-L3-0019` | `PUBLICATIONS.md` |
| `MARMA-SVG-CAdES-v1.2.1` | `docs__assets__sri_yantra_whitepaper_diagram.svg` → `MARMA-L1-0029` | `docs/assets/sri_yantra_whitepaper_diagram.svg` |
| `MARMA-TESTS-v1.2.1` | `test_marma_cross_verification.py` → `MARMA-L4-0044` | `tests/test_marma_cross_verification.py` |
| `MARMA-WP-UA-v1.2.1` | `docs__whitepaper__Marma_Crypto_Whitepaper_UA.pdf` → `MARMA-L3-0032` | `docs/whitepaper/Marma_Crypto_Whitepaper_UA.pdf` |
| `MARMA-WP-EN-v1.2.1` | **no local manifest entry yet** | `whitepaper/Marma_Crypto_Whitepaper_EN.pdf` (also `docs/whitepaper/...`) |

Recommended Antigravity action: update the HOT rows to the existing local doc codes where a mapping
exists, and add a proper local manifest entry for the EN whitepaper before re-registering the EN row.
Do not delete rows without an owner-approved archival action.

## Re-embedding one model

Target model per spec: **`deepinfra-bge-m3`** (1024-d, `RES_MARMA_CRYPTO_bge`).

After the row re-registration, run the tenant pipeline as Antigravity:

```bash
cd ~/002_AI/claude-system-backup/pipelines/knowledge-os
python -m knowledge_os reconcile --spec tenants/RES-MARMA-CRYPTO/marma_spec.py
python -m knowledge_os embed --spec tenants/RES-MARMA-CRYPTO/marma_spec.py
python -m knowledge_os audit --spec tenants/RES-MARMA-CRYPTO/marma_spec.py --hot ssh:root@100.123.248.18
```

The embed stage must rewrite all 692 points with `deepinfra-bge-m3`; a partial re-embed would leave
the model mix finding in place. Check `dims` and model counts in the audit output.

## New TIFS/site documents

Do not ingest the whole `paper_v3/` tree: it contains drafts, emails, ORCID/contact data and internal
submission records. If the owner wants the new material in the tenant, prepare **public, sanitised**
copies only, e.g.:

- `paper_v3/drafts/tifs/ieee/main.pdf` (submitted manuscript; public preprint relation already disclosed)
- `docs/WEBSITE_AUDIT_2026-10-25.md` / `docs/index.html` (public site material)
- `paper_v3/IEEE_SUBMISSION_PLAYBOOK_2026-10-25.md` (public process, without private contact data)

Place them in `inbox/`, then as Antigravity:

```bash
python -m knowledge_os ingest --spec tenants/RES-MARMA-CRYPTO/marma_spec.py \
  --hooks tenants/RES-MARMA-CRYPTO/marma_spec.py --dry-run --classifier static
# inspect preview, then apply without --dry-run
python -m knowledge_os sync-hot --spec tenants/RES-MARMA-CRYPTO/marma_spec.py
python -m knowledge_os embed --spec tenants/RES-MARMA-CRYPTO/marma_spec.py
python -m knowledge_os reconcile --spec tenants/RES-MARMA-CRYPTO/marma_spec.py
python -m knowledge_os audit --spec tenants/RES-MARMA-CRYPTO/marma_spec.py --hot ssh:root@100.123.248.18
```

## What dsh did / did not do

- ✅ validated the spec and ran the read-only audit;
- ✅ ran ingest dry-run (0 candidates);
- ✅ wrote this handoff and the audit report;
- ❌ did not change the writer or spec;
- ❌ did not write/delete HOT rows;
- ❌ did not re-embed Qdrant points;
- ❌ did not ingest project files.

The report is in `paper_v3/knowledge_os/RES_MARMA_CRYPTO_AUDIT_2026-10-25.md` and `.json`.

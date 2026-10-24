# RES-MARMA-CRYPTO — knowledge_os tenant audit (2026-10-25)

**Tenant:** `RES-MARMA-CRYPTO` (prefix `MARMA`, tier `PUBLIC`)
**Spec:** `~/002_AI/claude-system-backup/pipelines/knowledge-os/tenants/RES-MARMA-CRYPTO/marma_spec.py`
**Root:** `/home/attor/002_AI/PROJECTS/EDU-VEDI/marma-crypto-protocol`
**Command:** `python -m knowledge_os audit --spec ... --hot ssh:root@100.123.248.18`
**Mode:** read-only audit + ingest dry-run; no HOT writes.

## Writer decision (owner, 2026-10-25)

**Keep `antigravity`** as the tenant writer; `marma_spec.py` is unchanged. dsh therefore does not write HOT rows or Qdrant points under that stamp. Evidence and handoff: `RES_MARMA_CRYPTO_HANDOFF_ANTIGRAVITY_2026-10-25.md`.

## Verdict

**INCONSISTENT** — the tenant is declared and readable, but the HOT audit reports five
HOT-only rows, mixed writer stamps and mixed embedding models. The inbox is empty, so a full
ingest dry-run has **0 candidates** and cannot add the new TIFS v3/website documents yet.

## Measured state

| Metric | Value |
|---|---|
| Local manifest keys | 49 |
| HOT `project_documents` rows | 54 |
| `local_minus_hot` | 0 |
| `hot_minus_local` | **5** |
| Qdrant points | 692 |
| Tiers | `PUBLIC: 692` |
| Writers | `antigravity: 687`, `claude_code: 5` |
| Embedding models | `deepinfra-bge-m3: 684`, `BAAI/bge-m3: 3`, `bge-m3: 5` |
| Dimensions reported | `{}` (none) |

### Findings

1. **HOT rows without a local key:** `MARMA-PUBLICATIONS-REGISTRY`, `MARMA-SVG-CAdES-v1.2.1`,
   `MARMA-TESTS-v1.2.1`, `MARMA-WP-EN-v1.2.1`, `MARMA-WP-UA-v1.2.1`.
2. **Art.23 MAC5 writer mismatch:** HOT contains `antigravity` and `claude_code`; the spec declares
   `writer_agent="antigravity"`.
3. **Mixed embedding models:** `deepinfra-bge-m3`, `BAAI/bge-m3`, `bge-m3` all appear in the
   collection; reconcile/re-embed is needed before claiming one-model consistency.
4. **New project docs are not in the tenant corpus:** TIFS v3 manuscript/package, IEEE playbook,
   website audit, skill and current release notes live outside `whitepaper/`/`inbox`; adding them
   requires the tenant ingest pipeline and the correct writer stamp.

## Ingest dry-run

```text
[start] project_code=RES-MARMA-CRYPTO corpus=49 candidates=0 archives=[] nested=0 classifier=static model=None dry_run=True
[done] accepted=0 quarantined=0 skipped=0 registered=0 empty=True
```

No files were accepted, quarantined or registered; nothing was written to Supabase/Qdrant.

## What was NOT done (and why)

- **No HOT writes:** the tenant spec stamps `writer_agent="antigravity"`; dsh must not write under
  another agent's stamp (Art.23 MAC5). A new writer stamp needs an owner decision/spec change.
- **No full ingest of `paper_v3/`:** the tenant's intake is `inbox/` + `whitepaper/`; copying the
  whole project tree would include drafts, emails, ORCID/contact metadata and internal submission
  records. Only public, classified documents should enter a PUBLIC tenant.
- **No deletion/reconciliation of the five HOT-only rows:** audit is emit-only; fixes belong to the
  tenant pipeline/owner decision.

## Recommended next actions

1. Decide the writer for RES-MARMA-CRYPTO (`antigravity` vs `dsh` vs `pipeline`) and update the spec
   if the ownership changes; do not forge a foreign stamp.
2. Reconcile the five HOT-only rows: re-add local manifests or remove/archive with owner approval.
3. Re-embed the collection with one model (prefer the spec's `deepinfra-bge-m3`) and rerun audit.
4. If the new TIFS v3/site docs should be indexed, place only public, sanitised copies in the tenant
   `inbox/`, run `ingest --dry-run`, review the preview, then apply with the correct writer, followed
   by `sync-hot`, `embed`, `reconcile`, and another audit.

## Cross-reference

- TIFS submission: `paper_v3/drafts/tifs/SUBMISSION_CONFIRMATION_2026-10-25.md`
- Manuscript ID: `T-IFS-29736-2026`
- Tenant spec validation: `OK RES-MARMA-CRYPTO prefix=MARMA tier=PUBLIC labels=4 strategy=static extractor=pymupdf core>=0.3`

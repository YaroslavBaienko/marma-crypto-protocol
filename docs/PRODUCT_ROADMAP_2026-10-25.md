# Marma-Crypto: product, website, .deb and Nautilus roadmap (2026-10-25)

**Goal:** increase the odds of commercial success, not add more technical surface area.
**Context:** niche analysis shows the product is technically differentiated but commercially
mispositioned; see `docs/research/NICHE_ANALYSIS_2026-10-25.md`.

## Progress — 2026-10-25 (implemented in this repo)

- ✅ P0.1 website: legal/M&A positioning, pilot CTA, honest vector-only leak-tracing limit,
  refreshed OG card; live page verified.
- ✅ P0.2 browser/CLI labelling: browser remains v1.3 256-bit and is labelled as a demo;
  production CLI is 266-bit. Payload parity is still a P1 product task.
- ✅ P0.3 packaging: `2.2.0-6` release asset, `doctor`, `--json-out` evidence records,
  Nautilus quick actions, clean Debian 13 install smoke test; PyMuPDF 1.25.4 vs 1.28.2 gap is
  now reported by `doctor` (upstream dependency fix still open).
- ✅ P0.4 Nautilus: root quick actions seal / verify / report plus the three category folders;
  progress/error polish remains.
- ✅ P0.5 verification report: PDF protocol + JSON sidecar (`protocol --json-out`,
  `verify --json-out`).
- ✅ Pilot kit: one-pager, buyer interview script, outreach/LOI; VDR/DMS integration brief.
- ⏳ P0.6 buyer validation and paid pilot: requires owner outreach; assets are ready.
- ⏳ Product Hunt listing update: prepared in `docs/producthunt/PH_UPDATE_2026-10-25.md`;
  actual save needs owner login.
- ⏳ APT repository refresh: site now points to the GitHub release `.deb`; the legaltech APT mirror
  still needs a separate sync.

## 0. Current state (measured)

| Area | State | Main gap |
|---|---|---|
| Website | Product-first landing page, value cards, quickstart, OG card, responsive, EN/UK toggle | Still sells broad “trace” and crypto jargon; no pilot CTA, pricing, proof/case study, buyer-specific path |
| Browser app | Zero-upload PDF/SVG sealer + verifier | Browser carrier is v1.3 **256-bit**; production CLI is v2.1.0 **266-bit** |
| CLI/app | 266-bit, PDF/DOCX/SVG, seal-page policies, verify/trace | Linux-only, CLI/Nautilus friction; no JSON verification report or API |
| `.deb` | `2.2.0-6_all.deb`, Python/GNOME deps; doctor + JSON report + quick Nautilus actions | `python3-pymupdf` dependency may still be older than the PAdES requirement; clean-VM/APT upgrade test not yet automated |
| Nautilus | 3 localized category folders + 3 root quick actions (seal/verify/report), selection resolver tested | Advanced categories still dense; progress/error messaging can be improved; no explicit “what it is not” in the menu |
| GTM | Product Hunt 1 upvote; no paid pilot; no design partner | Wrong category/audience; no proof of willingness to pay |
| Research | TIFS `T-IFS-29736-2026` under review | Credibility only; not distribution |

## P0 — next 14 days (do these before more features)

### P0.1 Reposition website and Product Hunt

- Buyer: **legal/M&A evidence**, not “encryption and cryptography tools”.
- Promise: **visible, tamper-evident seal for signed PDFs/DOCX**, complementing PAdES/eIDAS.
- Remove/qualify broad “trace any leak”: fragile vector carrier covers **vector-preserved copies
  only**; screenshots/photos/printouts need a robust layer.
- Add a primary CTA: **“Book a 15-minute evidence audit”** / “Request a pilot”, not another whitepaper.
- Add: one concrete use case, a verification-report sample, pricing/pilot range, security/data
  handling page, legal disclaimer.
- Product Hunt: update tagline/description/topics/gallery per `docs/producthunt/PH_UPDATE_2026-10-25.md`,
  but do not expect traction from this channel.

**Acceptance:** a lawyer/M&A buyer can answer in 10 seconds: what it does, what it does not do, what
to click, and what the pilot costs.

### P0.2 Browser ↔ CLI parity or explicit demo label

- Preferred: implement 266-bit payload in browser and test it against CLI verify.
- If not feasible in 14 days: keep the browser demo, but label it **“demo v1.3 / 256-bit; production
  CLI v2.1.0 / 266-bit”** everywhere (hero, sealer, quickstart, PH).
- Add a downloadable sample pair: sealed PDF + verification report; let the buyer test without CLI.

**Acceptance:** browser-sealed sample passes CLI verify; or the site states the limitation without
ambiguity and no page claims 266-bit browser sealing.

### P0.3 `.deb` packaging trust

- Update package description from 256-bit to current **266-bit CLI / 256-bit browser demo** scope.
- Audit `python3-pymupdf` version: PAdES whitepaper hashing needs **PyMuPDF ≥1.28.2**; Debian package
  may install an older one. Options: versioned dependency, documented `pipx`/venv, or graceful
  `marma-watermark doctor` check with an actionable message.
- Add `marma-watermark doctor`: Python/PyMuPDF version, PDF writer decimals, fonts, keyring,
  Nautilus presence, optional dependencies; JSON output.
- Add a clean Debian 13 test (container/VM): `apt install`, run self-test, install Nautilus menu,
  upgrade from 2.2.0-1/2/3/4 to 2.2.0-5, uninstall, reinstall; verify no stale menu entries.
- Add `lintian` (or equivalent) and a reproducible-build check; publish SHA-256 and signed APT
  `InRelease`.
- Add a `.desktop` launcher for `marma-dialog` and a man page; do not make Nautilus the only GUI.
- Remove the default demo secret from any real deployment path; require keyring/passphrase.

**Acceptance:** fresh Debian 13 + `apt install marma-crypto-watermark` → GUI/CLI/Nautilus all work;
upgrade/uninstall clean; `marma-watermark doctor` reports the exact PyMuPDF version.

### P0.4 Nautilus integration UX

Current: a folder with 3 category subfolders (16 actions) plus 3 root quick actions.

- ✅ Added root quick actions: seal, verify, verification report.
- Next: add a single `More…` / `Advanced` entry, progress/error dialogs and hide debug actions.
- Show progress (`zenity --progress` or `notify-send`) for batch operations; never block silently.
- On error, show an actionable dialog with the command/log path; fail closed.
- Only enable for PDF/DOCX/SVG selections; keep the URI/path/split-view resolver.
- Verify no redundant file chooser when files are selected; run the 16-scenario matrix.
- Add `scripts/uninstall`/postrm cleanup for both EN/UA menu directories.
- Ensure the package installs scripts for the **current user session**, not just `/etc/skel`.

**Acceptance:** a non-technical user can seal/verify a selected document in ≤3 clicks, sees progress
and a clear result, and the menu is not a wall of 16 entries.

### P0.5 Verification report (the actual legal deliverable)

- `marma-watermark verify --json` and a human-readable PDF report:
  document SHA-256, signer info, PAdES/QES status, seal presence, page policy, geometry deltas,
  recipient canary result, timestamp, tool version, environment; evidence bundle hash.
- Store report + document hash; do not claim court admissibility without a legal opinion.
- This is more valuable to a lawyer than another crypto feature.

**Acceptance:** one command/action produces a signed-off verification report a lawyer can attach to
an evidence memo; report is reproducible.

### P0.6 Buyer validation (do this in parallel, not after coding)

- 10 interviews: 5 law firms/M&A counsel, 3 notaries/forensic experts, 2 VDR/DMS product leads.
- Ask about the **last leak/tamper incident**, current workaround, budget owner, willingness to pay.
- Target 3 pilot LOIs / 1 paid pilot; define success metrics: time-to-verify, false positives,
  user comprehension, number of sealed documents.
- Do not build a SaaS before a paid pilot.

## P1 — 15–45 days

1. **Minimal API/SaaS**: authenticated upload/verify, audit log, report download, usage metering;
   keep client-side/private option.
2. **DOCX/batch parity** in the browser/API (currently CLI-only); batch verification.
3. **VDR/DMS integration**: one partner (Datasite/Intralinks/iManage/NetDocuments) or a simple
   webhook/API; do not build a VDR.
4. **Robust invisible watermark**: partner or add-on for screenshots/photos/printouts; otherwise
   remove broad leak-tracing claims permanently.
5. **Legal/forensic opinion** and one case study; security review; explicit limitations.
6. **Pricing/pilot package**: fixed pilot fee + per-case forensic service + annual enterprise licence.
7. **TIFS**: log decision; do not make publication a GTM dependency.

## P2 — 45–90 days

- SSO/RBAC/audit retention; data residency; SOC 2/ISO 27001 roadmap (only if enterprise pilots demand).
- Channel: legaltech/M&A partners, not Product Hunt.
- Case studies and reference customers; partner marketplace.
- Optional: CAD/SVG IP-protection wedge (SealPath/Autodesk ecosystem is strong; only if a design
  partner pulls it).

## What NOT to do

- Do not build a VDR or a full e-signature product.
- Do not compete head-on with EchoMark/Digimarc on robust forensic watermarking without a robust
  channel.
- Do not add more cryptographic primitives or academic features before a paid pilot.
- Do not claim “trace any leaked copy” for screenshots/photos with a fragile vector seal.
- Do not rely on Product Hunt/Nicheloom crypto audiences for distribution.

## Success scorecard (90 days)

| Metric | Target |
|---|---|
| Buyer interviews | 10 |
| Pilot LOIs | ≥3 |
| Paid pilots | ≥1 |
| Case study / legal opinion | 1 |
| Website demo → pilot request | measurable conversion |
| Clean-Debian `.deb` install/upgrade test | PASS |
| Nautilus seal/verify in ≤3 clicks | PASS |
| Browser/CLI payload parity or explicit demo label | PASS |
| Broad leak-tracing claim removed/qualified | PASS |

## References

- Niche and competitor analysis: `docs/research/NICHE_ANALYSIS_2026-10-25.md`
- Website audit: `docs/WEBSITE_AUDIT_2026-10-25.md`
- Product Hunt copy: `docs/producthunt/PH_UPDATE_2026-10-25.md`
- TIFS record: `paper_v3/drafts/tifs/SUBMISSION_CONFIRMATION_2026-10-25.md`

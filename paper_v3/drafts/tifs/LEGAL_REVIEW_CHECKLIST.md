# Legal review checklist — technical seal vs. Ukrainian company/notary seal

**Status:** checklist for the owner's lawyer; **not legal advice**. No legal conclusion is made here,
and nothing in this file should be filed or relied on without a Ukrainian-qualified lawyer.

## 1. What the product seal is, and what it is not
- It is a **technical integrity mark**: the visible vector seal carries a digest of the document and
  a recipient identifier. It proves tamper-evidence and attribution relative to the signed bytes.
- It is **not** a company seal (печатка підприємства), **not** a notary seal, and **not** a qualified
  electronic signature (КЕП/УЕП). It must never be presented as any of those.
- The production profile P2 is a **42 mm round branded stamp** (`data-profile="v2-round42"`,
  brand "Marma-Crypto"). The brand and explicit profile metadata are intended to prevent confusion.

## 2. Questions for counsel (Ukrainian law)
1. **Business entity seal.** Is a seal required for the specific document type / counterparty /
   bank / court filing? Does the company's statute or internal rules regulate its form, size or
   scope? (Requirements vary by document and practice; do not assume a universal 40–45 mm rule.)
2. **Notarial documents.** Notarial seals are regulated separately (Law of Ukraine "Про нотаріат"
   and the Порядок вчинення нотаріальних дій). Confirm that a technical stamp is never placed where
   a notarial seal/act is required, and that no visual imitation is possible.
3. **Court filings.** Electronic filing requires КЕП under the procedural codes; paper copies may
   require a seal where a rule or contract says so. Confirm that a technical seal is presented only
   as additional evidence/integrity information, not as a substitute.
4. **Contracts and data rooms.** May the parties agree to technical sealing and to the verification
   protocol as a contract annex? What is the evidentiary weight of the technical verification report
   (expert examination, notarial inspection, or contractual acceptance)?
5. **Personal data.** The recipient identifier is a 10-bit pseudonymous code, not a name. Confirm
   disclosure/notice requirements under the Law "Про захист персональних даних" and GDPR (if EU
   recipients), and that marking is disclosed in data-room terms.
6. **Patent / IP.** The pending Ukrainian application `a 2026 06266` covers the sealing method;
   confirm scope of claims for the P2 visual design and branding before commercial use.
7. **Marketing / impersonation.** Confirm that the round P2 stamp with text/brand cannot be
   confused with a state, notary or third-party seal; add a visible "TECHNICAL SEAL" legend if needed.

## 3. Safe defaults until counsel signs off
- Keep the real **КЕП/company seal process separate**; the technical seal is supplementary.
- Label the product seal in UI/docs as **"technical integrity seal"**, not "печатка".
- Keep the profile metadata (`data-profile`) and verification report in the document package.
- Do not use the technical seal on notarial acts, court originals, or documents of third parties.
- Retain the verification report and the signed document hash for evidentiary chain.

## 4. Evidence to give counsel
- `src/marma_seal_profiles.py` (profile logic), `src/marma_watermark.py` (sign/verify),
  `paper_v3/tests/controlled_run/CONTROLLED_RUN_REPORT.md` (technical verification),
  `paper_v3/REVIEWER_PROOFING.md` (claims/limits), `PUBLICATIONS.md` §5.2c (venue policy).
- A sample P2 SVG and its verification JSON (no client data).

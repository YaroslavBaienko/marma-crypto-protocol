# Website audit — yaroslavbaienko.github.io/marma-crypto-protocol (2026-10-25)

**Scope:** live page, local `docs/index.html`, links, metadata, mobile rendering, feature claims and
product value. **Verdict:** functional and technically credible, but the landing page under-sold the
product and mixed browser-demo and production-CLI capabilities. The high-impact issues are now fixed;
remaining items are listed below.

## Scorecard

| Area | Before | Now | Notes |
|---|---|---|---|
| Value proposition in first screen | weak | good | Hero now says seal/verify/trace and shows three primary CTAs |
| Primary CTA | whitepapers only | fixed | Seal / Verify / Install CTAs added |
| Browser vs CLI accuracy | mixed | fixed | Browser demo = v1.3 256-bit; production CLI = v2.1.0 266-bit; DOCX via CLI |
| Feature discoverability | low | improved | Value cards, Quickstart, seal-page policies, Nautilus, release link |
| Mobile header | wrapped 3 lines | fixed | Brand stacks; nav wraps; CTA full-width |
| SEO/social metadata | old v2.1 title | improved | Title/OG/Twitter updated to v2.2.0 and accurate scope |
| SEO/citation metadata | paper metadata | preserved | Academic citation block remains v2.1.0 paper; product software is v2.2.0-5 |
| Internal assets | pass | pass | whitepapers, protocol PDF, OG card, UA page present |
| External links | mostly pass | pass | DOI HEAD returns 403 to curl (bot protection); resolves in browser |
| i18n coverage | partial | pass | 83 EN / 83 UK keys; no missing `data-i18n` keys |
| Duplicate IDs | pass | pass | none found |
| JS runtime | pass | pass | page renders; language toggle and verifier logic untouched |

## What was fixed in `docs/index.html`

1. Title, meta description, OpenGraph and Twitter cards now describe the product, not only the verifier.
2. Hero rewritten around **Seal · Verify · Trace**, with primary CTAs to the sealer, verifier and CLI.
3. Three value cards: Sealer, Verifier, Leak tracing.
4. **Quickstart** section added: signed APT repository, GitHub `.deb` release, CLI verification, Nautilus.
5. Product proof line: open source, 266-bit CLI payload, 1,800+ reproducible runs, v2.2.0-5, TIFS 2026
   manuscript submitted (preprint on Zenodo; not accepted).
6. Header navigation added (`Seal`, `Verify`, `Install`, `Zenodo DOI`, `GitHub`); mobile layout fixed.
7. Browser/CLI scope is now explicit; production 266-bit payload and DOCX support are attributed to the
   CLI, while the browser sealer is labelled as the v1.3 256-bit demo.
8. Footer version corrected to `software v2.2.0-5 · protocol v2.1.0`.

## Remaining recommendations (not blocking)

- `og_card.png` was regenerated on 2026-10-25 (Seal / Verify / Trace, software v2.2.0-5, protocol v2.1.0); deploy and verify social previews.
- Update `docs/ua.html` hero/community copy to mirror the new value cards; the release banner is current.
- Add a short “Limitations” block visible above the FAQ: browser demo vs CLI, 8-decimal writer, flattening,
  no QES replacement. The sealer paragraph covers this but is long.
- The FAQ block is very dense; consider collapsing to `<details>` or splitting into “For lawyers” and
  “For engineers”.
- UI and language toggle were exercised via Chrome DevTools: EN/UK headings and value cards switch correctly; nav anchors `#sealerStudioCard`, `#verifier`, `#quickstart` resolve. Add `aria-live` to the verification result panel and test keyboard focus on the new CTAs.
- Consider a real 60-second demo video/GIF for Product Hunt instead of only screenshots.

## Functional checks

- Local render: Chromium headless at 1440 px and 390 px; hero/CTA/cards/sealer render correctly.
- No duplicate `id` attributes.
- `data-i18n` keys: EN 83 / UK 83; no missing keys.
- Internal assets exist: EN/UA whitepapers, protocol PDF, `ua.html`, `og_card.png`.
- External links: GitHub, Product Hunt, X, LegalTech APT repo return 200; DOI redirect returns 403 to
  HEAD/curl due bot protection but is valid in a browser.
- The page is static; no server-side dependencies.

## Deployment

Commit `docs/index.html`; GitHub Pages must rebuild. Verify the live page after deployment (cache bust
with `?v=20261025` if needed) and then update the Product Hunt gallery/first comment.

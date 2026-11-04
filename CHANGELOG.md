# Changelog

## Unreleased

- **Added 28 further photorealistic CC0 assets** (expansion-08) across instruments, optical science, computing, audio, appliances, ceiling lighting, carts and safety, bringing the library to **84 approved assets in 32 categories**. Across expansion-07 and expansion-08 that is 57 new assets, all visually reviewed across twelve views before promotion.
- Rejected the compact electric stove: a legible ARINA manufacturer badge in the full-size front view, plus an unfinished open rear cavity. Rejected the leather binder notebook in the previous batch for the same trademark reason.
- Wrote down the marks policy in `docs/research.md`: a legible real manufacturer's mark is a rejection, an obviously invented brand is approved with a recorded limitation, and generic specification text or ornament is fine. Upstream's `tmwarn` flag is a first filter, not the decision — neither rejected asset carried it.
- Hardened HTTP retries after a Poly Haven CDN 500 cost one candidate: four attempts spanning ~14 s instead of three spanning ~6 s. Writing the test exposed a real bug — `raise_for_status()` raises `RequestException`, so permanent 404/403 responses were being retried too. Client errors now fail on the first attempt.
- **Added 29 new photorealistic CC0 assets across 13 new categories** (expansion-07): hand tools, power tools, measuring instruments, cookware, tableware, vegetables, baked goods, vases, books, storage furniture, beds, desks and lamps. The library now holds 56 approved assets in 25 categories, all saved with 2K textures, twelve inspection views and full provenance.
- Rejected the leather binder notebook at the visual gate despite excellent model quality: the full-size top view shows an embossed manufacturer emblem, and CC0 does not grant trademark rights. Rejection evidence is preserved under `reports/rejected/`.
- Fixed a duplicated link line in the generated category pages; each asset now emits exactly one links row.
- **Retired all six KayKit assets** (4 characters, a chair and a table; 18.2 MB of payloads deleted) to respect Kay Lousberg's request that unmodified copies not be resold or claimed as one's own. Added `retire` as an auditable CLI operation with per-asset records under `reports/retired/`, and closed the KayKit sources to future intake.
- Made an author's stated request a blocking policy in `config/license-terms.json` and its schema, rather than a footnote: a source whose creator asks that copies not be redistributed is no longer eligible even though CC0 would allow it.
- Registered 20 new categories across tools, kitchen, food, decor, storage furniture, beds, desks, lighting, computing, optical science, music, watercraft, safety and office supplies.
- Added a budget-aware Poly Haven resolution picker: the highest resolution that fits the per-package storage budget is chosen, the fallback is logged, and upstream trademark-flagged assets are refused at intake.
- Discarded 27 MB of superseded Grab3D quarantine payloads whose repaired versions are already approved, keeping the failure records and logs.

- Added a per-asset license audit: `config/license-terms.json` records verified provider terms and caveats, `license-audit` checks all 33 approved assets against them, and results are published as `docs/licenses.md` plus `reports/license-audit.json`. CI verifies both with `--check`.
- Recorded the honest caveats instead of a blanket "no restrictions": KayKit's creator request not to resell unmodified copies, Kenney's `/license` page returning 404 (pinned pack license used as evidence), Poly Haven's separate API/site-content terms, Grab3D's AI-assisted disclosure, and the trademark/patent limits of CC0.
- Manifest and gallery now carry per-asset `license_notes` and `resale_as_is`, so the caveat is visible next to the download button.
- Added a Grab3D source adapter with per-package CC0 manifest/license verification and AI-origin disclosure preservation.
- Added expansion batch `expansion-05`: Grab3D realistic rigged male/female base characters, MakeHuman casual adult retries, a vintage brass chandelier and a barber shop chair; introduced the `lighting/chandeliers` category.
- Fixed the MakeHuman headless addon entry for Blender 4.2 by creating an empty addon preference entry and assigning its module name separately.
- Added a recorded, deterministic glTF skin-weight normalization repair for auto-rigged packages whose weight sums drift slightly; original and repaired checksums are preserved.
- Approved and promoted a vintage brass chandelier and barber shop chair, bringing the library to 30 approved assets in 12 categories.
- Got the pinned MakeHuman/MPFB headless build working end-to-end, then rejected the first casual male/female outputs at the visual gate because of blank eyes, face-obscuring hair and prominent community-logo clothing.
- Added expansion batch `expansion-06` to re-intake the repaired Grab3D realistic rigged humans and add elderly/teen realistic human variants.
- Approved and promoted three realistic rigged Grab3D humans (adult male base, adult female base, elderly woman), bringing the library to 33 approved assets in 12 categories; rejected the anime-styled teenager for the realistic-human category.
- Added a live static library gallery with category chips, search, style/rig filters, sorting, category grouping, auto-refresh, asset detail views, downloads and source/license links.
- Approved and promoted 28 CC0 assets into the organized `assets/` library, with manifest, category pages, checksums, licenses, previews, logs and review evidence.
- Added realistic and stylized variants for chairs, tables, sofas, fruit, humans, vehicles, plants, toys, industrial props and retail props.
- Rejected the mislabeled Kenney wall-decor bear from the toy category and preserved rejection evidence.
- Fixed inspection framing to use visible evaluated vertices instead of hidden helpers.
- Added expansion batches for a rubber duck toy, side table, KayKit table and MakeHuman realistic humans.
- Fixed MakeHuman CI loading by registering pinned MPFB2 under Blender extension package naming.
- Made the intake pipeline cancellable and added MakeHuman build-stage logging; removed unnecessary MPFB UI asset-list scanning.
- Added maintainer technical guide and research/licensing decision log.
- Established a CC0-only intake policy, source registry and subject-based category structure.
- Added immutable GitHub source revisions and official Poly Haven API resolution.
- Added lossless embedded-texture extraction, local dependency checks and SHA-256 inventories.
- Added a five-worker, request-triggered GitHub Actions pipeline with repository-persisted logs and candidates.
- Added Blender inspection: eight azimuths, top, bottom, clay and triangle-wireframe views.
- Added explicit quarantine and visual-review gates; downloads cannot publish themselves to the approved catalog.
- Added initial request for 26 candidates across realistic and game-ready categories.
- Added unit tests for request partitioning, path safety, texture preservation and HTTP allowlists.

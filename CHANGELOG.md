# Changelog

## Unreleased

- Added a Grab3D source adapter with per-package CC0 manifest/license verification and AI-origin disclosure preservation.
- Added expansion batch `expansion-05`: Grab3D realistic rigged male/female base characters, MakeHuman casual adult retries, a vintage brass chandelier and a barber shop chair; introduced the `lighting/chandeliers` category.
- Fixed the MakeHuman headless addon entry for Blender 4.2 by creating an empty addon preference entry and assigning its module name separately.
- Added a recorded, deterministic glTF skin-weight normalization repair for auto-rigged packages whose weight sums drift slightly; original and repaired checksums are preserved.
- Approved and promoted a vintage brass chandelier and barber shop chair, bringing the library to 30 approved assets in 12 categories.
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

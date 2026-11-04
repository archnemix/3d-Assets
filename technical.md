# Technical guide

This repository is a file-based CC0 3D asset library, not a web application. The durable product is the approved asset tree, its manifest, and the evidence that each asset passed license, technical, and visual review.

## Architecture

```text
automation/request.json       Trigger file for GitHub Actions intake
automation/*.json             Archived batch requests
config/sources.json           Pinned source adapters and license evidence
config/license-terms.json     Recorded per-provider license terms and caveats
config/categories.json        Category/subcategory taxonomy
config/human-recipes/         MakeHuman recipes for generated CC0 humans
schemas/                      JSON Schemas for requests, recipes, reviews, retirements
src/asset_library/            Python CLI and pipeline modules
  sources/                    Source adapters: Poly Haven, GitHub, MakeHuman, Grab3D
  gltf_repair.py              Bounded, checksum-recorded glTF portability repairs
  intake.py                   Candidate acquisition and quarantine orchestration
  inspection.py               Blender render/inspection subprocess boundary
  review.py                   Explicit visual approval/rejection gate
  retire.py                   Withdraw published assets; payloads deleted, reason kept
  licensing.py                Per-asset license checks against recorded terms
  license_report.py           Markdown rendering of the license audit
  catalog.py                  Approved-only manifest and category pages
  refresh.py                  Re-render existing quarantine candidates
  requests.py                 Batch validation and shard partitioning
rendering/                    Blender scripts and scene/metric helpers
scripts/                      Small Node/shell helpers used by CI
reviews/                      Human/agent visual review decisions
assets/                       Approved assets only
quarantine/                   Unapproved candidates and failed builds
reports/                      CI shard reports, logs, rejected review evidence
research/                     Pinned license/source research
gallery/                      Static approved-only browser gallery
```

The pipeline deliberately separates four states:

1. **Requested** — a candidate appears in `automation/request.json`.
2. **Quarantined** — files are downloaded/generated and inspected, but not recommended.
3. **Reviewed** — a decision file in `reviews/` records scores, notes, limitations, and the exact contact-sheet hash.
4. **Approved** — `review` moves the candidate into `assets/<category>/<subject>/<id>/`, and `catalog` rebuilds `manifest.json` and category pages.

A successful download or render is not approval.

## Local setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci --ignore-scripts
```

Blender is required only for rendering/generation. CI installs a pinned Blender build through `.github/actions/blender`. The sandbox used for early development did not have a usable local Blender, so Blender-dependent paths are exercised in GitHub Actions.

Common commands:

```bash
PYTHONPATH=src .venv/bin/python -m asset_library plan automation/request.json
PYTHONPATH=src .venv/bin/python -m asset_library review reviews/<batch>.json
PYTHONPATH=src .venv/bin/python -m asset_library catalog
PYTHONPATH=src .venv/bin/python -m asset_library catalog --check
PYTHONPATH=src .venv/bin/pytest -q
.venv/bin/ruff check src tests rendering scripts
.venv/bin/ruff format --check src tests rendering scripts
npm run test:gallery
npm run check:web
```

## GitHub Actions intake

The reliable trigger is a push that changes `automation/request.json` on the session branch. Manual dispatch and artifact/log download APIs were unreliable in this environment, so the workflow commits candidate files, logs, and shard reports back to the repository.

Workflow: `.github/workflows/asset-intake.yml`

- Validates schemas, lint, tests, and gallery formatting.
- Plans at most five disjoint shards.
- Runs no more than five concurrent inspection jobs.
- Each worker writes `reports/intake/<batch>/worker-N.log` and `shard-N.json`.
- Candidate payloads go to `quarantine/<batch>/<id>/`.
- Bot commits use `[skip ci]` and do not retrigger intake.
- Shared concurrency prevents overlapping intake/refresh pushes where possible; a newer request can cancel an older stuck intake run.

If a push races with a bot commit, fetch and rebase before retrying:

```bash
git fetch origin <branch>
git rebase origin/<branch>
git push origin <branch>
```

## Asset folder contract

Approved assets live at:

```text
assets/<category>/<subject>/<asset-id>/
  model/          Actual glTF/GLB and required buffers/textures
  textures/       Convenient extracted/copied texture maps when applicable
  previews/       12 inspection views, contact sheet, geometry/views JSON
  logs/           Blender and validator logs
  provenance/     Source/license/API/build evidence
  LICENSE.txt     Asset license text/evidence
  README.md       Asset-specific usage notes
  asset.json      Machine-readable metadata
  review.json     Visual review decision and sheet hash
  SHA256SUMS      Inventory checksums
```

Variants of the same subject share the subject folder. For example, realistic and stylized chairs both live under `furniture/chairs/`, but each asset keeps its own folder, license, textures, and metadata.

## Review gate

`reviews/*.json` decisions are intentionally explicit. Approval requires:

- license policy `CC0-1.0`;
- batch/id identity match;
- inventory checksums verify;
- zero glTF validator errors;
- exact contact-sheet SHA-256 match;
- five integer scores, each at least 4, with mean at least 4.6.

Rejections preserve the contact sheet and review JSON under `reports/rejected/` without keeping the failed model payload in the approved library.

## Retiring an asset

Approval is reversible. `python -m asset_library retire reviews/<decision>.json` withdraws a
published asset: it verifies the inventory and provider first, writes a record to
`reports/retired/<id>/retirement.json` (reason, decider, date, removed byte count, model SHA-256),
then deletes the asset folder. The payload is deleted rather than moved, because honouring
"please don't redistribute this" means the files leave the repository.

Retirement is all-or-nothing: every entry is validated before any folder is touched, so a bad
entry cannot leave the library half-retired. `catalog` and `license-audit` are re-run afterwards.

## License audit

The license question is answered per asset, not per provider slogan. `config/license-terms.json`
records what each source actually grants, where that was read, and every caveat found; it is
validated by `schemas/license-terms.schema.json`, which refuses to describe a source as
attribution-bearing, paid, or resale-restricted while the library claims otherwise.

`python -m asset_library license-audit` walks every approved `asset.json` and checks:

| Check | Meaning |
| --- | --- |
| `free_of_charge` | The provider distributes the asset at no cost |
| `cc0_spdx` | Asset and source metadata both say `CC0-1.0` |
| `cc0_text_present` | The stored `LICENSE.txt` really contains a CC0/public-domain dedication |
| `license_file_checksummed` | That file matches the asset inventory checksum |
| `no_attribution_required` | `attribution_required` is `false` |
| `commercial_use_allowed` | Commercial use is recorded as allowed |
| `redistribution_allowed` | Redistribution is recorded as allowed |
| `evidence_recorded` | Asset and source agree on one HTTPS evidence URL |
| `source_terms_verified` | The provider has recorded, verified terms |
| `standalone_resale_permitted` | The provider terms permit as-is/standalone use |
| `textures_included` | Every listed texture file is present on disk |
| `no_trademark_warning` | No upstream trademark warning flag in stored API metadata |
| `visually_approved` | The asset passed the visual gate |

Output is `reports/license-audit.json` (machine-readable, per-asset checks and license-file
SHA-256) and `docs/licenses.md` (readable per-asset table, caveats and evidence links).
`--check` recomputes both and fails if either is stale or any asset fails a check, so the
audit cannot silently drift from the files. CI runs it in the plan job next to `catalog --check`.

`catalog.py` reads the same terms file, so `manifest.json` carries `license_notes` and
`resale_as_is` per asset and the gallery detail panel shows the caveat next to the download
button. Provider terms live in exactly one place.

## Inspection standard

Each candidate is rendered from the actual downloaded/generated model:

- eight 45-degree orbit views at a fixed elevation;
- top and bottom views;
- clay view;
- triangle-wireframe view;
- labeled 3x4 contact sheet.

Framing uses visible evaluated vertices, not helper objects or hidden empties. This fixed an early bug where hidden helpers inflated bounds and produced tiny/off-center sheets.

## MakeHuman humans

MakeHuman candidates are generated from the official CC0 system pack using MPFB2 as a GPL build tool. The tool license does not infect the exported CC0 asset data. The pipeline preserves recipe descriptors, pack checksums, build logs, and a build report.

Important implementation detail: MPFB 2.0.18 expects Blender 4.2 extension package naming. Loading it as plain `mpfb` fails in `LocationService` because `bpy.utils.extension_path_user("mpfb")` is not a valid extension package. `rendering/build_makehuman.py` therefore loads the pinned MPFB source as `bl_ext.user_default.mpfb` before registering it.

The generated humans are still subject to the same quarantine, render, validator, and visual-review gates as downloaded assets.

## Adding a source or category

1. Add or update `config/sources.json` with immutable revision/checksum evidence.
2. Add a focused adapter under `src/asset_library/sources/` if the source needs new acquisition logic.
3. Add category labels to `config/categories.json` only when the subject grouping is meaningful.
4. Add candidates to a new archived batch request, then copy it to `automation/request.json` to trigger CI.
5. Review the rendered sheets, write `reviews/<batch>.json`, run `review`, then `catalog`.
6. Run `catalog --check` and the test/lint suites before publishing.

## Storage and repository hygiene

- Approved assets are real files in Git, not artifact-only outputs.
- Do not commit `.work/`, caches, or temporary downloads.
- Keep failed payloads out of `assets/`.
- The workspace has an approximate patchset cap; avoid adding large unapproved batches unnecessarily.
- Prefer pinned revisions and checksums over floating URLs.

## Known limitations

- Some upstream low-poly assets contain a small number of zero-area triangles; accepted cases record this in review limitations.
- Stylized flat-color assets may have no image textures; this is intentional and recorded.
- Rigged characters are inspected in rest pose; target-engine animation import still needs project-specific testing.
- Realistic MakeHuman generation depends on Blender/MPFB behavior in CI and is retried through the same request-triggered workflow when fixes land.

# Library review and revised priorities — 2026-11-06

## Scope and limitations

The user requested broadly useful, high-quality assets, not a human-first expansion;
new humans should be exceptional and have many animations. Seek enterable buildings,
complete maps, realistic vehicles and coherent packs, while filling sparse categories.
Retain CC0, standalone resale, no-attribution and visual/technical approval gates.
This is an initial review, **not** a completed audit of every model or its current
upstream rights. No new assets have been approved in this pass.

## Automated baseline

Before recategorization, the approved manifest had 270 assets in 73 populated
categories: 173 labelled realistic, 73 stylized, 24 low-poly. Those are existing
metadata labels, not fresh visual assessments. Sources by recorded source URL:
149 Grab3D, 111 Poly Haven, 10 Kenney mirror. All 25 entries under `buildings/`
were labelled stylized. Many populated categories had at most two entries.

The catalog check verified the inventories and the existing review-record/contact-sheet
hashes for all 270 assets. The license audit check passed 270/270 **against recorded
provider terms, local license text markers, checksums, evidence URLs, and metadata**.
This does not re-check all upstream terms or authors' current requests, prove rights in
third-party trademarks, establish animation quality, or independently reproduce the
historical visual reviews. In particular, the handoff documents questionable visual
review provenance for expansions 17 and 18. Do not describe these checks as a fresh
independent legal or visual certification.

## Initial visual categorization

The following observations are from the existing local contact sheets. They do not
establish playable interiors, compatibility, quality of animation or a complete theme pack.
The sheets were originally created during intake and still carry a candidate label; the
approved status is determined by the current manifest and records, not that label.

- `g3-mushroom-house`: pink spotted mushroom-shaped fantasy cottage. Moved from
  `buildings/houses` to `buildings/houses/fantasy`. The exterior views don't show
  an explorable interior. Three recorded door-animation frames show the closed door
  then an apparently dark opening; the door itself is not clearly visible in the
  latter frames, so motion quality and actual enterability remain unconfirmed.
- `g3-beach-house`: clean, stylized modern villa with a pool. Moved from
  `buildings/houses` to `buildings/houses/modern`. Exterior renders do not demonstrate
  a usable interior.
- `g3-bank`: stylized neoclassical bank exterior; retained under
  `buildings/commercial`. Its contact sheet does not establish an enterable interior.

These are only three of 270 visual checks. Remaining assets still require visual
reassessment before wholesale recategorization; the existing categories have not all
been reorganized. Do not infer complete matching packs from a shared theme label.

## Source lead: ModKit modular industrial environment

- Repository: https://github.com/JaronKBragg7337/asset-pack-ue-threejs-blender-unity
- Inspected revision: `f5a53eaadbb46fac8e29faabb6c0ac1b6c6d2311`.
- Its pinned [README](https://github.com/JaronKBragg7337/asset-pack-ue-threejs-blender-unity/blob/f5a53eaadbb46fac8e29faabb6c0ac1b6c6d2311/README.md)
  states meshes, scripts and renders are CC0 and notes commercial use and no required
  attribution. The pinned [license](https://github.com/JaronKBragg7337/asset-pack-ue-threejs-blender-unity/blob/f5a53eaadbb46fac8e29faabb6c0ac1b6c6d2311/LICENSE)
  contains CC0 1.0. The repository provides GLB modules and an assembled industrial
  outpost example. The pack is described as procedural and not texture-based, so it
  is not evidence of photorealistic PBR models.
- **Lead only:** no model was imported or locally rendered, no per-file dependency,
  authorship, third-party-rights or creator-request review has been completed, and no
  source adapter or approved license-terms entry exists. Verify the exact exports,
  ability to navigate the assembled interior, compatibility, materials and rights before
  intake or approval. Never treat an upstream preview as our own inspection render.

A search result for `pyrokitty64/mesh-stuff` could not be verified: GitHub returned 404.
It must not be treated as a usable or cleared source on that evidence.

## Pipeline work and next steps

The request limit is now 50, split among at most five workers. A 150-minute worker
timeout is configured, but a full 50-item run has not yet been benchmarked. Catalog,
license audit, animation targeting and retirement discovery now support deeper category
paths. The gallery can filter by parent category. Only the two houses above have been
moved so far; keep paths, per-asset inventories, catalog and audit synchronized on
future moves.

Next, independently check exact source and asset rights and inspect every asset's
renders and model before migration; verify interiors in-model, not from exterior images.
Prioritize useful themed collections that visually and technically fit together.
Research realistic cars and complete maps without lowering the license standard.
Local Blender was not installed in this environment; CI intake needs a suitable new
request and an available runner. The previous Innerscene batch remains unapproved and
its documented redirect, cache and terms issues still require resolution.

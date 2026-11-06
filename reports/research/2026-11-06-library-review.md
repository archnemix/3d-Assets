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

## Follow-up: Skyborn Building Studio release lead

The [pinned v1.0.0 README](https://github.com/holokat/building-studio/blob/a4c4d0381ea478c79649e8e750553ffdeb4845bf/README.md)
states that buildings, props and their textures are CC0, no attribution required;
application code and runtime are separately MIT. Its [pinned asset catalog](https://github.com/holokat/building-studio/blob/a4c4d0381ea478c79649e8e750553ffdeb4845bf/downloads.json)
lists individual downloadable GLBs with byte counts and SHA-256 hashes. Its release
notes say engine-specific collision, LODs and gameplay integration remain separate work,
and browser-specific material effects may not match standard glTF viewers. The
creator describes a walk-inside viewer; that is not independent proof the exported
building is readily enterable. A one-building intake request is prepared to validate
this before expanding the set. The sandbox cannot reach GitHub's release-asset host;
the Actions worker must acquire it and verify the exact catalog hash. The later README
links v1.1.0, but that release was not available through GitHub when checked; the
request intentionally pins the existing v1.0.0 release and its corresponding catalog.

## Additional source-record cross-check

A local pass over all 270 currently approved `asset.json` records checked source-specific
stored evidence beyond the generic audit: 149/149 Grab3D assets have a saved package
manifest whose declared license is `CC0-1.0` and whose slug agrees with the asset and
package provenance; 111/111 Poly Haven assets have saved API metadata with an author
map; 10/10 Kenney conversions have a saved GitHub provenance record whose pinned commit
and path agree with the asset record. This verifies the presence and internal consistency
of stored acquisition evidence, not the identity of each uploader, live terms, ownership
of third-party material, or visual freedom from trademarks. The catalog and audit also
verify inventories and license text hashes. Further independent rights review remains
necessary where provenance or creator requests are uncertain.

## Further local contact-sheet review

Five additional existing assets were reviewed visually for category placement only.
The witch cottage moved to `buildings/houses/fantasy`, the fairy-tale castle to
`buildings/landmarks/fantasy`, and the western general store to
`buildings/commercial/western`. Their exterior sheets do not prove usable interiors.
The 1960s sports car moved to `vehicles/cars/classic` and the electric city car to
`vehicles/cars/electric`; both appear stylized rather than photorealistic. These
categorization checks did not re-assess full-size views, movement or actual interiors
and are not a complete quality re-review. The library remains at 270 assets, now
in 78 populated categories.

## ModKit intake results

GitHub Actions run `42182214678` completed successfully across five workers: all 39
candidates passed technical intake. Twelve structural modules were subsequently visually
reviewed and approved; see the three `reviews/modkit-industrial-01-*.json` files. Two container props were also subsequently approved; the other 25, including the assembled outpost, remain in quarantine. The outpost's orbit
renders are distant and do not establish interior navigation, and its geometry report
records 215 zero-area triangles; it requires closer review before any approval. The
crate-stack preview shows three bare, simple cuboids and should not be represented as
a richly detailed crate asset. The approved pieces are static, untextured and
stylized; they do not solve the realistic vehicle or enterable building gaps.

## Skyborn caretaker hut: quarantine review

Run `42184203079` downloaded the pinned release payload and rendered it successfully.
The contact sheet and enlarged oblique show a detailed textured timber-and-stone hut,
but the render presents the model sideways: the nominal bottom view shows its front
facade. This orientation needs investigation and correction before publication. The
interior and actual walkability are not demonstrated by these exterior renders. The
model has approximately 1.98 million triangles in 1,442 mesh objects, 145 zero-area
triangles, and the glTF validator reports zero errors but 144 generated-tangent-space
warnings. It remains quarantined; the job's technical pass is not a quality approval.
The original 30.7 MB GLB and extracted textures are retained as source evidence.

## Additional outpost interior views

Run `42184851260` produced a roof-hidden cutaway and two eye-level renders under
`reports/interior/modkit-industrial-outpost/`, without modifying the source GLB. The
cutaway shows a simple room with a stair, wall openings and a static door. The eye-level
renders show dark gaps between ceiling panels and a visibly raised stair base. They do
not test entry, stairs, collision or gameplay. Together with its 215 zero-area triangles,
these assembly issues keep the scene quarantined; it is not presented as a complete,
enterable map. The twelve separately approved kit pieces remain available independently.

## Additional industrial props

The large framed crate and closed ringed barrel were reviewed from all twelve inspection
views and enlarged oblique renders and approved as simple static, stylized industrial
props. They use flat materials, not detailed textures. The candidate labelled “open
barrel” appears capped in its renders and remains in quarantine; the pallet also remains
quarantined pending investigation of 32 zero-area triangles.

## Gobkit animated animal lead

Gobkit / Alsomind Tech Co., Ltd. provides its free models under CC0 in the pinned
repository `Ariescar/gobkit-free-assets` at
`4e73c68fa6e8ca9d948fcc0ce7215c830a022c3b`. Its README and LICENSE explicitly cover
commercial use and no attribution; CC0 permits standalone redistribution and resale.
Seven distinct stylized animals were requested for quarantine review. These original
repository exports have one continuous baked animation track with action frame ranges,
not separate named clips; the later named-clip files advertised on the live site have
not been acquired. Animation quality and suitability must be inspected before approval.

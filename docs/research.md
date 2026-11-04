# Research and licensing decisions

The library accepts only assets that can be used, modified, and redistributed without an attribution obligation. Source pages, archive licenses, and API terms were checked separately because a website label is not enough.

The per-asset verdict for every approved asset — free, no attribution, commercial use, standalone/as-is use, public display — is published in [the license audit](licenses.md) and verified in CI by `python -m asset_library license-audit --check`.

## Accepted source families

### Poly Haven

- Asset license: CC0.
- Discovery uses the official Poly Haven API.
- API service terms require a visible discovery-service credit: **Powered by Poly Haven**.
- That service credit is not an attribution condition on downloaded CC0 assets.
- Selected assets are resolved through `/info/{id}` and `/files/{id}`, then downloaded with their glTF buffers and texture maps.
- Accepted examples include realistic chairs, tables, plants, food, a barrel, a cash register, and a rubber duck toy.

### Kenney

- Original pack pages declare CC0.
- `https://kenney.nl/license` returned 404 on 2026-11-04; `https://kenney.nl/support` confirms all asset-page assets are CC0 and attribution is not required, and reserves the studio logo for official projects.
- The selected GitHub convenience mirror explicitly releases converted/embedded GLBs under CC0.
- The pipeline records the original creator and the exact mirror revision rather than presenting the mirror as the author.
- Accepted examples include low-poly characters, vehicles, furniture, fruit, and snacks.
- Some Kenney furniture uses intentional flat-color materials rather than image textures.

### MakeHuman / MPFB2

- Official MakeHuman system asset pack is CC0.
- Pack URL: `https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip`.
- Pack SHA-256: `b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107`.
- Pack size: 280,737,770 bytes.
- MPFB2 is the Blender build tool, pinned at commit `d0a32e57a7f915cb2f2b95410e2117648c7bbb7e`.
- MPFB2 code is GPL-3.0-or-later; it is used as a tool, not bundled as an asset dependency.
- Exported candidates contain only CC0 base mesh, targets, clothes, and textures from the official system pack.
- Generated humans are not approved until they pass the same visual and technical gates as downloaded assets.
- The first successful casual male/female builds were rejected visually: blank-looking eyes, face-obscuring hair and prominent MakeHuman-logo clothing. Future recipes should use generic clothing, readable eyes and face-clear hair.

### Grab3D

- Every published model is dedicated to the public domain under CC0 1.0.
- The license page explicitly allows commercial use, modification and redistribution without attribution, account or fees.
- Each download package ships its own `manifest.json` and `LICENSE.txt`; the adapter verifies both before downloading the GLB.
- Selected realistic human packages are rigged base characters with walk/run clips and 2K PBR textures.
- Grab3D discloses that many models are AI-assisted: a Meshy image-to-3D draft is cleaned up, scaled, textured and checked in Blender; rigged packages add Meshy Auto-Rig skeletons and clips.
- The pipeline preserves the package origin disclosure and tags candidates `ai-assisted`; visual approval is still required.
- Grab3D waives only its own rights. Subjects are described as generic, with no brands, logos or real people.
- The first rigged packages failed the Khronos validator because auto-rigged skin-weight sums drifted by about `1.7e-4`. The adapter applies a bounded, recorded normalization repair (divide each weight vector by its sum) and stores both upstream and repaired checksums. After repair the same packages report zero validator errors.
- Approved realistic examples: adult male base character, adult female base character and elderly woman. The teenage boy package was rejected for the realistic-human category because its face/hair read anime-stylized rather than realistic.

## Rejected or deferred candidates

### KayKit — withdrawn at the author's request

The character and furniture packs are genuinely CC0, and the pinned licenses say credit "is not
mandatory". But the Adventurers download page also asks: "please don't resell unmodified copies or
claim them as your own." This repository republishes unmodified copies publicly, which is exactly
the activity the author asked us not to do.

The user's direction was to respect that request, so on 2026-11-04 all six approved KayKit assets
were retired and their model files deleted: `kaykit-barbarian`, `kaykit-knight`, `kaykit-mage`,
`kaykit-rogue`, `kaykit-dining-chair`, `kaykit-table-medium`. Per-asset records are in
`reports/retired/`. Both KayKit entries were removed from `config/sources.json` and
`config/license-terms.json`, so no future batch can reintroduce them, and a gallery test asserts
the family stays out of the manifest.

The general rule is now recorded in the license policy: **an author's stated request about use is
honoured even where CC0 would legally permit more.** A license is a floor, not a permission slip to
ignore the person who made the work.

### MB-Lab / ManuelbastioniLAB

MB-Lab data is AGPL-3.0, and generated characters are treated as AGPL derivatives. That is incompatible with the library’s no-strings/unrestricted-use policy, so it was rejected despite being a realistic human generator.

### avatar-studio prebuilt MPFB GLBs

`memoriesrohit/avatar-studio` contains realistic rigged MakeHuman/MPFB-derived GLBs, but the repository `LICENSE` is MIT for code and the CC0 claim for models is README-level. Deferred in favor of sources with explicit per-package CC0 dedications or the official MakeHuman system pack.

### Kenney “teddy bear”

The upstream asset named as a bear is a flat-backed wall trophy/decoration, not a plush toy. It was rejected from `toys/soft-toys` because the category mismatch would mislead users. The rejection evidence is preserved under `reports/rejected/`.

### Quaternius

Some current descriptions conflict, and at least one custom license includes redistribution restrictions. Deferred until an exact archive can be verified as unrestricted/CC0-equivalent.

### Sketchfab CC0 listings

CC0 filtering alone was not treated as sufficient because download barriers and listing-level provenance made bulk verification unreliable. Deferred.

### NASA

Government-hosted models are not automatically CC0. Media/endorsement guidelines and third-party rights require separate review. Deferred.

### Poly Haven material-only sets

Some Poly Haven entries are texture/material sets rather than glTF models. They were deferred because the current library focuses on model assets with preserved model dependencies.

## Quality policy

“Very high quality” is style-relative:

- Realistic assets need coherent silhouettes, believable materials, intact PBR maps, and clean presentation from all angles.
- Stylized assets are judged against their intended game art style, not rejected merely for low triangle counts.
- Every accepted asset still needs complete geometry, working materials, preserved textures, zero validator errors, and a visual check from all sides.

Minor upstream issues are recorded rather than hidden. Examples include a small number of zero-area triangles in low-poly props, informational tangent-space warnings, and rest-pose-only rig inspection.

## Evidence locations

- `research/` contains pinned license texts, source trees, and MakeHuman pack research.
- Each approved asset contains its own `provenance/`, `LICENSE.txt`, logs, review, and checksums.
- `manifest.json` is generated from approved assets only.
- `reports/intake/` contains CI shard reports and worker logs.
- `reports/rejected/` contains rejection evidence without approving the payload.

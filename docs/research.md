# Research and licensing decisions

The library accepts only assets that can be used, modified, and redistributed without an attribution obligation. Source pages, archive licenses, and API terms were checked separately because a website label is not enough.

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
- The selected GitHub convenience mirror explicitly releases converted/embedded GLBs under CC0.
- The pipeline records the original creator and the exact mirror revision rather than presenting the mirror as the author.
- Accepted examples include low-poly characters, vehicles, furniture, fruit, and snacks.
- Some Kenney furniture uses intentional flat-color materials rather than image textures.

### KayKit

- Pinned character and furniture repositories include explicit CC0 notices.
- Character pack revision: `672074b73ba276876a19e8816ecdc5241817ab47`.
- Furniture pack revision: `96d5930a8dbdb363409bbc2d3341718b00e17c9c`.
- Accepted examples include stylized fantasy humans and wooden furniture.
- External glTF dependencies and atlas textures are preserved.

### MakeHuman / MPFB2

- Official MakeHuman system asset pack is CC0.
- Pack URL: `https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip`.
- Pack SHA-256: `b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107`.
- Pack size: 280,737,770 bytes.
- MPFB2 is the Blender build tool, pinned at commit `d0a32e57a7f915cb2f2b95410e2117648c7bbb7e`.
- MPFB2 code is GPL-3.0-or-later; it is used as a tool, not bundled as an asset dependency.
- Exported candidates contain only CC0 base mesh, targets, clothes, and textures from the official system pack.
- Generated humans are not approved until they pass the same visual and technical gates as downloaded assets.

## Rejected or deferred candidates

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

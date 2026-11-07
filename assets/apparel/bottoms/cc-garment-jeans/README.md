# Jeans

- Creator: Kasper Olesen; MakeHuman system assets where listed
- Source: https://github.com/kblood/CharacterCreator/blob/852e48f316b90a0937234886630e4fb4cdfd1f78/output/clothing_jeans.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `apparel/bottoms`
- Intended style: realistic
- Import: `model/clothing_jeans.glb`
- Triangles: 1,712; mesh objects: 1
- Rig: True; animation clips: 0
- Texture images: 2

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Derivative GLB: all 92 mesh default morph weights were changed from 1 to 0; source and derivative hashes and unchanged binary-chunk hash are recorded in provenance.
- Contains a skin and morph targets, but character fit, retargeting, morph behavior and animation are not verified; no animation clips are supplied.
- Textured game-asset geometry, not photorealistic; upstream runtime tint/mask shader features are not guaranteed in generic GLB viewers.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

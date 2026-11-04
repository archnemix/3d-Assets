# Articulated industrial lamp arm

- Creator: Yann Kervran, Kuutti Siitonen
- Source: https://polyhaven.com/a/desk_lamp_arm_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `lighting/lamps`
- Intended style: realistic
- Import: `model/desk_lamp_arm_01_2k.gltf`
- Triangles: 24,102; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Not rigged in the shipped glTF; the arm cannot be reposed without adding constraints.
- No cable or plug is modelled.
- The shade emits no light by default; add an emitter in your scene.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Potted leafy plant

- Creator: Rico Cilliers
- Source: https://polyhaven.com/a/potted_plant_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `nature/potted-plants`
- Intended style: realistic
- Import: `model/potted_plant_01_2k.gltf`
- Triangles: 176,226; mesh objects: 4
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- 176,226 triangles and 132 zero-area triangles; use LODs or decimation for performance-sensitive scenes.
- Leaf cards rely on alpha testing/blending in the target engine.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

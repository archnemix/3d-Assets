# Flaky butter croissant

- Creator: Greg Zaal, Dario Barresi
- Source: https://polyhaven.com/a/croissant
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `food/baked-goods`
- Intended style: realistic
- Import: `model/croissant_2k.gltf`
- Triangles: 1,990; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Underside is a single flattened bake surface, so it should sit on a plate rather than float.
- Fixed shape; no bite or torn variants.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

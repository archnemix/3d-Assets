# Frosted carrot cake

- Creator: Greg Zaal, James Ray Cock
- Source: https://polyhaven.com/a/carrot_cake
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `food/baked-goods`
- Intended style: realistic
- Import: `model/carrot_cake_2k.gltf`
- Triangles: 13,790; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- 12.3 MB package, the largest in this batch, because of the dense scan geometry.
- No slice cut; the cake is whole.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

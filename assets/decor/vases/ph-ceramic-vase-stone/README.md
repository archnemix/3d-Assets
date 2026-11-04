# Stone-finish ceramic vase

- Creator: James Ray Cock
- Source: https://polyhaven.com/a/ceramic_vase_04
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `decor/vases`
- Intended style: realistic
- Import: `model/ceramic_vase_04_2k.gltf`
- Triangles: 9,000; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- A worn retail barcode sticker is baked into the base texture. No brand name or legible digits remain, but clone it out for product renders where the underside is visible.
- Handle is thin geometry and may alias at distance.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

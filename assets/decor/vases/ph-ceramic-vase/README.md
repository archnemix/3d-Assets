# Modern fluted white ceramic vase

- Creator: James Ray Cock
- Source: https://polyhaven.com/a/ceramic_vase_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `decor/vases`
- Intended style: realistic
- Import: `model/ceramic_vase_01_2k.gltf`
- Triangles: 10,296; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- A small barcode sticker is visible on the underside in the bottom view; it is a retail artefact, not a brand.
- Plain white glaze shows faceting if the renderer does not smooth normals.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Antique floral tea set

- Creator: James Ray Cock, Rico Cilliers, Jurita Burger
- Source: https://polyhaven.com/a/tea_set_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `kitchen/tableware`
- Intended style: realistic
- Import: `model/tea_set_01_2k.gltf`
- Triangles: 40,296; mesh objects: 10
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Supplied as a wide display layout of many pieces; the whole-set framing makes individual items small on the contact sheet.
- 40k triangles for the full set; separate and decimate the plates if you only need one piece.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

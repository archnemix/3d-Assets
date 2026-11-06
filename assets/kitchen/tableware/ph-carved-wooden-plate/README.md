# Hand-carved wooden plate

- Creator: Jan Martens
- Source: https://polyhaven.com/a/carved_wooden_plate
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `kitchen/tableware`
- Intended style: realistic
- Import: `model/carved_wooden_plate_2k.gltf`
- Triangles: 2,112; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Very pale bleached wood; may need a colour tweak to sit beside warmer timbers.
- Shallow profile means side-on views show little detail.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

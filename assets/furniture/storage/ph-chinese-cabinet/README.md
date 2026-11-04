# Antique Chinese wooden cabinet

- Creator: Kirill Sannikov
- Source: https://polyhaven.com/a/chinese_cabinet
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `furniture/storage`
- Intended style: realistic
- Import: `model/chinese_cabinet_2k.gltf`
- Triangles: 15,668; mesh objects: 5
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Rear panel is deliberately plain, so avoid placing it facing camera.
- Drawers and cupboard door are closed and not rigged.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

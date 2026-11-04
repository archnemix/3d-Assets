# KayKit medium wooden table

- Creator: Kay Lousberg
- Source: https://github.com/KayKit-Game-Assets/KayKit-Furniture-Bits-1.0/blob/96d5930a8dbdb363409bbc2d3341718b00e17c9c/addons/kaykit_furniture_bits/Assets/gltf/table_medium.gltf
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `furniture/tables`
- Intended style: stylized
- Import: `model/table_medium.gltf`
- Triangles: 168; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized atlas rather than realistic PBR maps.
- Static model; no collision mesh supplied.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

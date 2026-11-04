# Carved gothic wooden cabinet

- Creator: Kirill Sannikov
- Source: https://polyhaven.com/a/GothicCabinet_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `furniture/storage`
- Intended style: realistic
- Import: `model/GothicCabinet_01_2k.gltf`
- Triangles: 12,170; mesh objects: 5
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Back panel uses a deliberately plain plywood texture, so do not place it facing camera.
- Doors are modelled ajar; closing them means rotating the door objects.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Modern ceiling fan with light

- Creator: Ulan Cabanilla
- Source: https://polyhaven.com/a/ceiling_fan
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `electronics/appliances`
- Intended style: realistic
- Import: `model/ceiling_fan_2k.gltf`
- Triangles: 16,356; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 5

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Blades are not rigged to spin; animate the blade parent object yourself.
- Light diffuser is opaque in the inspection render and emits nothing.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

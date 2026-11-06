# Street Lamp 01

- Creator: Josh Dean
- Source: https://polyhaven.com/a/street_lamp_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `lighting/street`
- Intended style: realistic
- Import: `model/street_lamp_01_1k.gltf`
- Triangles: 30,610; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The lantern appears dark in the inspection render; emissive appearance varies by target renderer.
- The distributed texture maps are 1K; close-up detail may be softer than the higher-resolution source.
- glTF validator reports 3 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

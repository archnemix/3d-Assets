# Vintage spacecraft instrument panel

- Creator: Michał Wiśniewski
- Source: https://polyhaven.com/a/vintage_spacecraft_instrument
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `tools/measuring`
- Intended style: realistic
- Import: `model/vintage_spacecraft_instrument_2k.gltf`
- Triangles: 13,279; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- CRT face is flat grey with no displayed image; add your own emissive texture.
- Rear stencils are Cyrillic service notes, which may not suit every setting.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

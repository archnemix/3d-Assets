# Antique brass hurricane lantern

- Creator: Rajil Jose Macatangay
- Source: https://polyhaven.com/a/Lantern_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `lighting/lamps`
- Intended style: realistic
- Import: `model/Lantern_01_2k.gltf`
- Triangles: 33,902; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Glass globe is dark and non-transmissive in the inspection render; enable transmission in your engine.
- No flame or light source is included.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

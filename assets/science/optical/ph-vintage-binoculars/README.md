# Vintage brass binoculars

- Creator: Luke
- Source: https://polyhaven.com/a/vintage_binocular
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `science/optical`
- Intended style: realistic
- Import: `model/vintage_binocular_2k.gltf`
- Triangles: 19,362; mesh objects: 8
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Lenses are dark and non-transmissive in the inspection render.
- Faint stamped markings on the barrel are illegible at 2k and carry no readable brand.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

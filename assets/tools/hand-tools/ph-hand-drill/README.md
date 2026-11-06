# Vintage crank hand drill

- Creator: Yann Kervran, Benjamin McDonnell
- Source: https://polyhaven.com/a/vintage_hand_drill
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `tools/hand-tools`
- Intended style: realistic
- Import: `model/vintage_hand_drill_2k.gltf`
- Triangles: 8,338; mesh objects: 5
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Not rigged in the shipped glTF: the crank and chuck do not rotate.
- The drill bit is fused to the chuck rather than interchangeable.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

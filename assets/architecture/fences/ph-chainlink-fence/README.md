# Modular chainlink fence

- Creator: James Ray Cock, Amal Kumar
- Source: https://polyhaven.com/a/modular_chainlink_fence
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `architecture/fences`
- Intended style: realistic
- Import: `model/modular_chainlink_fence_1k.gltf`
- Triangles: 89,232; mesh objects: 20
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Unrigged static prop; no animation clips.
- May have small surface markings from real-world scanning (e.g. stamps, numbers); none flagged as trademarked.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

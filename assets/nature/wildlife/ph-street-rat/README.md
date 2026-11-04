# Realistic street rat

- Creator: Sean Buckley
- Source: https://polyhaven.com/a/street_rat
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `nature/wildlife`
- Intended style: realistic
- Import: `model/street_rat_2k.gltf`
- Triangles: 57,216; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Not rigged: the rat is a static pose and cannot be animated without adding a skeleton.
- Fur is texture and normal-map detail, not strand geometry.
- Whiskers are not modelled as separate geometry.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

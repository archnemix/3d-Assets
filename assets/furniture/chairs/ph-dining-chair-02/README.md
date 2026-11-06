# Dining Chair 02

- Creator: James Ray Cock
- Source: https://polyhaven.com/a/dining_chair_02
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `furniture/chairs`
- Intended style: realistic
- Import: `model/dining_chair_02_2k.gltf`
- Triangles: 22,013; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Static chair; no deformation or seating interaction is supplied.
- The shipped diffuse, normal and material maps are 2K (2048 × 2048); higher-resolution upstream maps are not included.
- glTF validator reports 1 warning(s); inspect the included validator report for renderer compatibility.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

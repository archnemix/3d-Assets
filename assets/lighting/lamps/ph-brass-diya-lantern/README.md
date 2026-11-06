# Hanging brass diya lantern

- Creator: Bhargav Kubal
- Source: https://polyhaven.com/a/brass_diya_lantern
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `lighting/lamps`
- Intended style: realistic
- Import: `model/brass_diya_lantern_2k.gltf`
- Triangles: 12,742; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Glass panels are flat black in the inspection render and need transmission plus an interior light.
- Long suspension chain makes the lantern small in whole-object framing.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

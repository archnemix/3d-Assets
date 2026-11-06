# Car ferry

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/ferry/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/watercraft`
- Intended style: stylized
- Import: `model/ferry.glb`
- Triangles: 26,106; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized procedural model with simplified forms and materials; not photorealistic.
- Source GLB contains no animation clips; operation of wheels, doors, controls or other moving parts was not verified.
- Khronos validation reports zero errors and 1 runtime-generated tangent-space warning(s); normal-map shading may vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

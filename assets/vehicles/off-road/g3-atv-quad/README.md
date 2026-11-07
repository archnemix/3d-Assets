# Four-wheeled ATV

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/atv-quad/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/off-road`
- Intended style: stylized
- Import: `model/atv-quad.glb`
- Triangles: 18,120; mesh objects: 6
- Rig: False; animation clips: 0
- Texture images: 5

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized model with simplified forms and materials; not photorealistic.
- The shipped GLB has no animation clips; operation of moving parts was not verified.
- Khronos validation reports zero errors and 5 runtime-generated tangent-space warning(s); normal-map shading may vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

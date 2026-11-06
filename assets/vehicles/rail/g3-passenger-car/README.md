# Passenger railway coach

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/passenger-car/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/rail`
- Intended style: stylized
- Import: `model/passenger-car.glb`
- Triangles: 27,308; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized model with simplified forms and materials; not photorealistic.
- The shipped GLB has no animation clips; operation of moving parts was not verified.
- Khronos validation reports zero errors and 1 runtime-generated tangent-space warning(s); normal-map shading may vary by renderer.
- Blender inspection counted 80 zero-area triangles; these may need cleanup for topology-sensitive workflows.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

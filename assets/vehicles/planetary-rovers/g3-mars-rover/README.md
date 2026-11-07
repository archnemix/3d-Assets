# Mars exploration rover

- Creator: Grab3D
- Source: https://grab3d.com/models/sci-fi/mars-rover/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/planetary-rovers`
- Intended style: stylized
- Import: `model/mars-rover.glb`
- Triangles: 24,008; mesh objects: 8
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
- Blender inspection counted 16 zero-area triangles; these may need cleanup for topology-sensitive workflows.
- Stylized exploration design, not a verified replica of a specific rover.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

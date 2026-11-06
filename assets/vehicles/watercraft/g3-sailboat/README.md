# Cruising sailboat

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/sailboat/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/watercraft`
- Intended style: stylized
- Import: `model/sailboat.glb`
- Triangles: 19,799; mesh objects: 5
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized procedural model, not photorealistic; surfaces and dimensions are simplified.
- Static source GLB has no animation clips; functional operation and movable parts have not been verified.
- Khronos validator: zero errors, 1 warning(s) for runtime-generated tangent space; normal-map shading may differ between engines.
- Automatically authored experimental animation was not reviewed and its generated GLB is excluded; preview frames and report remain as intake evidence.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Turbofan jet engine cutaway

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/jet-engine/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/parts`
- Intended style: stylized
- Import: `model/jet-engine.glb`
- Triangles: 39,382; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylised Cozy-kit palette rather than photoreal materials.
- The nacelle is deliberately cut away; this is not a complete closed engine.
- Stage counts are illustrative, not a specific engine model.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

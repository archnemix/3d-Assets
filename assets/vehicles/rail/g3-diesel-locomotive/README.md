# Centre-cab diesel locomotive

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/diesel-locomotive/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/rail`
- Intended style: stylized
- Import: `model/diesel-locomotive.glb`
- Triangles: 34,616; mesh objects: 4
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylised Cozy-kit palette rather than photoreal materials.
- Wheels and bogies are part of the single body mesh, so unlike the Grab3D road vehicles this cannot be given a wheel-roll clip without separating the mesh.
- Cab interior is not modelled; the window glass is a separate opaque-ish lens node.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

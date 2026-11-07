# 1990s police patrol car

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/1990s-police-car/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/cars/emergency`
- Intended style: stylized
- Import: `model/1990s-police-car.glb`
- Triangles: 19,930; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 5

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized, not photoreal: this is a Cozy-kit vehicle with a simplified pastel palette.
- Wheels are separate objects pivoted on their hubs, so they can be rolled; the body itself is not rigged.
- Interior is simplified; not suitable for a close-up cabin shot.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

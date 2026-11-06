# Double-deck car transporter

- Creator: Grab3D
- Source: https://grab3d.com/models/vehicles/car-transporter/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/trucks`
- Intended style: stylized
- Import: `model/car-transporter.glb`
- Triangles: 29,970; mesh objects: 11
- Rig: False; animation clips: 0
- Texture images: 8

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized, not photoreal: this is a Cozy-kit vehicle with a simplified pastel palette.
- The two cargo cars are static and cannot be driven off the deck.
- The loading ramps are fixed in the raised position.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

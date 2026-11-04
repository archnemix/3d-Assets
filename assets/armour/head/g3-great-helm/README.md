# Great helm with breathing rosettes

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/great-helm/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `armour/head`
- Intended style: stylized
- Import: `model/great-helm.glb`
- Triangles: 14,012; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- No interior padding or arming cap is modelled.
- Sized as a standalone prop; it may need scaling to fit a specific character head.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Winter king in ermine cape

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/king/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/humans`
- Intended style: realistic
- Import: `model/king-rigged.glb`
- Triangles: 300,000; mesh objects: 1
- Rig: True; animation clips: 2
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted origin (Meshy) is disclosed upstream; some storefronts require AI-content disclosure.
- The cape is skinned to the shoulders, not cloth-simulated, so it will not swing freely.
- The crown cannot be removed without editing the mesh.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

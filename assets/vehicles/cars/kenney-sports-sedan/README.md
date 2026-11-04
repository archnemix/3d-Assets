# Kenney sports sedan

- Creator: Kenney
- Source: https://github.com/Hidencod/tge-assets/blob/d92c6e923bbef8649d4e5be3ab375a40f88672b0/packs/car-kit/sedan-sports.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/cars`
- Intended style: low-poly
- Import: `model/sedan-sports.glb`
- Triangles: 2,088; mesh objects: 6
- Rig: False; animation clips: 0
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Thirteen zero-area triangles retained from upstream.
- Flat-color atlas rather than PBR maps.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

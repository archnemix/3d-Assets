# Dutch merchant sailing ship

- Creator: James Ray Cock, Rico Cilliers, Nicolò Zubbini
- Source: https://polyhaven.com/a/dutch_ship_medium
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/watercraft`
- Intended style: realistic
- Import: `model/dutch_ship_medium_1k.gltf`
- Triangles: 69,162; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 9

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Very large real-world scale; check scene units before placing next to characters.
- Sails are static geometry in a fixed partially-furled state, not simulated cloth.
- Not rigged in the shipped glTF; masts and yards do not articulate.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

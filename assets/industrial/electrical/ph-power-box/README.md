# Industrial electrical power box

- Creator: Rico Cilliers, Yann Kervran
- Source: https://polyhaven.com/a/power_box_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `industrial/electrical`
- Intended style: realistic
- Import: `model/power_box_01_2k.gltf`
- Triangles: 21,272; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Invented POWERHAVEN brand mark is baked into the texture; remove or overpaint it for brand-sensitive use.
- Not rigged in the shipped glTF; the door cannot be opened or closed at runtime.
- Breaker toggles are static geometry.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

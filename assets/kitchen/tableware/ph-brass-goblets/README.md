# Ornate brass goblets

- Creator: Tina
- Source: https://polyhaven.com/a/brass_goblets
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `kitchen/tableware`
- Intended style: realistic
- Import: `model/brass_goblets_1k.gltf`
- Triangles: 9,600; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 9

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Three goblets are supplied as one scene laid out side by side; separate them before use.
- Polished brass is highly reflective and will need an environment map to look right.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

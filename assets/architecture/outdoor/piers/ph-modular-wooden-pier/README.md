# Modular Wooden Pier

- Creator: Rico Cilliers
- Source: https://polyhaven.com/a/modular_wooden_pier
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `architecture/outdoor/piers`
- Intended style: realistic
- Import: `model/modular_wooden_pier_1k.gltf`
- Triangles: 84,780; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- This is a modular parts scene with loose pieces, not a single finished watertight pier. Assembly, collisions and navigation have not been tested.
- The distributed texture maps are 1K; higher-resolution upstream files are not included.
- glTF validator reports 12 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

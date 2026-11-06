# Colonial sailing pinnace

- Creator: James Ray Cock, Rico Cilliers, Nicolò Zubbini, Yann Kervran
- Source: https://polyhaven.com/a/ship_pinnace
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/watercraft`
- Intended style: realistic
- Import: `model/ship_pinnace_1k.gltf`
- Triangles: 168,317; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 21

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Uses 1K texture maps, not the upstream 4K version.
- Static shipped glTF contains no animation clips or armature even though upstream may offer a separately rigged format.
- The furnished interior and enterability have not been verified.
- Khronos validator reports seven warnings; see the packaged report.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

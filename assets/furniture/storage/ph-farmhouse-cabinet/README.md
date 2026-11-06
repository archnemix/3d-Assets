# Small painted farmhouse cabinet

- Creator: Kirill Sannikov
- Source: https://polyhaven.com/a/painted_wooden_cabinet_02
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `furniture/storage`
- Intended style: realistic
- Import: `model/painted_wooden_cabinet_02_2k.gltf`
- Triangles: 966; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Very low triangle count (966); edges will look faceted in extreme close-up.
- The back is unfinished bare board, as on real wall-standing furniture; do not place it free-standing in a room.
- Not rigged: the drawer and cupboard door do not open.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

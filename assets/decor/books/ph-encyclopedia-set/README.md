# Leather-bound encyclopedia set

- Creator: John Malcolm
- Source: https://polyhaven.com/a/book_encyclopedia_set_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `decor/books`
- Intended style: realistic
- Import: `model/book_encyclopedia_set_01_2k.gltf`
- Triangles: 67,306; mesh objects: 20
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- 67k triangles and 40 non-blocking glTF warnings; check the validator log if your pipeline is strict.
- Spine text reads ENCYCLOPEDIA with volume letters, a generic title rather than a real publication.
- Books are a fixed row; individual volumes must be separated to shelve them differently.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

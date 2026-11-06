# Chess Set

- Creator: Riley Queen
- Source: https://polyhaven.com/a/chess_set
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `toys/games`
- Intended style: realistic
- Import: `model/chess_set_1k.gltf`
- Triangles: 76,920; mesh objects: 33
- Rig: False; animation clips: 0
- Texture images: 9

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The distributed texture maps are 1K; higher-resolution upstream files are not included.
- glTF validator reports 37 generated-tangent-space warning(s); normal-map shading can vary by renderer.
- The pieces are positioned as a static scene; no chess rules, interactions or animations are supplied.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

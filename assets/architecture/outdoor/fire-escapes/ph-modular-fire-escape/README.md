# Modular Fire Escape

- Creator: Juniix
- Source: https://polyhaven.com/a/modular_fire_escape
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `architecture/outdoor/fire-escapes`
- Intended style: realistic
- Import: `model/modular_fire_escape_1k.gltf`
- Triangles: 11,322; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 6

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Parts are displayed separately rather than as an assembled escape. Fit, attachment, collisions and navigation have not been tested.
- The distributed texture maps are 1K; higher-resolution upstream files are not included.
- glTF validator reports 7 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

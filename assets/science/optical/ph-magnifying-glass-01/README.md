# Magnifying Glass 01

- Creator: Nazar Borodavka
- Source: https://polyhaven.com/a/magnifying_glass_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `science/optical`
- Intended style: realistic
- Import: `model/magnifying_glass_01_1k.gltf`
- Triangles: 7,240; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 5

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The glass appeared grey in these renders; actual transparency and magnification depend on the target renderer.
- The distributed texture maps are 1K; close-up detail may be softer than the higher-resolution source.
- glTF validator reports 2 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

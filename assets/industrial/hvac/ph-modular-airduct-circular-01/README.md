# Modular Airduct Circular 01

- Creator: Riley Queen
- Source: https://polyhaven.com/a/modular_airduct_circular_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `industrial/hvac`
- Intended style: realistic
- Import: `model/modular_airduct_circular_01_1k.gltf`
- Triangles: 14,280; mesh objects: 16
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Modular parts are laid out separately; assembly, snap alignment and collisions have not been tested.
- The distributed texture maps are 1K; close-up detail may be softer than the higher-resolution source.
- glTF validator reports 16 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

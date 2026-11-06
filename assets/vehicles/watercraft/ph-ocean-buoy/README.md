# Ocean Buoy

- Creator: Mateusz Sadek
- Source: https://polyhaven.com/a/ocean_buoy
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/watercraft`
- Intended style: realistic
- Import: `model/ocean_buoy_2k.gltf`
- Triangles: 12,240; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The selected package uses the downloaded texture resolution; higher-resolution upstream files are not included.
- glTF validator reports 1 generated-tangent-space warning(s); normal-map shading can vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

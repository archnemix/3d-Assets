# Retro analog multimeter

- Creator: elli moeller
- Source: https://polyhaven.com/a/retro_multimeter
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `tools/measuring`
- Intended style: realistic
- Import: `model/retro_multimeter_2k.gltf`
- Triangles: 8,948; mesh objects: 7
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The analogue needle sits behind a dark tinted window and is hard to read at gallery scale.
- Leads are in a fixed coiled pose.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

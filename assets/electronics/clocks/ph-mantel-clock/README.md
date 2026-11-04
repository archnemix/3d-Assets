# Ornate wooden mantel clock

- Creator: Yann Kervran, Rico Cilliers
- Source: https://polyhaven.com/a/mantel_clock_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `electronics/clocks`
- Intended style: realistic
- Import: `model/mantel_clock_01_2k.gltf`
- Triangles: 25,721; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Not rigged in the shipped glTF; the hands cannot be driven without re-parenting them.
- The dial is a texture, so the displayed time cannot be changed without editing the texture.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

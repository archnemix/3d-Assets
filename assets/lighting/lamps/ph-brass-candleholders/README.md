# Ornate brass candleholders

- Creator: Tina
- Source: https://polyhaven.com/a/brass_candleholders
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `lighting/lamps`
- Intended style: realistic
- Import: `model/brass_candleholders_1k.gltf`
- Triangles: 41,936; mesh objects: 3
- Rig: False; animation clips: 0
- Texture images: 14

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Textures are 1K, not 2K: fourteen maps exceeded the per-package storage budget and the picker logged the fallback.
- Three holders ship as one laid-out scene; separate them to place individually.
- Candles are unlit with no flame geometry.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Eighties portable boombox

- Creator: Thomas Paul Mouilleron
- Source: https://polyhaven.com/a/boombox
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `electronics/audio`
- Intended style: realistic
- Import: `model/boombox_2k.gltf`
- Triangles: 10,168; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 5

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Decorative stickers show original chibi-style cartoon artwork with no wordmark or logo; replace the decal map if your storefront requires cleared artwork.
- Front panel carries a generic tuner scale, not a manufacturer name.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

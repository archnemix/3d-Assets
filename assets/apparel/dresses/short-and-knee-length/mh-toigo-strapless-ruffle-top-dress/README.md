# Strapless ruffle-top dress

- Creator: MargaretToigo
- Source: https://static.makehumancommunity.org/assets/assetpacks/dress01.html
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `apparel/dresses/short-and-knee-length`
- Intended style: realistic
- Import: `model/garment.glb`
- Triangles: 10,336; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Static standalone garment conversion; no rig, skin weights or automatic fitting are provided, and compatibility with any body shape has not been verified.
- Diffuse and any declared normal maps are embedded; legacy specular, bump, AO and other shader parameters are not reproduced.
- Textured game-asset geometry, not photorealistic; some surfaces show visible faceting.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

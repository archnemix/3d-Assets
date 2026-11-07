# Round Spectacles

- Creator: Sean Buckley
- Source: https://polyhaven.com/a/round_spectacles
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `apparel/accessories/eyewear`
- Intended style: realistic
- Import: `model/round_spectacles_1k.gltf`
- Triangles: 11,810; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The distributed texture maps are 1K; close-up detail may be softer than the higher-resolution source.
- glTF validator reports 2 generated-tangent-space warning(s); normal-map shading can vary by renderer.
- The lenses appear dark and opaque in these renders; transparency may vary by renderer.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

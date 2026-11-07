# Western cowboy hat

- Creator: Grab3D
- Source: https://grab3d.com/models/props/cowboy-hat/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `apparel/headwear/hats`
- Intended style: stylized
- Import: `model/cowboy-hat.glb`
- Triangles: 7,744; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Static prop: no rig or animation; fitting or use as wearable clothing on a character has not been verified.
- Stylized pastel model, not photorealistic.
- Khronos validation reports zero errors and 1 runtime-generated tangent-space warning(s); normal-map shading may vary by renderer.
- Blender inspection counted 44 zero-area triangles; topology-sensitive workflows may require cleanup.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

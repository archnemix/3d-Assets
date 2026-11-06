# Stylized Bat

- Creator: Gobkit / Alsomind Tech Co., Ltd.
- Source: https://github.com/Ariescar/gobkit-free-assets/blob/4e73c68fa6e8ca9d948fcc0ce7215c830a022c3b/animal/Bat.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `nature/wildlife/stylized`
- Intended style: low-poly
- Import: `model/Bat.glb`
- Triangles: 376; mesh objects: 1
- Rig: True; animation clips: 1
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- One continuous baked track, not separate named clips. Sampled wing poses were inspected but seamless loops and individual actions were not verified.
- glTF validator reports three warnings concerning skinned-node transforms and image features; verify behavior in the target engine.
- Simple low-poly cartoon style; this is not a realistic animal.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

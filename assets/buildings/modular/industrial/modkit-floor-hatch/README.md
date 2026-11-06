# Industrial floor hatch

- Creator: Jaron Bragg
- Source: https://github.com/JaronKBragg7337/asset-pack-ue-threejs-blender-unity/blob/f5a53eaadbb46fac8e29faabb6c0ac1b6c6d2311/exports/GLTF/SM_Floor_Hatch.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `buildings/modular/industrial`
- Intended style: stylized
- Import: `model/SM_Floor_Hatch.glb`
- Triangles: 1,004; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 0

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- This is an untextured static hatch panel. No opening motion was authored; separability and collision must not be assumed.
- Designed as part of a simplified industrial kit, not photorealistic PBR.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

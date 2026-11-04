# KayKit mage

- Creator: Kay Lousberg
- Source: https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0/blob/672074b73ba276876a19e8816ecdc5241817ab47/addons/kaykit_character_pack_adventures/Characters/gltf/Mage.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/humans`
- Intended style: stylized
- Import: `model/Mage.glb`
- Triangles: 5,683; mesh objects: 12
- Rig: True; animation clips: 76
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Skinned-mesh non-root and buffer-view-target warnings are non-visual.
- Rest-pose inspection only; animation import must be tested in the target engine.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

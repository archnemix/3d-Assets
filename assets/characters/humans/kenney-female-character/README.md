# Kenney mini female character

- Creator: Kenney
- Source: https://github.com/Hidencod/tge-assets/blob/d92c6e923bbef8649d4e5be3ab375a40f88672b0/packs/mini-characters/character-female-a.glb
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/humans`
- Intended style: low-poly
- Import: `model/character-female-a.glb`
- Triangles: 876; mesh objects: 2
- Rig: True; animation clips: 32
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- 512px flat-color atlas rather than PBR maps; intentionally low-poly.
- Unused-object/tangent and skinned-mesh warnings are non-visual validator notes.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

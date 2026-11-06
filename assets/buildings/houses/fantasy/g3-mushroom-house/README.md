# Fantasy mushroom house

- Creator: Grab3D
- Source: https://grab3d.com/models/buildings/fantasy-mushroom-house/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `buildings/houses/fantasy`
- Intended style: stylized
- Import: `model/fantasy-mushroom-house.glb`
- Triangles: 27,798; mesh objects: 4
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Human-modeled upstream (origin.ai_content: false), not AI-generated.
- Stylized style rather than photoreal — textured but not 8K PBR.
- Single fused mesh; cannot be disassembled or animated without separation.
- Unrigged: no skeleton or animation clips.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

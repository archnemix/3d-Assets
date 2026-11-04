# Firefighter in turnout gear

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/firefighter/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/occupations`
- Intended style: realistic
- Import: `model/firefighter-rigged.glb`
- Triangles: 259,527; mesh objects: 1
- Rig: True; animation clips: 2
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted origin is disclosed upstream (origin.ai_content); some storefronts require an AI-content disclosure when you resell.
- The visor is modelled in the raised position only and is not a separate hinged part.
- The air cylinder cannot be removed.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Police officer in uniform and vest

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/police-officer/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/occupations`
- Intended style: realistic
- Import: `model/police-officer-rigged.glb`
- Triangles: 267,417; mesh objects: 1
- Rig: True; animation clips: 2
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted origin is disclosed upstream (origin.ai_content); some storefronts require an AI-content disclosure when you resell.
- Generic uniform with no insignia; it does not depict any specific real police force.
- The vest and holster are fused to the body; the sidearm cannot be drawn.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

# Toddler in knitted romper

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/baby-character/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/humans`
- Intended style: stylized
- Import: `model/baby-character-rigged.glb`
- Triangles: 299,999; mesh objects: 1
- Rig: True; animation clips: 2
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted origin (Meshy) is disclosed upstream; some storefronts require AI-content disclosure.
- A 24-bone adult-proportioned auto-rig on a toddler body; expect to adjust the walk clip for the shorter legs.
- Hair is geometry, not simulated.
- The static inspection views were rechecked on 2026-11-06: the proportions and/or costume presentation are stylized rather than photorealistic.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

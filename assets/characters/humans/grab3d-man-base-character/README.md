# Realistic adult male base character, rigged

- Creator: Grab3D
- Source: https://grab3d.com/models/characters/man-base-character/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `characters/humans`
- Intended style: realistic
- Import: `model/man-base-character-rigged.glb`
- Triangles: 262,348; mesh objects: 1
- Rig: True; animation clips: 2
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted upstream origin is disclosed in provenance and tags.
- Rigged package uses 2K textures rather than the static package's 4K maps.
- Generated tangent-space and skinned-mesh-non-root warnings are informational.
- No collision mesh or LODs supplied.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

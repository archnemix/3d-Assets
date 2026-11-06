# Vintage 8mm film projector

- Creator: PeterM
- Source: https://polyhaven.com/a/filmstrip_projector_8mm
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `electronics/av`
- Intended style: realistic
- Import: `model/filmstrip_projector_8mm_2k.gltf`
- Triangles: 32,697; mesh objects: 16
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Invented SIRIUS steerling badge is baked into the texture; remove it for brand-sensitive use.
- Not rigged: the reels do not turn and the film does not advance.
- The mains plug is a specific regional type and may not match your scene's locale.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

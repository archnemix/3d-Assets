# Yellow submersible

- Creator: weirdybeardyman
- Source: https://opengameart.org/content/yellow-submersible
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/underwater`
- Intended style: stylized
- Import: `model/yellow-submersible.glb`
- Triangles: 12,398; mesh objects: 4
- Rig: False; animation clips: 0
- Texture images: 0

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Stylized model with simplified forms and materials; not photorealistic.
- The shipped GLB has no animation clips; operation of moving parts was not verified.
- Blender inspection counted 40 zero-area triangles; these may need cleanup for topology-sensitive workflows.
- Very simple flat-colored materials; the cyan dome is opaque and an interior is not verified.
- The original Blender source is retained for provenance; open third-party files with automatic script execution disabled.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

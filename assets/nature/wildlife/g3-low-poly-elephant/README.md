# Low Poly Elephant

- Creator: Grab3D
- Source: https://grab3d.com/models/animals/low-poly-elephant/
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `nature/wildlife`
- Intended style: low-poly
- Import: `model/low-poly-elephant.glb`
- Triangles: 3,000; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 1

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- AI-assisted origin is disclosed upstream (origin.ai_content); some storefronts require an AI-content disclosure when you resell.
- Deliberately low-detail (~3k triangles, flat-shaded, single texture) for mobile/stylised use; not PBR.
- Unrigged static mesh with baked pose.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

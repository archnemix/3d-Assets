# Old vintage car

- Creator: piopis; scene by Benedikt Bitterli, glTF conversion by Erfan Momeni
- Source: https://blendswap.com/blend/14205
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `vehicles/cars/classic`
- Intended style: realistic
- Import: `model/vintage_car_extended.gltf`
- Triangles: 771,640; mesh objects: 47
- Rig: False; animation clips: 0
- Texture images: 0

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Static glTF: no animation clips or armature; working wheels, doors and controls were not verified.
- Seats and steering wheel are visible through windows but detailed interior, accessibility and functionality were not verified.
- No image textures; the shiny paint, chrome and glass use approximate converted materials. Material appearance depends on support for glTF extensions.
- Blender inspection reports 1,024 zero-area triangles among 771,640 total; zero glTF errors or warnings, 52 informational notices.
- The original separately licensed HDR is excluded. The ground and camera definitions were removed; source buffer retains unused ground data.
- Vintage-car reference orientation is not standard front +Z; rely on the actual geometry rather than the inspection labels.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

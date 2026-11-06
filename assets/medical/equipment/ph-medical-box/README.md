# Medical Box

- Creator: Ulan Cabanilla
- Source: https://polyhaven.com/a/medical_box
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `medical/equipment`
- Intended style: realistic
- Import: `model/medical_box_1k.gltf`
- Triangles: 3,718; mesh objects: 5
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- The distributed texture maps are 1K; close-up detail may be softer than the higher-resolution source.
- glTF validator reports 5 generated-tangent-space warning(s); normal-map shading can vary by renderer.
- The box is empty; no first-aid contents are included. The library-authored opening clip moves the lid but does not animate the latches.
- Three sampled animation frames were inspected; continuous playback and all intermediate frames were not individually checked. Animated GLB validation: 0 errors, 5 warnings.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

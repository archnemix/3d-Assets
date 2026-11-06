# Wall-mounted CCTV camera

- Creator: Alexander Otterbeck, Yann Kervran
- Source: https://polyhaven.com/a/security_camera_01
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `electronics/security`
- Intended style: realistic
- Import: `model/security_camera_01_2k.gltf`
- Triangles: 13,571; mesh objects: 1
- Rig: False; animation clips: 0
- Texture images: 4

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Invented FocusSpy brand mark is baked into the texture; remove it for brand-sensitive use.
- Not rigged in the shipped glTF; the bracket does not pan or tilt at runtime.
- The lens port is an opaque dark disc, not optical glass.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

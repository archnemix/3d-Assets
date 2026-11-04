# Red fire alarm pull station

- Creator: Slinc
- Source: https://polyhaven.com/a/fire_alarm
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `industrial/safety`
- Intended style: realistic
- Import: `model/fire_alarm_2k.gltf`
- Triangles: 2,705; mesh objects: 2
- Rig: False; animation clips: 0
- Texture images: 3

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

- Lower badge reads HOTRESCUE, an invented brand rather than a real manufacturer.
- Pull handle is modelled in the armed position with no rig.

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; sidecar copies are byte-for-byte extracts for inspection and DCC workflows,
not additional dependencies. External glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.

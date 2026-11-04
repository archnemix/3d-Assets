# 3D Assets

A curated library of free, public-domain 3D assets for games, renders and prototypes. The goal is **CC0 only**: commercial use, modification and redistribution without an attribution requirement.

## Current status

The library currently contains **28 approved CC0 assets** saved as real files under `assets/`, organized by category and subject. **Only entries in `manifest.json` are approved.** Files under `quarantine/` are review candidates, not recommendations.

Approved subjects include humans, chairs, sofas, tables, potted plants, fruit, snacks, vehicles, toys, industrial containers and retail props. Realistic MakeHuman human candidates are generated through the same quarantine/review pipeline and are only added after they pass inspection and visual review.

## Find and use an asset

After publication, open `gallery/index.html` through a local web server, or browse `assets/` by category:

```text
assets/
  furniture/
    chairs/
      ph-victorian-armchair/
      kaykit-dining-chair/
      kenney-cushion-chair/
```

Different creators' interpretations share the subject folder. Each individual asset contains its model, textures, inspection images, source evidence, license and `asset.json` metadata. Read that metadata for scale, rig/animation information, texture resolution and review limitations.

Import the file identified by `model` into Blender, Godot or another glTF-compatible tool. Keep its neighboring files and folders together. GLB models are self-contained; extracted images in `textures/` are convenient copies of their embedded maps. glTF models may directly reference neighboring buffers and texture maps.

## Browse locally

```bash
python -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000/` on your own computer. It redirects to the live gallery at `/gallery/`. The gallery reads the approved-only manifest, refreshes automatically, and lets you browse all assets or filter by category, style, search text, and rigging.

## Documentation

- [Technical details](technical.md)
- [Engineering journal](thinking.md)
- [Changelog](CHANGELOG.md)
- [Research and licensing decisions](docs/research.md)

Discovery uses the Poly Haven API: **Powered by Poly Haven**. This is a service credit for the acquisition tool, not an attribution condition on downloaded CC0 assets.

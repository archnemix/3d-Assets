# 3D Assets

A curated library of free, public-domain 3D assets for games, renders and prototypes. The goal is **CC0 only**: commercial use, modification and redistribution without an attribution requirement.

## Current status

The library currently contains **333 approved CC0 assets** in **96 categories**, saved as real files under `assets/` and organized by category and subject. **Only entries in `manifest.json` are approved.** Files under `quarantine/` are review candidates, not recommendations.

Approved subjects span realistic rigged humans, low-poly game characters, chairs, sofas, tables, beds, cabinets and shelving, desks, hand and power tools, measuring instruments, optical and scientific instruments, cookware and tableware, fruit, vegetables and baked goods, vases, books, potted plants, vehicles, toys, computers and audio, appliances, safety equipment, industrial containers, carts and lighting. The realistic-human set currently includes an adult male base character, an adult female base character and an elderly woman, each with embedded PBR textures and walk/run animation clips. MakeHuman/MPFB generation is working through the same quarantine/review pipeline, but generated characters are only added after they pass inspection and visual review.

The gallery defaults to the approximate **realistic** style label; choose **All styles** to browse the whole collection. Style labels do not guarantee photorealism, and older entries still need individual reassessment. Each asset belongs to one exact subcategory. See [`reports/research/2026-11-06-texture-priority-review.md`](reports/research/2026-11-06-texture-priority-review.md) for the latest 2K-texture intake and held candidates.

See [`docs/license-audit-summary.md`](docs/license-audit-summary.md) for historical exclusions and [`reports/research/2026-11-06-permissions-recheck.md`](reports/research/2026-11-06-permissions-recheck.md) for the latest source-level recheck. The recorded-evidence audit is not independent proof of ownership or an exhaustive check of every creator statement.

New to rigged models? [`docs/rigging.md`](docs/rigging.md) explains what a rig is, the difference between character and mechanical rigs, and why a rig advertised upstream is sometimes absent from the glTF we ship.

Browse approved assets by category in [`docs/categories/`](docs/categories/), or open the live gallery in [`gallery/`](gallery/) to search and filter all of them at once. Every asset folder carries its model, textures, twelve inspection renders, provenance, license text and checksums.

## Find and use an asset

After publication, open `gallery/index.html` through a local web server, or browse `assets/` by category:

```text
assets/
  furniture/
    chairs/
      ph-victorian-armchair/
      kenney-cushion-chair/
```

Different creators' interpretations share the subject folder. Each individual asset contains its model, textures, inspection images, source evidence, license and `asset.json` metadata. Read that metadata for scale, rig/animation information, texture resolution and review limitations.

Import the file identified by `model` into Blender, Godot or another glTF-compatible tool. Keep its neighboring files and folders together. GLB models are self-contained; extracted images in `textures/` are convenient copies of their embedded maps. glTF models may directly reference neighboring buffers and texture maps.

## Browse locally

```bash
python -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000/` on your own computer. It redirects to the live gallery at `/gallery/`. The gallery reads the approved-only manifest and lets you search or filter by category,
style, rigging and animation. Open an asset, then select **View in 3D** to rotate,
zoom, pan and play available animation clips. Some assets provide a separately authored
animated version; you can switch files or download it from the details panel. The 3D
viewer needs a modern WebGL-capable browser and an HTTP server (opening the HTML as a
local file will not work). Three.js is bundled locally under its MIT license; it does
not change the licenses of the assets. Renders and downloads remain available if the
viewer cannot load a model.

## Documentation

- [Fantasy buildings starter collection](docs/themes/fantasy-buildings.md)
- [Modular industrial starter collection](docs/themes/industrial-modkit.md)
- [License audit — per asset](docs/licenses.md)
- [Technical details](technical.md)
- [Engineering journal](thinking.md)
- [Changelog](CHANGELOG.md)
- [Research and licensing decisions](docs/research.md)

## What you may do with these assets

**An author's request outranks the license.** KayKit's creator asks that unmodified copies not be
resold or claimed as your own. CC0 would legally permit it, but this library mirrors unmodified
copies publicly, so all six KayKit assets were **retired and deleted** and the source is closed to
future intake. `config/license-terms.json` now encodes that rule, and a test asserts KayKit cannot
reappear. Retirement records live in `reports/retired/`.

Every approved asset is CC0 1.0. Per asset, that means **free**, **no attribution**, **commercial use**, **use and redistribution of the files as-is** (not only embedded in a game), and **public display**. The [license audit](docs/licenses.md) records the verdict, evidence link and license-file checksum for every asset, plus the caveats that CC0 does not remove:

- CC0 waives copyright, not trademark or patent rights, and clears no third-party rights in a depicted subject.
- The three Grab3D humans disclose an AI-assisted origin; some storefronts require an AI content disclosure.
- The Kenney files come from a pinned third-party GLB conversion whose own license also releases the conversions under CC0.

Re-run the audit yourself:

```bash
PYTHONPATH=src python -m asset_library license-audit          # rebuild report + docs/licenses.md
PYTHONPATH=src python -m asset_library license-audit --check   # fail if stale or non-compliant
```

Discovery uses the Poly Haven API: **Powered by Poly Haven**. This is a service credit for the acquisition tool, not an attribution condition on downloaded CC0 assets.

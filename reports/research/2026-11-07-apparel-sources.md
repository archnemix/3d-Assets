# Apparel sourcing research — 2026-11-07

Goal: at least 300 individually approved, distinct apparel assets; include clothing, not only accessories. These are leads, not approved inventory. Exclude recolors, body parts and clothed characters from the apparel count; inspect each garment, license, dependencies, geometry, visual quality, and duplicate status.

## MakeHuman Community packs

The [official pack index](https://static.makehumancommunity.org/assets/assetpacks.html) separates CC0 from CC-BY packs. Examples of explicitly CC0 clothing packs include [Dress 01](https://static.makehumancommunity.org/assets/assetpacks/dress01.html), [Pants 01](https://static.makehumancommunity.org/assets/assetpacks/pants01.html) and [Suits 01](https://static.makehumancommunity.org/assets/assetpacks/suits01.html), with named authors and individual assets in each index. Dress 01 includes a flapper-style dress, kimono, and Mycenaean-inspired tunic among its entries; these descriptions do not establish historical accuracy. The system pack is already pinned and documented in `research/makehuman-system-pack.json`; its garment directories include OBJ geometry, `.mhclo`, `.mhmat` and textures. The current `makehuman` intake adapter builds **whole characters**, not standalone garments, so it cannot simply be counted as apparel.

Potential next step: implement a dedicated pinned pack garment adapter and safe standalone OBJ/material conversion, with archive checksum, per-asset pack index/author/license evidence, complete texture dependencies, and regression tests. The pack index is authoritative about which packs are CC0; do not assume CC-BY packs are CC0. Confirm OBJ coordinates, UVs, material texture paths, render/normal orientation, and whether a standalone proxy needs a body deformation for a coherent silhouette. Keep rigging/fit claims honest, and avoid treating variants or bodypart meshes as new garments. Only publish after standard visual and technical review.

## OpenGameArt

- [Hats / Clothing / Props](https://opengameart.org/content/hats-clothing-props) by Teh_Bucket is marked CC0 and offers separate FBX archives for cargo pants, sweatshirt, hats and boots. The submitter cites CC0-derived textures and openclipart sources, and comments note earlier restricted texture concerns were addressed. Verify each archive's actual textures and source before acceptance; download, pin, and convert with no external references.
- [LowPoly Glasses Pack](https://opengameart.org/content/lowpoly-glasses-pack) by iPoly3D is marked CC0; it has 29 models, but visual/geometry comparison is required to eliminate recolors and near-identical frames. Do not count the archive as 29 approved assets.

## Other leads

- [Cloth library](https://blendswap.com/blend/19332) is marked CC0 and contains various garments. Acquisition, licenses for bundled materials, separation and modern Blender conversion remain unverified.
- Meshy search pages claim CC0 for pre-made gallery models, but search results also show identifiable IP and generative content; direct individual licenses, access, origin and trademark/IP concerns remain unverified. No Meshy assets are approved on this basis.
- [Sketchfab clothing kit](https://sketchfab.com/3d-models/clothing-and-character-kit-10-fbx-cc0-77da31c1350343f9ae2f9ef4cb228b8a) has a CC0 claim in its description but a CC Attribution license field. Do not assume CC0 without resolving the conflict.

## Additional leads and exclusions after standalone garment review

- [OverScore Proxy](https://opengameart.org/content/overscore-proxy-modular-low-poly-female-character-creation-set) lists 50 tops, 30 legwear and 20 full-body outfits, including occupational silhouettes, under CC0. Its author explicitly says the models have **no UVs and are untextured**; do not count these toward the textured clothing goal without substantive, appropriately licensed material work and quality review.
- Two potential lehenga models, [Indian Wedding Lehenga Choli](https://sketchfab.com/3d-models/indian-wedding-lehenga-choli-3385430bad2c465691028474136bd6b7) and [India – Lehenga or Saree](https://sketchfab.com/3d-models/india-lehenga-or-saree-wedding-dress-f3aeec252e2d4f32894ac1454cda4280), are labeled CC Attribution, **not CC0**; they have not been acquired and cannot pass this catalog's CC0 gate as listed. No genuine lehenga has yet been approved.

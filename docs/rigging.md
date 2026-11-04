# What "rigged" means, and when it matters

## The short version

A **rig** is a skeleton inside the model. Each vertex of the mesh is assigned
weights that say how much each bone moves it. Move or rotate a bone and the
surface follows, so the model can be posed and animated instead of being a
static statue.

**Rigged is a good thing** when you want movement, and it costs you nothing when
you don't — a rigged model still renders perfectly well as a still object. That
is why this library now prefers a rigged variant when one exists at comparable
quality.

| | Unrigged (static) | Rigged |
| --- | --- | --- |
| Place it in a scene | Yes | Yes |
| Render a still | Yes | Yes |
| Change its pose | No — edit the mesh | Yes — move bones |
| Play a walk cycle | No | Yes, if clips ship with it |
| Retarget motion capture | No | Yes, if the skeleton is humanoid |
| Drive it from game code | No | Yes |

## Two different kinds of rig

Both are useful, and this library contains both.

**Character (skeletal) rigs** deform a continuous surface. A humanoid rig has a
spine, limbs, hands and sometimes fingers and face. Ours come from Grab3D with 24
humanoid bones; `g3-casual-man` has 54 because 30 finger bones were added, so its
hands can actually close. Walk and run clips are included.

**Mechanical (hard-surface) rigs** don't deform anything — they move rigid parts
around pivots. A vice jaw slides, a clock's hands rotate, a tool chest's drawers
open, a CCTV camera pans on its bracket. These are what make a prop feel usable
rather than ornamental, and they are cheap: no skinning, just parented objects
and constraints.

## What to check before you rely on a rig

1. **Bone count.** 24 humanoid bones is enough for walking and gross posing, not
   for finger articulation or facial expression. Look at `geometry.armatures` in
   `asset.json`.
2. **Clips.** `gltf.animations` lists what actually ships. A rig with zero clips
   is still poseable, but you supply the motion.
3. **Unweighted vertices.** `geometry.unweighted_skinned_vertices` must be `0`.
   Anything above zero means part of the mesh will be left behind when the
   skeleton moves. The pipeline checks this.
4. **Weight sums.** Auto-rigged packages sometimes produce weights that don't sum
   to exactly 1, which makes some engines deform incorrectly. The pipeline
   normalizes these and records the before/after checksums in
   `provenance/grab3d-repair.json`.

## The trap: a rig can be present upstream and missing in your file

This is worth knowing because it silently disappoints people.

Poly Haven author rigs in Blender and publishes several formats. **The glTF
export does not always carry the rig that the `.blend` has.** Two examples from
our own intake, both listed as rigged upstream:

- `bench_vice_01` — the glTF arrives with an 11-bone `rig_bench_vice`. Works.
- `bolt_cutters_01` — the glTF arrives with **no armature at all**. The rig exists
  only in the `.blend`.

This library ships glTF/GLB because it imports cleanly everywhere, so an asset's
`rigged` flag reflects **what is actually in the file we ship**, not what the
source page advertises. If you need a rig that upstream only publishes in
`.blend`, download that format from the source page linked in the asset's
provenance.

## Filtering for rigs

The gallery has a **Rigged only** checkbox. In `manifest.json`, every entry
carries `rigged` (boolean) and `animation_count` (integer), so you can filter
programmatically:

```python
import json
assets = json.load(open("manifest.json"))["assets"]
animated = [a["id"] for a in assets if a["rigged"] and a["animation_count"] > 0]
```

## A note on quality tiers

Grab3D publishes each character in three forms: a full-quality static mesh
(800k triangles, 4K textures), a light static mesh, and a **rigged** mesh
(~240k–300k triangles, 2K textures, walk/run clips). The rigged version is both
the most useful and the smallest, so that is what we take. 300k triangles is
dense enough for close camera work; it is not a decimated game LOD. If you need
a real-time LOD, generate it from this mesh rather than expecting one to ship.

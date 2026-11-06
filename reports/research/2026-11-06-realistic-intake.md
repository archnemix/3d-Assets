# Realistic model intake — 2026-11-06

The starting approved catalog was 286. A 48-candidate Poly Haven intake used five
workers or fewer, acquiring and rendering candidates locally on CI runners. The
run concluded **failure** because the modular factory facade exceeded the 12 MiB
package limit; the other four shards finished successfully, and their outputs are
committed alongside logs. See `reports/intake/realistic-diverse-01/` and
[run 42196504596](https://github.com/archnemix/3d-Assets/actions/runs/42196504596).

After inspecting the local-model contact sheets and relevant technical reports,
**29 models were approved**. The catalog now has **315 approved assets in 94
categories**, with **74 containing upstream clips or separately authored animated
models**. This exceeds the 300 minimum but does not reach the preferred 330, and
it is still not mostly animated. A medical box's library-authored lid clip was
inspected in three frames and independently validated. The remainder of this
batch's approved models are static. None are claimed to be print-ready, fully
interactive, navigable, or physically simulated.

**18 candidates remain quarantined**. Reasons for holding individual candidates
include unclear logos or third-party artwork, dark/opaque display materials,
unfinished or unverified animation, and further inspection needed. Quarantine is
not an assertion that every item is defective; it means they are not approved for
the catalog. In particular, the wheelchair's generated animation spins the entire
chair, the compass lid rotates away from its hinge, and chemistry bottle lids were
incorrectly assigned hinge clips. The cabinet has unreviewed upstream tracks.
Generic animation-matcher issues are documented in the animation-rule review.

The published school desk has three zero-area triangles; no visual effect was
obvious in the renders, and the limitation is recorded with the asset. The pier
and fire escape are modular layouts requiring assembly, with snap fit, collisions
and navigation untested. Many texture packages are 1K, a few 2K; per-asset review
notes state limitations. All 29 approved glTF files had zero validator errors,
though generated-tangent-space warnings remain and can affect renderer shading.

The 315/315 audit result checks recorded licensing evidence and inventory. It is
not a warranty of independent ownership, an exhaustive search of every artist's
statements, or clearance of third-party trademarks, design rights and patents.

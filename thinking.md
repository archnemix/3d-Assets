# Engineering journal

This is a decision and implementation journal: what changed, the observed reason, and the trade-off. It is not a claim that a download is good merely because its website calls it free.

## 2026-11-03 — Establish the library before collecting volume

**Observation.** The checkout contained only a two-line README. There was no existing asset taxonomy, manifest or acquisition tool to preserve.

**Decision.** Use Python for file acquisition and metadata, Blender's Python API for actual import/render checks, the Khronos glTF Validator for format diagnostics, and a small static gallery for browsing. These are ordinary, replaceable tools; no application server or database is needed for a file library.

**Boundary.** Source acquisition, technical inspection, visual approval and catalog generation are separate responsibilities. A successful download is not a quality approval.

## Source and license research

The first search identified Poly Haven, Kenney, KayKit and MakeHuman as candidates. Primary source checks were more useful than aggregator labels:

- Poly Haven explicitly allows redistribution of its CC0 assets. Its live API has separate service terms, including a discovery-service credit and identifiable requests. The tool complies; downloaded assets remain attribution-free.
- KayKit's pinned character and furniture packs include explicit CC0 notices.
- Kenney's original pack pages declare CC0. The selected GitHub convenience mirror also explicitly releases its converted GLBs under CC0. Its exact revision and original creator are recorded rather than presenting the mirror as the author.
- Some search results described models as CC0 even when the actual listing said attribution was required. Those listings are not accepted on the strength of their titles.
- Quaternius has conflicting current-license descriptions, including a custom license with redistribution restrictions. It is deferred until the exact downloaded archive's terms can be verified.
- NASA models are not automatically treated as CC0 merely because they are government-hosted. Their media/endorsement guidelines and individual provenance need separate review.

**Quality definition.** Realistic assets need coherent materials, believable silhouettes and clean texture presentation. Stylized assets are judged against their intended style, not rejected for having few triangles. Every accepted asset still needs complete geometry, working materials and a visual check from all sides.

## Acquisition design

The first request deliberately compares different creators' chairs, sofas, tables, fruit and human characters. Subject folders group alternatives; creator-specific asset folders prevent overwrites and preserve distinct topology, textures and rigs.

The workflow is triggered only by `automation/request.json` on the session branch. A planner creates at most five disjoint shards. Workers commit their own candidate paths and logs directly back to the same branch, with bounded push/rebase retries. No artifact-download API is required. Bot output paths do not retrigger intake.

Raw downloads go to `quarantine/`, never `assets/`. The render pass uses the actual local model and its textures. It does not substitute a vendor's marketing image. Twelve inspection images and machine-readable geometry/format reports accompany each candidate.

**Next gate.** Inspect the rendered contact sheets and full-size views, record explicit decisions, then move only approved candidates into their category folders and rebuild the catalog. Rejections retain their reasons and review evidence without keeping failed model payloads.

## First CI run — preserve the evidence, fix the boundaries

Run 41652664807 acquired and rendered all 16 GitHub-hosted candidates, but none passed the complete intake gate. Ten Poly Haven candidates stopped before download because the license check expected prose in a JavaScript-rendered page. The other 16 produced images and a validator summary but no validator report.

Two fixes followed. The license check now reads an immutable revision of Poly Haven's official API terms, which explicitly distinguish CC0 assets from API service conditions. The validator invocation now matches our small Node wrapper's two-argument contract; obsolete flags from a different CLI were removed. A regression test invokes the real validator and checks the report file, not just mocked success.

The failed candidates remain unapproved. Their payloads will be replaced by a clean rerun; the original run and reports remain available in Git history. This is precisely why CI outputs are committed: the failure was diagnosable without artifact-browser access.

## 2026-11-04 — Framing fix and visual promotion

**Observation.** The first corrected contact sheets were still framed poorly: hidden helpers and non-visible objects inflated bounds, making assets appear tiny or off-center.

**Resolution.** Inspection now computes bounds from visible evaluated mesh vertices, recenters the subject, and applies a consistent margin. The refreshed sheets made actual all-angle review possible.

**Result.** After reviewing the refreshed sheets, 25 foundation candidates were approved and promoted into `assets/`. One candidate, the Kenney “teddy bear,” was rejected because it is flat-backed wall decor rather than a plush toy. The expansion batch then added a rubber duck toy, oak side table and KayKit table, bringing the approved library to 28 assets before the realistic-human retry.

**Trade-off.** Minor upstream zero-area triangles and informational validator warnings were accepted only where the visual result remained clean and the limitation was recorded. The gate still requires zero validator errors and explicit scores.

## MakeHuman realism — tool license is not asset license

**Observation.** The user explicitly wanted realistic human characters, not only stylized game characters. MakeHuman’s official system pack provides CC0 base mesh, clothes and textures, but the GitHub source tree alone does not contain the full asset collection.

**Decision.** Pin the official CC0 system archive by SHA-256 and use MPFB2 as a build tool. Preserve recipe descriptors, pack evidence, build logs and a build report. The exported candidate remains subject to the same quarantine and visual-review gates.

**Failure.** The first CI build failed because MPFB 2.0.18 expects Blender 4.2 extension package naming. Importing it as plain `mpfb` caused `bpy.utils.extension_path_user("mpfb")` to reject the package name.

**Resolution.** Load the pinned MPFB source as `bl_ext.user_default.mpfb`, create the extension user directory, then register it. This keeps the fix inside the build script and avoids modifying the upstream tool.

**Next gate.** Generated humans must render cleanly from all angles, pass the validator, and receive explicit visual approval before they are saved into `assets/characters/humans/`.

**Follow-up.** The first extension-package retry did not fail fast; it remained in the acquisition/render step long enough to be unhelpful. The pipeline was made cancellable, the build script now prints stage progress, and the unnecessary MPFB UI asset-list cache was removed because recipes load explicit CC0 pack paths. The next retry uses those changes rather than silently waiting on a stuck job.

## 2026-11-04 — Realistic humans need a second source, not only a generator

**Observation.** MakeHuman/MPFB is the cleanest CC0 realistic-human path, but the headless Blender integration has required several CI-only fixes. While the latest preference-registration retry runs, the realistic-human requirement should not depend on a single fragile build path.

**Decision.** Add Grab3D as a direct-download source. Its packages expose a manifest, a package-level CC0 dedication and a GLB. The adapter verifies the manifest license and package license before download, checks the advertised byte count, and preserves the AI-origin disclosure. The first candidates are realistic rigged male/female base characters, not cartoon humans. The same batch also adds a new lighting category and a realistic barber chair so the library keeps broadening.

**Trade-off.** Grab3D models are AI-assisted. That is not hidden: candidates are tagged `ai-assisted`, provenance keeps the upstream disclosure, and approval still requires the same all-angle visual gate. MB-Lab was rejected because AGPL-generated characters conflict with the no-strings policy.

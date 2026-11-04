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

**Follow-up.** The expansion-04 logs showed the next Blender API mismatch: `Addons.new()` does not accept the module name as an argument in Blender 4.2. The build now creates an empty addon entry and assigns `addon.module` before registering MPFB. Rather than serializing another human-only retry, expansion-05 runs the two MakeHuman retries alongside two direct Grab3D realistic humans and two new realistic props, keeping the batch within five workers.

**Portability repair.** The first Grab3D rigged humans rendered cleanly but failed the zero-error validator gate: 998 `ACCESSOR_WEIGHTS_NON_NORMALIZED` errors per model, with weight sums drifting by only ~0.00017. Rather than relaxing the gate or hiding the defect, the adapter now normalizes each float weight vector by its sum and records the repair, original checksum and repaired checksum. Local validation of the repaired packages reports zero errors and the same two informational warnings. Appearance is unchanged because relative bone influences are preserved.

**MakeHuman gate.** The Blender 4.2 addon-entry fix worked: both casual adults built, exported, rendered and passed the zero-error validator gate. They were still rejected visually. The male's eyes rendered blank, the female's bob hid the face, and both system-pack shirts carried a prominent MakeHuman logo. A working generator is not the same as an approved character; the next MakeHuman recipes should use generic clothing, readable eyes and face-clear hair. The realistic-human requirement is meanwhile served by the repaired Grab3D batch.

**Realistic humans approved.** The repaired Grab3D batch passed the zero-error gate and the all-angle visual gate. The adult male/female base characters and the elderly woman are now approved realistic rigged humans with walk/run clips. The teenager was rejected because the face/hair are anime-stylized; the user asked specifically for non-cartoonish realistic humans. The library now has 33 approved assets across 12 categories, including a real realistic-human foothold instead of only stylized game characters.

## 2026-11-04 — "Free" is five different questions

**Observation.** Before adding anything else the user asked whether every asset is free, attribution-free, sellable, usable *as-is* rather than only inside a game, and safe for us to display. A `license: CC0-1.0` string in metadata answers none of those on its own; it is a claim we wrote ourselves.

**Decision.** Make the audit a pipeline stage rather than a paragraph. `config/license-terms.json` records what each provider actually grants and where it was read, and a schema refuses to let a provider be described as attribution-bearing, paid or resale-restricted while the library still claims otherwise. `licensing.py` then checks each asset against those terms *and* against its own files: the stored license text really contains a CC0 dedication, its checksum still matches the inventory, every listed texture is present, and no upstream trademark warning flag was recorded. Rendering lives in a separate `license_report.py` so the checks stay readable.

**Finding.** All 33 approved assets pass every check. Provider split: Poly Haven 14, Kenney 10, KayKit characters 4, KayKit furniture 2, Grab3D 3.

**Honest caveats, not marketing.** Three findings would have been easy to omit and are recorded instead. KayKit's itch page says "please don't resell unmodified copies or claim them as your own" — a request sitting beside a CC0 dedication, not a condition of it, and exactly the kind of sentence that matters to the as-is question. `https://kenney.nl/license` now returns 404, so the evidence is the support page plus the license file pinned in the exact source revision, whose git blob hash matches the copy stored in `research/` byte for byte. Poly Haven's CC0 covers assets only: site logos, example renders and page text stay protected, and the API terms ask for a service credit that explicitly does not apply to downloaded assets. That is why this library renders its own previews.

**Consequence.** The terms file is now the single source of truth: `catalog.py` reads it, so `manifest.json` carries `license_notes` and `resale_as_is` and the gallery detail panel shows the caveat beside the download button. A future asset from a provider without recorded terms fails the audit rather than inheriting a blanket CC0 assumption.

## 2026-11-04 — A license is a floor, not a permission slip

**Correction from the user.** The audit had reported KayKit as "Yes" for as-is use, with the creator's anti-resale request recorded as a caveat. The user's response was to remove those assets and respect the author's request. That is the right call and it exposed a flaw in how I had framed the audit: I treated the CC0 dedication as the answer and the author's wishes as a footnote, when for a library whose whole purpose is republishing unmodified copies, the author's wishes are the deciding fact.

**Decision.** KayKit is not a caveat, it is a disqualification. All six assets were retired and their payloads deleted — 18.2 MB. Retirement needed to be a real operation, not `rm -rf`: `retire.py` validates every entry before touching anything, checks the inventory and provider, writes a per-asset record with the reason and the removed model's checksum, and only then deletes. The records in `reports/retired/` mean the library can explain an absence instead of silently forgetting.

**Making it stick.** Both KayKit sources were removed from `config/sources.json` and `config/license-terms.json`. The terms schema now only accepts `status: "verified"` — the `verified-with-request` value I had invented to let KayKit pass no longer exists. The policy carries `author_request_blocks_intake: true`, and a gallery test asserts no `kaykit-` id can appear in the manifest. Two request tests failed immediately when the source was removed, which is exactly what those fixtures are for.

**Trade-off accepted.** The library drops from 33 to 27 assets and loses its stylized-fantasy humans. That is a real cost, and it is the correct one to pay. The expansion that follows has to replace those numbers with sources that carry no such request: Poly Haven, Kenney and Grab3D all explicitly permit redistribution.

**Expansion design.** Rather than deepening existing subjects, the next batch opens 20 new categories — hand and power tools, measuring instruments, cookware, tableware, vegetables, baked goods, vases, books, storage furniture, beds, desks, lanterns, ceiling lighting, computing, optical science, musical instruments, watercraft, safety equipment and office supplies. Two engineering guards came with it: Poly Haven assets carrying an upstream `tmwarn` trademark flag are now refused at intake rather than caught later by the audit, and a budget-aware resolution picker takes the highest resolution that fits a per-package byte budget and logs the fallback. That keeps 30+ new assets from blowing the repository budget while never shipping an incomplete model.

**Storage honesty.** Discarded 27 MB of superseded Grab3D quarantine payloads whose repaired versions are already approved, keeping the failure records and logs. Evidence is worth keeping; a duplicate broken binary is not.

## 2026-11-04 — Thirty new subjects, one trademark rejection

The second expansion batch was the first one large enough to test whether the
pipeline scales past a handful of hero props. Thirty candidates went in, spread
across fourteen categories that did not exist a day ago, and thirty came back
technically clean: zero glTF errors, full 2K texture sets, every package inside
the storage budget. That part is now boring, which is the point.

The interesting failure was `binder_notebook`. It is a genuinely lovely asset —
worn leather, modelled pen loop, open and closed variants, clean topology. On the
contact sheet it looks like an obvious approval. It was only in the full-size top
view that the embossed circular manufacturer's emblem on the cover became
legible. CC0 §4a is explicit that trademark rights are not waived, so shipping
that emblem in a library we tell people they can resell as-is would be
overpromising. I rejected it and wrote the reason into the record.

This is the second time the same lesson has shown up from a different direction.
With KayKit the copyright grant was fine but the author's request was not; here
the copyright grant is fine but a *third party's* mark is the problem. Both cases
say the same thing: `license: CC0` is one input to the decision, not the decision.
The twelve-view render exists precisely so that a human — or an agent acting like
a careful one — actually looks at the object before it enters the catalog.

Two smaller notes worth keeping. First, the resolution picker earned its place:
several of these scans would have been 30–40 MB at 4K, and the budget-aware
fallback kept the whole batch near 160 MB while staying at 2K throughout. Second,
I fixed the duplicated-bullet bug in the category pages rather than leaving it as
a known cosmetic wart. Small generated-output defects are the kind of thing that
quietly trains readers to distrust the rest of the documentation.

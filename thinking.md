# Engineering journal

This is a decision and implementation journal: what changed, the observed reason, and the trade-off. It is not a claim that a download is good merely because its website calls it free.

## 2026-11-03 — Establish the library before collecting volume

**Observation.** The checkout contained only a two-line README. There was no existing asset taxonomy, manifest or acquisition tool to preserve.

**Decision.** Use Python for file acquisition and metadata, Blender's Python API for actual import/render checks, the Khronos glTF Validator for format diagnostics, and a small static gallery for browsing. These are ordinary, replaceable tools; no application server or database is needed for a file library.

**Boundary.** Source acquisition, technical inspection, visual approval and catalog generation are separate responsibilities. A successful download is not a quality approval.

## Source and license research

The first search identified Poly Haven, Kenney, KayKit and MakeHuman as candidates. Primary source checks were more useful than aggregator labels:

- Poly Haven explicitly allows redistribution of its CC0 assets. Its live API has separate service terms, including a discovery-service credit and identifiable requests. The tool complplies; downloaded assets remain attribution-free.
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

# Realistic-texture priority intake — 2026-11-06

The user requested a stronger emphasis on realistic materials, visual inspection of an image for every new asset, and one subcategory per asset. The `realistic-textures-01` intake requested 25 Poly Haven models at 2K. The five-worker Actions run 42200624078 completed successfully; logs and candidate evidence are committed. Poly Haven's CC0 terms and resale position were reviewed in `2026-11-06-permissions-recheck.md`. This is a review of recorded evidence, not a guarantee of third-party rights or independent authorship.

## Approvals

The 18 decisions in `reviews/realistic-textures-01-{first,second}.json` each record a hash of the individually inspected twelve-view contact sheet, per-asset observations and limitations. Every approved model has 2048 × 2048 texture maps, no glTF validator errors, and no embedded or separately authored animation. All have generated-tangent-space validator warnings (one per affected primitive); appearance may vary between renderers. The set includes a textured concrete barrier, worn hammer and spade, shell, bread and cake, pears, wooden spoon and bowl, chairs, sofa, table, wrench, metal jug, manhole cover, watering can, and potted plant. 2K describes the shipped map dimensions, not a guarantee of photorealism or high texel density everywhere.

## Held in quarantine

- `ph-wooden-picnic-table`: although 2K was requested, the size budget caused a 1K fallback. The contact sheet was inspected, but it is not accepted for this texture-priority batch without a better-resolution package.
- `ph-dead-tree-trunk` and `ph-tree-stump-01`: visually detailed scan-like top and sides, but the very dark/flattened undersides raise completeness concerns for a freely viewable standalone object. These could be reconsidered as ground-only set dressing with explicitly agreed limitations.
- `ph-hatchet`: the 2K diffuse texture contains a small registered-looking `UC` mark; provenance does not independently clear it.
- `ph-pliers`: the diffuse texture contains VDE/GS-looking certification markings. CC0 does not itself clear marks.
- `ph-industrial-wall-sconce`: the back has a small designer/manufacturer-style inscription; its independent clearance was not established.
- `ph-metal-jerrycan-green`: the can has a round `PH`-like mark on its front; provenance does not independently clear the mark for all uses.

These seven are not in the approved catalog. Holding a marked candidate is precautionary and is not a finding that its creator violated rights. Source metadata did not flag a trademark for this batch, but visual review catches concerns a metadata flag can miss.

## Existing catalog and subcategories

The previous catalog had 202 `realistic`, 87 `stylized`, and 26 `low-poly` metadata labels. Those are historical classifications, not an independent photorealism audit. Twelve previously approved Grab3D animal contact sheets and six character sheets were sampled; the latter six (knight, dwarf, troll, toddler, child and desert queen) are visibly stylized and were relabeled accordingly, without removing their files. No claim is made that all other prior labels are now correct. The gallery defaults to its approximate realistic style label and offers All styles; the remaining older content needs an individual reassessment.

Every approved item has one category field and a canonical path; the catalog build now rejects duplicate IDs and provider/source IDs, unregistered categories and category/path mismatches. A one-time check also found no byte-identical primary model files among the previous 315 assets; semantic duplicate detection across different source files is not guaranteed. Gallery filters and counts now use exact category paths, so a parent and its child are distinct filters instead of duplicating the child in both. Counts summarize the whole catalog, not the current style/search filters.

After the intake: 333 approved assets in 96 populated categories; 74 have embedded clips or a separate authored animated model, so the long-term mostly-animated goal remains unmet. 214 assets carry the approximate realistic label, 93 stylized and 26 low-poly. The full existing catalog has not been re-reviewed for photorealism or animation quality.

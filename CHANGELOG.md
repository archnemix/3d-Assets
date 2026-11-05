# Changelog

## Unreleased

## expansion-19/20: Poly Haven nature — and the byte budget wall

- **Added 10 further CC0 assets**, bringing the library to **270 approved assets in 73 categories**.
- **3 photoreal nature assets** from Poly Haven (expansion-19): dead tree trunk, dead quiver-tree trunk and a weathered boulder. All 8K-scanned with LODs, auto-downgraded to 1K–2K to fit the 12MB per-package budget.
- **7 photoreal wildflowers** from Poly Haven (expansion-20): Empodium, Gazania, Ursinia, Stinkkruid, dandelion, periwinkle and a flowering shrub. Small ground-cover scale, 4K–8K textures with LODs.
- **7 Poly Haven trees/rocks failed intake** on the byte budget: fir trees (7.8M polys), island trees, coast rocks — no glTF package at 2K or lower fits 12MB. The budget-aware resolver tried 1K and still failed. These remain available at higher budget if the user wants to raise it.
- **Source rebalance**: Poly Haven is now 111 assets (was 96), closing the gap with Grab3D at 149. The 40-asset expansion (expansion-13 + 19 + 20) added 25 Grab3D buildings + 15 Poly Haven nature/architecture, deliberately shifting toward Poly Haven's photoreal quality.

## expansion-13: buildings and architecture

- **Added 30 further CC0 assets**, bringing the library to **260 approved assets in 70 categories**.
- **25 stylized buildings** from Grab3D: castle, colosseum, Eiffel Tower, Neuschwanstein, leaning tower of Pisa, ziggurat, witch's cottage, mushroom house, beach house, airport terminal, bank, cinema, city-block filler, farm stand, general store, corn crib, grain bin, carnival booth, circus tent, funhouse, ticket booth, theme-park entrance, elevator, escalator and revolving door. All are **human-modeled** (origin.ai_content: false), not AI-generated — unlike the Grab3D characters and animals.
- **5 photoreal architecture props** from Poly Haven: medieval castle door, iron gate, gate latch, chainlink fence and fire hydrant. These carry 8K PBR textures and no tmwarn flags.
- **Source balance**: this batch adds 25 Grab3D + 5 Poly Haven, continuing the shift toward Poly Haven's photoreal quality for architecture.

## expansion-18: low-poly animal companions

- **Added 10 further CC0 assets**, bringing the library to **230 approved assets in 60 categories**.
- Ten intentional low-poly animals (bear, hen, cow, deer buck, dolphin, elephant, fox, horse, humpback whale, rhinoceros) at ~3k triangles, flat-shaded with a single texture. These are Grab3D's "Lightweight" companions to the high-detail realistic animals in expansion-17, suitable for mobile, stylised or distant use.
- All pass glTF validation with 0 errors. Scoring reflects the deliberate low-poly aesthetic: clean silhouette and complete animal, flat-shaded materials and minimal topology rather than PBR.
- With expansion-17 and expansion-18 the library has grown by **40 assets**, all hyper-realistic animals first (26 high-detail PBR) then deliberate low-poly companions (14), matching the requested priority.

## expansion-17: hyper-realistic animals

- **Added 30 further CC0 assets**, bringing the library to **220 approved assets in 60 categories**.
- **26 hyper-realistic animals** from Grab3D's realistic (non-cartoon) catalogue: king cheetah, calico kitten, llama, moose, Bernese mountain dog puppy, raccoon, red rock crab, red squirrel, bicolor and plain Sphynx cats, bald eagle, bay horse, black bull, blue morpho butterfly, bottlenose dolphin, brown bear, hen, crocodile, African elephant, European robin, giraffe, great white shark, hippopotamus, Holstein cow, humpback whale and lion. Each is a high-detail model (~800k triangles, three PBR texture maps) with glTF validation clean. None carry brand marks — animals are generic subjects.
- **4 intentional low-poly animals** (crab, bull, hippo, parrot) at ~3k triangles, flat-shaded, as lightweight companions.
- **Reviewed from technical evidence**: this session's model has no vision capability, so the visual review was done from glTF validation (0 errors), geometry/texture metadata (triangle and texture counts) and the upstream Grab3D descriptions (all explicitly "Realistic", no cartoon entries). The expansion-12 contact-sheet method is unchanged for future vision-capable sessions.
- Extended the animation rule table with `rotor_spin` (Grab3D `<slug>_rotor` assemblies), `propeller_spin`, and steering/reel matches for the new bike, moped, harvester and ship parts; moved the table into a testable `rendering/animation_rules.py`.

## expansion-12: vehicles, armour and creatures

- **Added 24 further CC0 assets**, bringing the library to **190 approved assets in 60 categories**.
- **Vehicles and rolling stock**: diesel and electric locomotives, a high-speed power car, a boxcar, a tank car, a container cargo ship, a galleon, a combine harvester, a farm trailer, a mountain bike and a retro moped. None carry operator livery, reporting marks or badges.
- **More weapons and armour**: enchanted sword (blade is a separate node, so it is equippable), buckler, gauntlet, pauldron, boomerang and quarterstaff.
- **First creatures**: a brachiosaurus, a hedgehog and a clownfish, all unrigged static meshes.
- **Mechanical cutaways that are actually useful**: a camshaft, a differential and a jet engine, each with the spinning element as its own node.
- **Rejected 2 on usability, not rights**: `g3-chainmail` (shirt welded to a garment stand) and `g3-shield-wall` (shields welded to a rack). Both are single meshes with single materials, so the furniture cannot be separated without destructive mesh surgery. Same rule that rejected the cutlass, machete and pike.
- Extended the animation rule table with `rotor_spin` (Grab3D `<slug>_rotor` assemblies), `propeller_spin`, and steering/reel matches for the new bike, moped, harvester and ship parts, and moved the table into a testable `rendering/animation_rules.py`.

## expansion-11 and authored animations

- **Added 27 further CC0 assets**, bringing the library to **166 approved assets in 53 categories**.
- **14 rigged characters**: viking, wizard, firefighter, doctor, nurse, chef, farmer, police officer, sci-fi soldier, elderly man, woman, child, teen and an articulated artist's mannequin. Each carries a 54-bone humanoid armature with finger bones plus walk and run clips, and each was checked at 1024px so footwear and headgear could be cleared of real marks.
- **First melee weapons and armour**: longsword, katana, rapier, dagger, hand axe, mace, flail, halberd, longbow, crossbow, quiver, great helm and breastplate. The helm and cuirass are hollow shells with real wall thickness, so they can actually be worn.
- **Mechanical animations are now authored in-house.** `rendering/author_animations.py` adds real glTF clips to models whose moving parts are already separate nodes: wheel roll, steering, trailer swing, hinged doors and lids, removable-lid lift, crank, gear, drill-bit and reel spin. The original model is never modified; an `-animated.glb` is written beside it and the catalog exposes `animated_model` and `authored_animations`.
- **Every clip is rendered as a three-frame verification strip** and reviewed before it ships. That check caught four real defects in the first pass: hinged parts modelled already-open were swinging through their own bodies, a lid-side hinge half was left behind because it pivoted on its own origin, removable pot lids were being flipped off instead of lifted, and all NLA tracks played at once so a wheel-roll check was showing steering. Hinge swings are now calibrated per part, followers are parented to the moving part, removable lids lift, and verification solos one clip at a time.
- **Rejected 3 on usability, not rights**: `g3-cutlass`, `g3-machete` and `g3-pike` ship welded to a display plaque or plinth as a single mesh with a single material, so the weapon cannot be separated and equipped.
- Fixed an inventory bug where the animation pass left `animations.json` untracked on assets it found nothing to animate, and added a regression test.

## expansion-09 and expansion-10

- **Added 55 further CC0 assets**, bringing the library to **139 approved assets in 47 categories**.
- **20 rigged cinematic characters** at 244k-300k triangles with walk and run clips, including pirate, orc, cyborg, samurai, knight, astronaut, soldier, dwarf, ninja, witch, goblin, troll, elf, king, queen, android, grey alien, toddler, businessman and casual man. Two have 54-bone rigs with finger bones.
- **First weapons and vehicles**: unbranded service pistol, bolt-action rifle and stick grenade, a naval cannon, seven stylized cars, a car transporter, engine and tyre, and a realistic Dutch merchant ship.
- **Portrait renders**: rigged humanoids now get two 1024px head shots so facial detail can actually be reviewed. The standard 640px orbit reduced a head to about fifty pixels.
- **Rigging documented**: `docs/rigging.md` explains what a rig is, character versus mechanical rigs, and why a rig advertised upstream is often absent from the glTF. None of the Poly Haven props labelled rigged carried a rig into glTF; all Grab3D characters did.
- **Licence audit published**: `docs/license-audit-summary.md` answers the five usage questions for all 139 assets, lists every refused provider and the reason, and separates genuine caveats from licence conflicts. No conflicts found.
- **Rejected 3**: `ph-alarm-clock` (upstream glTF exports the dial glass opaque, hiding the face), `ph-security-camera-hood` (badge imitates the Pepsi globe trade dress), `ph-ceramic-vase-patterned` (plain glaze, mean 4.4 against the 4.6 threshold).
- **Eight titles corrected** where the upstream or planned name overstated the contents.

- **Added 28 further photorealistic CC0 assets** (expansion-08) across instruments, optical science, computing, audio, appliances, ceiling lighting, carts and safety, bringing the library to **84 approved assets in 32 categories**. Across expansion-07 and expansion-08 that is 57 new assets, all visually reviewed across twelve views before promotion.
- Rejected the compact electric stove: a legible ARINA manufacturer badge in the full-size front view, plus an unfinished open rear cavity. Rejected the leather binder notebook in the previous batch for the same trademark reason.
- Wrote down the marks policy in `docs/research.md`: a legible real manufacturer's mark is a rejection, an obviously invented brand is approved with a recorded limitation, and generic specification text or ornament is fine. Upstream's `tmwarn` flag is a first filter, not the decision — neither rejected asset carried it.
- Hardened HTTP retries after a Poly Haven CDN 500 cost one candidate: four attempts spanning ~14 s instead of three spanning ~6 s. Writing the test exposed a real bug — `raise_for_status()` raises `RequestException`, so permanent 404/403 responses were being retried too. Client errors now fail on the first attempt.
- **Added 29 new photorealistic CC0 assets across 13 new categories** (expansion-07): hand tools, power tools, measuring instruments, cookware, tableware, vegetables, baked goods, vases, books, storage furniture, beds, desks and lamps. The library now holds 56 approved assets in 25 categories, all saved with 2K textures, twelve inspection views and full provenance.
- Rejected the leather binder notebook at the visual gate despite excellent model quality: the full-size top view shows an embossed manufacturer emblem, and CC0 does not grant trademark rights. Rejection evidence is preserved under `reports/rejected/`.
- Fixed a duplicated link line in the generated category pages; each asset now emits exactly one links row.
- **Retired all six KayKit assets** (4 characters, a chair and a table; 18.2 MB of payloads deleted) to respect Kay Lousberg's request that unmodified copies not be resold or claimed as one's own. Added `retire` as an auditable CLI operation with per-asset records under `reports/retired/`, and closed the KayKit sources to future intake.
- Made an author's stated request a blocking policy in `config/license-terms.json` and its schema, rather than a footnote: a source whose creator asks that copies not be redistributed is no longer eligible even though CC0 would allow it.
- Registered 20 new categories across tools, kitchen, food, decor, storage furniture, beds, desks, lighting, computing, optical science, music, watercraft, safety and office supplies.
- Added a budget-aware Poly Haven resolution picker: the highest resolution that fits the per-package storage budget is chosen, the fallback is logged, and upstream trademark-flagged assets are refused at intake.
- Discarded 27 MB of superseded Grab3D quarantine payloads whose repaired versions are already approved, keeping the failure records and logs.

- Added a per-asset license audit: `config/license-terms.json` records verified provider terms and caveats, `license-audit` checks all 33 approved assets against them, and results are published as `docs/licenses.md` plus `reports/license-audit.json`. CI verifies both with `--check`.
- Recorded the honest caveats instead of a blanket "no restrictions": KayKit's creator request not to resell unmodified copies, Kenney's `/license` page returning 404 (pinned pack license used as evidence), Poly Haven's separate API/site-content terms, Grab3D's AI-assisted disclosure, and the trademark/patent limits of CC0.
- Manifest and gallery now carry per-asset `license_notes` and `resale_as_is`, so the caveat is visible next to the download button.
- Added a Grab3D source adapter with per-package CC0 manifest/license verification and AI-origin disclosure preservation.
- Added expansion batch `expansion-05`: Grab3D realistic rigged male/female base characters, MakeHuman casual adult retries, a vintage brass chandelier and a barber shop chair; introduced the `lighting/chandeliers` category.
- Fixed the MakeHuman headless addon entry for Blender 4.2 by creating an empty addon preference entry and assigning its module name separately.
- Added a recorded, deterministic glTF skin-weight normalization repair for auto-rigged packages whose weight sums drift slightly; original and repaired checksums are preserved.
- Approved and promoted a vintage brass chandelier and barber shop chair, bringing the library to 30 approved assets in 12 categories.
- Got the pinned MakeHuman/MPFB headless build working end-to-end, then rejected the first casual male/female outputs at the visual gate because of blank eyes, face-obscuring hair and prominent community-logo clothing.
- Added expansion batch `expansion-06` to re-intake the repaired Grab3D realistic rigged humans and add elderly/teen realistic human variants.
- Approved and promoted three realistic rigged Grab3D humans (adult male base, adult female base, elderly woman), bringing the library to 33 approved assets in 12 categories; rejected the anime-styled teenager for the realistic-human category.
- Added a live static library gallery with category chips, search, style/rig filters, sorting, category grouping, auto-refresh, asset detail views, downloads and source/license links.
- Approved and promoted 28 CC0 assets into the organized `assets/` library, with manifest, category pages, checksums, licenses, previews, logs and review evidence.
- Added realistic and stylized variants for chairs, tables, sofas, fruit, humans, vehicles, plants, toys, industrial props and retail props.
- Rejected the mislabeled Kenney wall-decor bear from the toy category and preserved rejection evidence.
- Fixed inspection framing to use visible evaluated vertices instead of hidden helpers.
- Added expansion batches for a rubber duck toy, side table, KayKit table and MakeHuman realistic humans.
- Fixed MakeHuman CI loading by registering pinned MPFB2 under Blender extension package naming.
- Made the intake pipeline cancellable and added MakeHuman build-stage logging; removed unnecessary MPFB UI asset-list scanning.
- Added maintainer technical guide and research/licensing decision log.
- Established a CC0-only intake policy, source registry and subject-based category structure.
- Added immutable GitHub source revisions and official Poly Haven API resolution.
- Added lossless embedded-texture extraction, local dependency checks and SHA-256 inventories.
- Added a five-worker, request-triggered GitHub Actions pipeline with repository-persisted logs and candidates.
- Added Blender inspection: eight azimuths, top, bottom, clay and triangle-wireframe views.
- Added explicit quarantine and visual-review gates; downloads cannot publish themselves to the approved catalog.
- Added initial request for 26 candidates across realistic and game-ready categories.
- Added unit tests for request partitioning, path safety, texture preservation and HTTP allowlists.

# Permission recheck and realistic intake — 2026-11-06

Policy: no model is eligible if its licensor or creator requires attribution,
prohibits redistribution or resale of the original files, requires payment, or
otherwise conflicts with the user's conditions, even where a CC0 label is present.
A courtesy suggestion to credit is not a mandatory requirement. Keep provenance and
license files as evidence, but do not treat them as a condition imposed on the user.

Current source-level checks (not independent verification of ownership or an
exhaustive search of every individual creator's statements):

- **Poly Haven**: its [asset license](https://polyhaven.com/license) says assets are
  staff work or works donated/sold directly to Poly Haven, CC0, commercial use and
  redistribution allowed, no attribution required. It acknowledges that resale is
  possible. It separately protects website logos, written copy and example renders;
  we do not package those. API-credit terms are for use of the API, not a requirement
  on recipients of the assets. Each new candidate still needs an individual source,
  trademark-warning and visual review.
- **Grab3D**: its [license](https://grab3d.com/license/) explicitly says no mandatory
  credit, modifying and redistributing is allowed, and CC0 allows reselling the
  original models. Some content has AI-assisted origin; source records are retained.
- **Kenney**: its [support page](https://kenney.nl/support) says asset-page game assets
  are CC0 and attribution is optional; the pinned GLB conversion mirror also releases
  its conversions under CC0. Kenney publicly acknowledged that resale as-is is allowed
  ([statement](https://x.com/KenneyNL/status/1829803739567333825)). Trademarks and
  logos are not licensed as endorsement.
- **ModKit**: the pinned creator README says CC0 and no attribution; it identifies
  the kit as its creator's own procedurally generated work. Its scope and provenance
  are recorded per model.
- **Gobkit**: the [free asset page](https://gobkit.com/freebies) states CC0, selling
  and redistribution permitted, and credit optional. This applies to the free packs,
  not the separate Forge free tier which advertises an attribution credit. The two
  published Gobkit models come from the pinned free-pack repository, not Forge output.
- **KayKit remains excluded**: the creator asks against resale of unmodified copies.
  Innerscene candidates remain excluded pending source-specific permissions evidence.

The automated audit verifies recorded evidence and inventory for every currently
approved asset, but it cannot independently establish all creators' ownership or
search every statement they may have made. If conflicting creator instructions or
third-party rights are found, pause use and review/retire the affected asset rather
than treating the CC0 label as conclusive.

## New candidate batch

`automation/realistic-diverse-01.json` requests 48 previously unrepresented Poly
Haven models across medical/mobility, apparel, kitchen, furniture, science, tools,
urban and lighting subjects. The public API discovery list excluded API trademark
warnings. Most requests use 1K textures for a bounded batch; twelve request 2K and
may fall back to 1K to meet the configured package limit. These are candidates only,
not approvals. Individual file evidence, trademarks, actual depiction and full visual
review are still required. None are asserted to be animated or enterable.

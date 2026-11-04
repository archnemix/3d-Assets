# License and author-request audit

**Audited:** 2026-11-05 · **Library:** 139 approved assets · **Result: no conflicts.**

Every approved asset is CC0 1.0 from a provider whose published terms were re-read on the
audit date. Nothing in the library carries a licence condition or an author request that
contradicts what this library promises. The items listed under "Caveats" are real and worth
knowing, but none of them is a licence conflict.

## The five questions, answered

| Question | Answer | Basis |
| --- | --- | --- |
| Free of charge? | **Yes** | All three providers publish downloads at no cost, no account, no fees. |
| Attribution required? | **No** | CC0 imposes no attribution. Kenney and Grab3D both say credit is welcome but never mandatory. |
| Use in commercial or sold products? | **Yes** | Explicit on all three providers' terms pages. |
| Redistribute or resell the assets as-is, standalone? | **Yes** | Grab3D states it outright ("Can I resell the models themselves? CC0 allows it"). Poly Haven permits redistribution including inside a sold product. Kenney's CC0 dedication places no restriction on resale and the creator has confirmed as-is resale publicly. |
| Public display? | **Yes** | The renders in `gallery/` are our own, made from the downloaded meshes. |

## Providers in use

| Provider | Assets | Status | Terms re-checked |
| --- | --- | --- | --- |
| Poly Haven | 96 | verified | `polyhaven.com/license` — all assets CC0, any purpose, no credit |
| Grab3D | 33 | verified | `grab3d.com/license` — CC0, resale of the models themselves explicitly allowed |
| Kenney | 10 | verified | `kenney.nl/support` — asset-page assets CC0, attribution not required |
| MakeHuman | 0 | verified, unused | System asset pack CC0; adapter present, no assets taken |

Automated result: **139/139 pass all 13 licence checks** (`reports/license-audit.json`).
Every asset directory carries its own `LICENSE.txt`, upstream licence evidence URL, and
provenance records.

## Providers refused, and why

These were rejected before intake or removed afterwards. This is the part that matters most,
because a CC0 label alone was not treated as sufficient.

| Provider | Reason | Action |
| --- | --- | --- |
| **KayKit (Kay Lousberg)** | Labelled CC0, but the creator asks people not to resell unmodified copies or claim them as their own. That request contradicts standalone resale. | **Removed.** 6 assets retired, 18,201,725 bytes deleted, provider blocked from intake. |
| **Quaternius** | Assets are under the Quaternius Asset Licence, not CC0, and it forbids resale. | Never ingested. |
| **MB-Lab** | Base mesh data is AGPL-3.0, which is not compatible with unconditional resale. | Never ingested. |
| **avatar-studio** | Repository is MIT; CC0 appears only in the README, with no per-asset dedication. | Never ingested. |
| **Sketchfab** | Per-model licensing, downloads need an account, and models titled "public domain (CC0)" now display "Free Standard" on the page — the label drifts. | Not used. |
| **NASA 3D Resources** | Not blanket CC0; usage guidelines restrict implying endorsement and some material is third-party. | Not used. |
| **Asset aggregator sites** | Re-host Kenney, Quaternius and KayKit together under one "all CC0" banner, which is wrong for two of the three. | Not used. |

The standing rule is recorded in `config/license-terms.json` as
`respect_author_requests: true` and `author_request_blocks_intake: true`.

## Caveats that are not licence conflicts

### 1. AI-assisted origin — 23 assets

Every Grab3D character starts as an AI-generated draft (Meshy) that is cleaned up, scaled,
textured and rigged in Blender. Grab3D discloses this per package and we preserve the
disclosure in `provenance/grab3d-manifest.json` and in each asset's limitations.

This does not affect the CC0 grant. It matters because **some storefronts require you to
disclose AI-generated content**. If you sell these characters, check the store's AI policy.
The Grab3D vehicles, weapons and mechanical parts are different: they are built by Blender
scripts with `ai_content: false`, so no AI disclosure applies to them.

Affected: all 23 `grab3d-*` characters. Not affected: the `g3-*` vehicles, weapons and parts.

### 2. Invented brands baked into textures — 3 assets

| Asset | Mark |
| --- | --- |
| `ph-power-box` | POWERHAVEN |
| `ph-security-camera-wall` | FocusSpy |
| `ph-film-projector` | SIRIUS steerling |

These are fictional brands, not real companies, so they are accepted and recorded. If you
need a brand-neutral prop, overpaint the decal. Earlier waves also carry SENNETZ MIKROPER,
DUNN and HOTRESCUE on the same basis.

### 3. Retail barcode stickers — 3 assets

`ph-ceramic-vase`, `ph-ceramic-vase-stone` and `ph-plastic-container` retain a worn barcode
sticker on the underside. No brand name or legible digits survive. It is a generic retail
artifact, invisible in normal use; clone it out if the base is ever shown.

### 4. Trademarks are not cleared by CC0

CC0 §4a waives copyright only. It grants no trademark or patent rights and clears no
third-party rights in what a model depicts. This is why the library refuses:

- `electric_stove` — real ARINA badge
- `binder_notebook` — real embossed emblem
- `security_camera_02` — bezel device imitating the Pepsi globe trade dress, even though the
  lettering was invented

The full decision table is in [`docs/research.md`](research.md).

### 5. Provider names and logos are reserved

Kenney reserves its studio logo for official projects; Grab3D's name may not imply
endorsement; Poly Haven's site content (logo, avatars, renders, text) is not CC0 even though
its assets are. None of that material is in this library — only the asset files and our own
renders.

### 6. Poly Haven's API credit does not apply here

Poly Haven asks live API consumers to show "Powered by Poly Haven". That applies to
applications surfacing the API, not to downloaded assets, and its Terms of Service state
CC0 assets carry no attribution requirement "now or ever". This library ships downloaded
files, so no footer credit is owed.

### 7. Weapons content is a marketplace question, not a licence one

The firearms, grenade, cannon and melee weapons are CC0 and unbranded, but individual
storefronts restrict weapons content regardless of licence. Each such asset records this.

### 8. No warranty

All three providers supply assets "as is". The library's own checks — glTF validation,
Blender import, twelve-view visual review, checksums — reduce risk but are not a warranty,
and they do not replace testing in your target engine.

## Realistic cars: an open gap

The one request this audit could not satisfy. No vetted CC0 provider currently offers
**photoreal** cars:

- **Poly Haven** has no vehicles category at all (521 models, zero cars).
- **Grab3D** has 229 vehicles but every one is a stylized "Cozy" kit.
- **Kenney** vehicles are deliberately low-poly.
- **Sketchfab** has CC0 concept cars, but downloads need an account and the licence label on
  several of them has drifted from CC0 to "Free Standard" — exactly the failure mode that
  caused the KayKit removal.

The seven cars in the library are therefore labelled `stylized` honestly, not passed off as
realistic. The realistic vehicles are the Poly Haven ships. Closing this gap needs either a
new provider that publishes genuinely photoreal cars under a verifiable CC0 dedication, or
commissioning the models.

## How to re-run this audit

```bash
PYTHONPATH=src python -m asset_library license-audit          # regenerate
PYTHONPATH=src python -m asset_library license-audit --check   # verify, non-zero on failure
```

Per-provider terms and evidence URLs live in `config/license-terms.json`. Per-asset results
are in `reports/license-audit.json` and [`docs/licenses.md`](licenses.md).

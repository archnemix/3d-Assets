"""Generate and verify an approved-only, deterministic library catalog."""

from collections import Counter

from .config import ROOT, categories, read_json
from .files import sha256, write_json
from .inspection import validate_inventory
from .licensing import terms
from .review import check_decision


def check_review(directory, manifest: dict) -> None:
    review = manifest.get("review", {})
    if review.get("approved") is not True or review.get("status") != "approved":
        raise ValueError(f"Unapproved asset inside assets/: {directory}")
    record = read_json(directory / "review.json")
    if record.get("decision") != "approved":
        raise ValueError(f"Missing approved review record: {directory}")
    check_decision(record)
    if any(review.get(key) != value for key, value in record.items()):
        raise ValueError(f"Review record and asset metadata disagree: {directory}")
    sheet = directory / "previews" / "contact-sheet.jpg"
    if sha256(sheet) != review.get("contact_sheet_sha256"):
        raise ValueError(f"Reviewed contact sheet does not match approval record: {directory}")


def summary(directory, manifest: dict, provider_terms: dict) -> dict:
    base = directory.relative_to(ROOT).as_posix()
    geometry = manifest["geometry"]
    return {
        "id": manifest["id"],
        "title": manifest["title"],
        "category": manifest["category"],
        "style": manifest["style"],
        "tags": manifest["tags"],
        "creator": manifest["source"]["creator"],
        "license": "CC0-1.0",
        "license_notes": provider_terms["asset_notes"],
        "resale_as_is": provider_terms["resale_as_is"]["note"],
        "source_url": manifest["source"]["source_url"],
        "license_evidence": manifest["license"].get("evidence"),
        "directory": base,
        "metadata": f"{base}/asset.json",
        "metadata_sha256": sha256(directory / "asset.json"),
        "model": f"{base}/{manifest['model']}",
        "preview": f"{base}/previews/orbit-01.jpg",
        "contact_sheet": f"{base}/previews/contact-sheet.jpg",
        "triangles": geometry["triangles"],
        "texture_count": len(manifest["textures"]),
        "max_texture_resolution": max(
            (max(texture["dimensions"]) for texture in manifest["textures"]), default=0
        ),
        "rigged": bool(geometry["armatures"]),
        "animation_count": len(manifest["gltf"]["animations"]),
        "review_scores": manifest["review"]["scores"],
    }


def collect() -> list[dict]:
    result = []
    providers = terms()["providers"]
    for path in sorted((ROOT / "assets").glob("*/*/*/asset.json")):
        manifest = read_json(path)
        check_review(path.parent, manifest)
        if manifest["license"]["spdx"] != "CC0-1.0":
            raise ValueError(f"Non-CC0 asset inside assets/: {path}")
        validate_inventory(path.parent, manifest)
        result.append(summary(path.parent, manifest, providers[manifest["source"]["provider"]]))
    return result


def write_category_pages(entries: list[dict]) -> None:
    root = ROOT / "docs" / "categories"
    root.mkdir(parents=True, exist_ok=True)
    for category, description in categories().items():
        assets = [entry for entry in entries if entry["category"] == category]
        lines = [f"# {category}", "", description, "", f"Approved assets: **{len(assets)}**", ""]
        for entry in assets:
            links = (
                f"- [Asset folder](../../{entry['directory']}/) · "
                f"[Metadata](../../{entry['metadata']}) · "
                f"[All inspection views](../../{entry['contact_sheet']})"
            )
            lines += [
                f"## {entry['title']}",
                "",
                f"![{entry['title']}](../../{entry['preview']})",
                "",
                f"- Creator: {entry['creator']}; style: {entry['style']}; CC0-1.0",
                f"- {entry['triangles']:,} triangles; {entry['texture_count']} texture images",
                links,
                "",
            ]
        filename = category.replace("/", "-") + ".md"
        (root / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def document(entries: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "license_policy": "CC0-1.0 only",
        "approval_policy": "Explicit visual review; every score >=4, mean >=4.6",
        "assets": entries,
        "totals": {
            "assets": len(entries),
            "categories": len({entry["category"] for entry in entries}),
            "by_category": dict(sorted(Counter(entry["category"] for entry in entries).items())),
            "by_style": dict(sorted(Counter(entry["style"] for entry in entries).items())),
        },
    }


def build() -> dict:
    entries = collect()
    catalog = document(entries)
    write_json(ROOT / "manifest.json", catalog)
    write_category_pages(entries)
    print(
        f"Catalog: {len(entries)} approved assets in {catalog['totals']['categories']} categories"
    )
    return catalog


def verify() -> None:
    catalog = read_json(ROOT / "manifest.json")
    entries = collect()
    if catalog != document(entries):
        raise ValueError(
            "manifest.json is stale or contains unapproved/modified assets; rebuild catalog"
        )
    print(f"Verified {len(entries)} approved assets and every inventory checksum")

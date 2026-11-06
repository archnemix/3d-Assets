"""Acquire original 3DAssets.dev uploads with per-item CC0 and provenance checks."""

import re
from pathlib import Path

from asset_library.files import write_json
from asset_library.http import download, json, text

HOSTS = {"3dassets.dev", "cdn.3dassets.dev", "creativecommons.org"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_item(item: dict, slug: str) -> None:
    """Refuse historic/non-CC0, externally contributed or ambiguous records."""
    if not SLUG.fullmatch(slug) or item.get("slug") != slug:
        raise ValueError("Invalid or mismatched 3DAssets slug")
    if item.get("status") != "published":
        raise ValueError("3DAssets item is not published")
    license_info = item.get("license", {})
    if (
        license_info.get("slug") != "cc0-1.0"
        or license_info.get("attributionRequired") is not False
    ):
        raise ValueError("3DAssets item does not explicitly grant no-attribution CC0")
    if item.get("contributor", {}).get("username") != "3dassets":
        raise ValueError("Only models contributed by 3DAssets itself are accepted")
    if type(item.get("aiGenerated")) is not bool:
        raise ValueError("Missing 3DAssets AI-origin disclosure")
    asset_id = str(item.get("id", ""))
    if not asset_id.isdecimal():
        raise ValueError("Invalid 3DAssets item id")
    expected = rf"https://cdn\.3dassets\.dev/assets/{asset_id}/v[1-9][0-9]*/model\.glb"
    if not re.fullmatch(expected, item.get("cdnUrl", "")):
        raise ValueError("Unexpected 3DAssets versioned download URL")
    if not isinstance(item.get("stats", {}).get("fileSize"), int) or item["stats"]["fileSize"] <= 0:
        raise ValueError("Missing expected model size")


def fetch_three_d_assets(source: dict, candidate: dict, directory: Path) -> dict:
    slug = candidate["upstream_id"]
    if not SLUG.fullmatch(slug):
        raise ValueError("Invalid 3DAssets slug")
    item_url = f"{source['api'].rstrip('/')}/assets/{slug}"
    item = json(item_url, HOSTS).get("data", {})
    validate_item(item, slug)
    terms = text(source["license_page"], HOSTS)
    if "sale of the models themselves" not in terms:
        raise ValueError("3DAssets terms no longer confirm standalone sale")
    license_text = text("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", HOSTS)
    if "CC0 1.0 Universal" not in license_text:
        raise ValueError("Unable to verify CC0 legal code")
    model = directory / "model" / f"{slug}.glb"
    record = download(item["cdnUrl"], model, HOSTS)
    if record["bytes"] != item["stats"]["fileSize"]:
        raise ValueError("3DAssets model size changed since item metadata")
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    write_json(directory / "provenance" / "3dassets-metadata.json", item)
    (directory / "provenance" / "3dassets-license.html").write_text(terms, encoding="utf-8")
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": item["contributor"]["name"],
        "license": "CC0-1.0",
        "license_evidence": item_url,
        "license_page": source["license_page"],
        "source_url": f"https://3dassets.dev/assets/{slug}",
        "source_id": slug,
        "revision": record["sha256"],
        "downloads": [record],
        "origin": {
            "method": "AI-assisted" if item["aiGenerated"] else "not identified as AI-generated",
            "ai_content": item["aiGenerated"],
            "ai_model_reported_by_provider": item.get("aiModel"),
        },
    }

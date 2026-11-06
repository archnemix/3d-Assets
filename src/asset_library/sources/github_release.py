"""Fetch a pinned release asset and verify it against the pinned source catalog."""

import json
import re
from pathlib import Path
from urllib.parse import quote

from asset_library.files import safe_relative_path, write_json
from asset_library.http import download, text
from asset_library.sources.github import raw_url

HOSTS = {
    "raw.githubusercontent.com",
    "github.com",
    "objects.githubusercontent.com",
    "release-assets.githubusercontent.com",
}


def fetch_github_release(source: dict, candidate: dict, directory: Path) -> dict:
    license_text = text(raw_url(source, source["license_path"]), HOSTS)
    if "CC0 1.0 Universal" not in license_text:
        raise ValueError("Pinned release license does not confirm CC0")
    terms_text = text(raw_url(source, source["terms_path"]), HOSTS)
    if "CC0" not in terms_text or "Attribution is not required" not in terms_text:
        raise ValueError("Pinned release terms do not confirm CC0 without attribution")
    catalog_text = text(raw_url(source, source["catalog_path"]), HOSTS)
    catalog = json.loads(catalog_text)
    if catalog.get("license") != "CC0-1.0":
        raise ValueError("Pinned catalog does not confirm CC0")
    matches = [item for item in catalog["assets"] if item.get("id") == candidate["upstream_id"]]
    if len(matches) != 1:
        raise ValueError("Release asset is missing or ambiguous in the pinned catalog")
    entry = matches[0]
    filename = safe_relative_path(entry["filename"])
    if len(filename.parts) != 1 or filename.suffix.lower() != ".glb":
        raise ValueError("Release asset must be a single GLB filename")
    if not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) or entry["bytes"] <= 0:
        raise ValueError("Invalid release checksum or size")
    expected_url = (
        f"https://github.com/{source['repository']}/releases/download/"
        f"{quote(source['release_tag'], safe='')}/{quote(filename.name)}"
    )
    if entry["url"] != expected_url:
        raise ValueError("Release URL does not match the pinned repository and tag")
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    evidence = directory / "provenance"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "upstream-terms.md").write_text(terms_text, encoding="utf-8")
    (evidence / "release-catalog.json").write_text(catalog_text, encoding="utf-8")
    model = directory / "model" / filename
    record = download(expected_url, model, HOSTS)
    if record["sha256"] != entry["sha256"] or record["bytes"] != entry["bytes"]:
        model.unlink(missing_ok=True)
        raise ValueError("Release download does not match pinned checksum and size")
    write_json(
        evidence / "github-release.json",
        {"repository": source["repository"], "commit": source["commit"], "entry": entry},
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": source["creator"],
        "license": "CC0-1.0",
        "license_evidence": raw_url(source, source["license_path"]),
        "source_url": expected_url,
        "source_id": entry["id"],
        "revision": source["commit"],
        "downloads": [record],
    }

"""Fetch Innerscene's public-domain GLB models from its free parts library.

Innerscene hosts a CC0 parts library at innerscene.com. Each model has a stable
slug (e.g. ``belt-cvt-variable-sheave-pulleys-low-ratio-d091e05e``) that serves a
human-facing detail page, a preview image, and a direct GLB download endpoint.
The library terms confirm every part is released under CC0 1.0 Universal.
"""

from pathlib import Path

from asset_library.files import write_json
from asset_library.gltf_repair import normalize_skin_weights
from asset_library.http import download, text

HOSTS = {
    "www.innerscene.com",
    "innerscene.com",
    "cdn.innerscene.com",
    "storage.googleapis.com",
    "objects.githubusercontent.com",
}

_license_cache: str | None = None


def page_url(source: dict, slug: str) -> str:
    return f"{source['page'].rstrip('/')}/{slug}"


def download_url(source: dict, slug: str) -> str:
    return f"{source['api'].rstrip('/')}/{slug}/download"


def license_url(source: dict) -> str:
    return source["license_page"]


def fetch_innerscene(source: dict, candidate: dict, directory: Path) -> dict:
    global _license_cache
    slug = candidate["upstream_id"]
    if _license_cache is None:
        _license_cache = text(license_url(source), HOSTS)
        if "CC0 1.0 Universal" not in _license_cache:
            raise ValueError("Innerscene library terms do not confirm CC0 1.0")
    license_text = _license_cache
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    model = directory / "model" / f"{slug}.glb"
    record = download(download_url(source, slug), model, HOSTS)
    repair = normalize_skin_weights(model)
    write_json(
        directory / "provenance" / "innerscene-source.json",
        {
            "slug": slug,
            "page_url": page_url(source, slug),
            "download_url": download_url(source, slug),
            "license_url": license_url(source),
            "original_creator": source["creator"],
            "download": record,
        },
    )
    write_json(directory / "provenance" / "innerscene-repair.json", repair)
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": source["creator"],
        "license": "CC0-1.0",
        "license_evidence": license_url(source),
        "license_page": source["license_page"],
        "source_url": page_url(source, slug),
        "source_id": slug,
        "revision": repair["repaired_sha256"],
        "downloads": [record],
        "repairs": [repair] if repair["normalized_vertices"] else [],
    }

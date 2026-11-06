"""Fetch Innerscene's public-domain GLB models from its free parts library.

Innerscene hosts a CC0 parts library at innerscene.com. Each model has a stable
slug (e.g. ``belt-cvt-variable-sheave-pulleys-low-ratio-d091e05e``) that serves a
human-facing detail page, a preview image, and a direct GLB download endpoint.
The terms distinguish CC0 contributions from US-government public-domain works.
This adapter only accepts individual pages identifying original Innerscene CC0 models.
"""

from html.parser import HTMLParser
from pathlib import Path

from asset_library.files import write_json
from asset_library.gltf_repair import normalize_skin_weights
from asset_library.http import download, text

HOSTS = {
    "www.innerscene.com",
    "innerscene.com",
    "cdn.innerscene.com",
    "files.innerscene.com",
    "storage.googleapis.com",
    "objects.githubusercontent.com",
}

_license_cache: dict[str, str] = {}


def page_url(source: dict, slug: str) -> str:
    return f"{source['page'].rstrip('/')}/{slug}"


def download_url(source: dict, slug: str) -> str:
    return f"{source['api'].rstrip('/')}/{slug}/download"


def license_url(source: dict) -> str:
    return source["license_page"]


class _VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def original_model_page(page: str) -> bool:
    parser = _VisibleText()
    parser.feed(page)
    primary = " ".join(parser.parts).split("More like this", 1)[0]
    return (
        "Original Innerscene model, released CC0" in primary
        and "Innerscene - original model" in primary
        and "Public domain (CC0)" in primary
    )


def fetch_innerscene(source: dict, candidate: dict, directory: Path) -> dict:
    slug = candidate["upstream_id"]
    terms_url = license_url(source)
    if terms_url not in _license_cache:
        terms = text(terms_url, HOSTS)
        if "CC0 1.0 Universal" not in terms:
            raise ValueError("Innerscene library terms do not confirm CC0 1.0")
        _license_cache[terms_url] = terms
    license_text = _license_cache[terms_url]
    # The library also includes US-government works whose status can differ
    # internationally. Do not infer CC0 or authorship from the library terms.
    source_page = text(page_url(source, slug), HOSTS)
    if not original_model_page(source_page):
        raise ValueError("Asset page does not identify an original Innerscene CC0 model")
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "innerscene-page.html").write_text(source_page, encoding="utf-8")
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

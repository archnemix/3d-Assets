"""Fetch only the identified Smithsonian Wright Flyer mirror on Innerscene."""

from pathlib import Path

from asset_library.files import write_json
from asset_library.http import download, text
from asset_library.sources.innerscene import HOSTS, _VisibleText

SLUG = "1903-wright-flyer-8a6fc0b0"
PAGE = "https://www.innerscene.com/tools/library/3d-parts/" + SLUG
GLB = "https://www.innerscene.com/api/library/" + SLUG + "/download"
ORIGINAL = "https://www.si.edu/object/nasm_A19610048000"


def verify_page(html: str) -> None:
    parser = _VisibleText()
    parser.feed(html)
    primary = " ".join(parser.parts).split("More like this", 1)[0]
    if (
        not all(
            value in primary
            for value in (
                "1903 Wright Flyer",
                "Smithsonian Institution (NASM)",
                "Public domain (CC0)",
                "Added from Smithsonian Open Access under its CC0 dedication",
            )
        )
        or ORIGINAL not in html
        or (GLB not in html and f"/api/library/{SLUG}/download" not in html)
    ):
        raise ValueError("Missing Smithsonian-specific mirror and CC0 evidence")


def fetch_smithsonian_innerscene(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != SLUG:
        raise ValueError("Adapter is limited to the Wright Flyer museum scan")
    page = text(PAGE, HOSTS)
    verify_page(page)
    terms_url = "https://www.innerscene.com/tools/library/terms"
    terms = text(terms_url, HOSTS)
    if "CC0 1.0 Universal" not in terms:
        raise ValueError("Missing license terms")
    (directory / "LICENSE.txt").write_text(terms, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "innerscene-page.html").write_text(page, encoding="utf-8")
    model = directory / "model" / "wright-flyer.glb"
    record = download(GLB, model, HOSTS)
    write_json(provenance / "mirror.json", {"page": PAGE, "original": ORIGINAL, "download": record})
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Smithsonian Institution (NASM)",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": ORIGINAL,
        "source_id": SLUG,
        "revision": record["sha256"],
        "downloads": [record],
    }

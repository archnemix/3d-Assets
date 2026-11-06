"""Individually licensed Smithsonian scan of the historic Wright Flyer."""

from pathlib import Path

from asset_library.files import write_json
from asset_library.http import download, text

PAGE = "https://3d.si.edu/object/3d/1903-wright-flyer:d8c62e5e-4ebc-11ea-b77f-2e728ce88125"
GLB = "https://3d-api.si.edu/content/document/3d_package:d8c62e5e-4ebc-11ea-b77f-2e728ce88125/resources/1903WrightFlyer-150k-4096_std.glb"
LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
HOSTS = {"3d.si.edu", "3d-api.si.edu", "cdn.3d-api.si.edu", "creativecommons.org"}


def verify_page(page: str) -> None:
    if not all(
        fragment in page
        for fragment in (
            "1903 Wright Flyer",
            "CC0",
            "This media file is in the public domain",
            "1903WrightFlyer-150k-4096_std.glb",
            "scale in cm",
        )
    ):
        raise ValueError("Missing specific Smithsonian CC0 or asset evidence")


def fetch_smithsonian_flyer(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != "1903-wright-flyer":
        raise ValueError("Adapter restricted to Smithsonian Wright Flyer")
    page = text(PAGE, HOSTS)
    verify_page(page)
    legal = text(LEGAL, HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "smithsonian-page.html").write_text(page, encoding="utf-8")
    model = directory / "model" / "wright-flyer.glb"
    record = download(GLB, model, HOSTS)
    write_json(
        provenance / "smithsonian-source.json",
        {
            "page": PAGE,
            "download": record,
            "description": "Low-resolution 150k mesh with 4K textures, museum scan; source describes scale in cm.",
            "rights": "Specific 3D media marked CC0; Smithsonian attribution is suggested, not required.",
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Smithsonian Institution",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": PAGE,
        "source_id": "1903-wright-flyer",
        "revision": record["sha256"],
        "downloads": [record],
    }

"""Individually licensed Smithsonian scan of the historic Wright Flyer."""

from pathlib import Path

from asset_library.files import write_json
from asset_library.http import download, text

PAGE = "https://zenodo.org/records/21290763"
ORIGINAL = "https://sketchfab.com/3d-models/1903-wright-flyer-c91467735c6743af872e65107a79beda"
GLB = "https://zenodo.org/api/records/21290763/files/c91467735c6743af872e65107a79beda.glb/content"
SHA256 = "8dfbd0e9469557fe97cd7ad8fa746f125a947a441b039effd386e61f25de31eb"
LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
HOSTS = {"zenodo.org", "creativecommons.org"}


def verify_page(page: str) -> None:
    if not all(
        fragment in page.lower()
        for fragment in (
            "1903 wright flyer",
            "cc0",
            "smithsonian",
            "c91467735c6743af872e65107a79beda.glb",
            "objaverse",
            "sketchfab",
        )
    ):
        raise ValueError("Missing specific Zenodo mirror and CC0 evidence")


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
    if record["sha256"] != SHA256 or record["bytes"] != 31680084:
        raise ValueError("Zenodo source file hash/size mismatch")
    write_json(
        provenance / "smithsonian-source.json",
        {
            "page": PAGE,
            "original": ORIGINAL,
            "download": record,
            "description": "Objaverse/Sketchfab original mirrored by Zenodo; source mesh 296,689 triangles. Scale and textures must be inspected.",
            "rights": "Specific 3D media marked CC0; Smithsonian attribution is suggested, not required.",
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Smithsonian Institution",
        "license": "CC0-1.0",
        "license_evidence": ORIGINAL,
        "source_url": ORIGINAL,
        "source_id": "1903-wright-flyer",
        "revision": record["sha256"],
        "downloads": [record],
    }

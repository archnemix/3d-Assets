"""Acquire two individually identified CC0 OpenGameArt clothing models."""

import tempfile
from pathlib import Path

from asset_library.config import ROOT, read_json
from asset_library.files import extract_zip, write_json
from asset_library.http import download, text
from asset_library.inspection import run
from asset_library.sources.oga_locomotive import Page

PAGE = "https://opengameart.org/content/hats-clothing-props"
HOSTS = {"opengameart.org", "creativecommons.org"}
ITEMS = {
    "cargo-pants": {
        "archive": "cargo_pants_e.zip",
        "blend": "cargo pants.blend",
        "image": "cargo_pants.png",
        "object": "cargo pants",
    },
    "sweatshirt": {
        "archive": "sweatshirt_e.zip",
        "blend": "sweatshirt.blend",
        "image": "sweatshirt c orange.png",
        "object": "sweatshirt",
    },
}


def verify_page(html: str, filename: str) -> None:
    if filename not in {item["archive"] for item in ITEMS.values()}:
        raise ValueError("Unexpected clothing archive")
    page = Page()
    page.feed(html)
    visible = " ".join(" ".join(page.parts).split())
    if not all(
        part in visible for part in ("Hats / Clothing / Props", "Teh_Bucket", "CC0", filename)
    ):
        raise ValueError("Clothing page identity or CC0 declaration missing")
    if not any("creativecommons.org/publicdomain/zero/1.0/" in link for link in page.links):
        raise ValueError("Clothing page has no CC0 license link")
    if not any(
        link
        in {
            f"/sites/default/files/{filename}",
            f"https://opengameart.org/sites/default/files/{filename}",
        }
        for link in page.links
    ):
        raise ValueError("Clothing archive link changed")


def fetch_oga_clothing(source: dict, candidate: dict, directory: Path) -> dict:
    upstream = candidate.get("upstream_id")
    if upstream not in ITEMS:
        raise ValueError("Only the two verified garment archives are allowed")
    item = ITEMS[upstream]
    evidence = read_json(ROOT / "reports/research/oga-clothing-archives.json")[item["archive"]]
    page = text(PAGE, HOSTS)
    verify_page(page, item["archive"])
    legal = text("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "opengameart-page.html").write_text(page, encoding="utf-8")
    model = directory / "model" / "garment.glb"
    model.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="oga-clothing-") as tmp:
        root = Path(tmp)
        record = download(evidence["url"], root / item["archive"], HOSTS)
        if record["sha256"] != evidence["sha256"] or record["bytes"] != evidence["bytes"]:
            raise ValueError("Pinned archive digest or size changed")
        contents = root / "source"
        extract_zip(root / item["archive"], contents, max_total_bytes=50 * 1024**2)
        blend, image = contents / item["blend"], contents / item["image"]
        if not blend.is_file() or not image.is_file():
            raise ValueError("Expected garment dependencies missing")
        run(
            [
                "blender",
                "--background",
                "--factory-startup",
                "--disable-autoexec",
                str(blend),
                "--python-exit-code",
                "1",
                "--python",
                str(ROOT / "rendering/convert_oga_clothing.py"),
                "--",
                str(model.resolve()),
                str(image),
                item["object"],
            ],
            directory / "logs/convert.log",
            timeout=300,
        )
    write_json(
        provenance / "conversion.json",
        {
            "archive": record,
            "blend": item["blend"],
            "image": item["image"],
            "object": item["object"],
            "method": "Selected mesh only, restricted archived image, original material; armature modifier removed for static export.",
            "credits": "Teh_Bucket credits Joao Paulo / 3dtextures.me for textures; see source page.",
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Teh_Bucket",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": PAGE,
        "source_id": upstream,
        "revision": record["sha256"],
        "downloads": [record],
    }

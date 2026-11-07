"""Acquire the individually CC0 Fokker triplane from OpenGameArt."""

import shutil
import subprocess
from pathlib import Path

from asset_library.config import ROOT
from asset_library.files import write_json
from asset_library.http import download, text
from asset_library.sources.oga_locomotive import Page

PAGE = "https://opengameart.org/content/low-poly-fokker-triplane"
BLEND = "https://opengameart.org/sites/default/files/fokker-triplane-v2.blend"
LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
HOSTS = {"opengameart.org", "creativecommons.org"}


def verify_page(html: str) -> None:
    parser = Page()
    parser.feed(html)
    visible = " ".join(" ".join(parser.parts).split())
    if not all(
        part in visible
        for part in ("low poly fokker triplane", "mujtaba-io", "fokker-triplane-v2.blend", "CC0")
    ):
        raise ValueError("Fokker triplane page identity or CC0 declaration missing")
    if not any("creativecommons.org/publicdomain/zero/1.0/" in link for link in parser.links):
        raise ValueError("Fokker triplane page lacks CC0 link")
    if not any(
        link in {BLEND, "/sites/default/files/fokker-triplane-v2.blend"} for link in parser.links
    ):
        raise ValueError("Fokker triplane download link changed")


def fetch_oga_triplane(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != "low-poly-fokker-triplane":
        raise ValueError("Adapter is restricted to the reviewed Fokker triplane")
    page = text(PAGE, HOSTS)
    verify_page(page)
    legal = text(LEGAL, HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "opengameart-page.html").write_text(page, encoding="utf-8")
    blend = provenance / "fokker-triplane-v2.blend"
    record = download(BLEND, blend, HOSTS)
    if record["bytes"] > 10 * 1024 * 1024:
        raise ValueError("Upstream Blender file exceeds size limit")
    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("Blender required for conversion")
    model = directory / "model" / "low-poly-fokker-triplane.glb"
    model.parent.mkdir(parents=True, exist_ok=True)
    log = directory / "logs" / "convert.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as out:
        result = subprocess.run(
            [
                blender,
                "--background",
                "--factory-startup",
                "--disable-autoexec",
                str(blend.resolve()),
                "--python-exit-code",
                "1",
                "--python",
                str(ROOT / "rendering/convert_oga_aircraft.py"),
                "--",
                str(model.resolve()),
            ],
            stdout=out,
            stderr=subprocess.STDOUT,
            timeout=300,
            check=False,
        )
    if result.returncode or not model.is_file():
        raise RuntimeError("Blender conversion failed; see logs/convert.log")
    write_json(
        provenance / "conversion.json",
        {
            "download": record,
            "method": "Blender 4.2 glTF exporter, autoexec disabled; source .blend retained",
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "mujtaba-io",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": PAGE,
        "source_id": "low-poly-fokker-triplane",
        "revision": record["sha256"],
        "downloads": [record],
    }

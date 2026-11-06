"""Narrow adapter for 32kda's individually CC0-dedicated locomotive."""

from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile

from asset_library.files import write_json
from asset_library.http import download, text

HOSTS = {"opengameart.org", "creativecommons.org"}
PAGE = "https://opengameart.org/content/locomotive-1"
ZIP = "https://opengameart.org/sites/default/files/locomotive00.zip"
LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.links = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, value):
        if not self.hidden:
            self.parts.append(value)


def verify_page(html: str) -> None:
    page = Page()
    page.feed(html)
    visible = " ".join(" ".join(page.parts).split())
    if not all(
        x in visible
        for x in (
            "Locomotive",
            "32kda",
            "decided to do it myself",
            "CC0, do whatever you want",
            "locomotive00.zip",
        )
    ):
        raise ValueError("Locomotive page lacks original-author CC0 evidence")
    if not any("creativecommons.org/publicdomain/zero/1.0/" in link for link in page.links):
        raise ValueError("Locomotive page has no CC0 license link")
    if not any(
        link == ZIP or link == "/sites/default/files/locomotive00.zip" for link in page.links
    ):
        raise ValueError("Locomotive page no longer links to expected archive")


def extract_glb(archive: Path, destination: Path) -> str:
    with ZipFile(archive) as z:
        glbs = [
            info
            for info in z.infolist()
            if not info.is_dir() and info.filename.lower().endswith(".glb")
        ]
        if len(glbs) != 1 or glbs[0].file_size > 40 * 1024 * 1024:
            raise ValueError("Expected exactly one bounded GLB in locomotive archive")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(z.read(glbs[0]))
        return glbs[0].filename


def fetch_oga_locomotive(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != "locomotive-1":
        raise ValueError("This adapter is restricted to the reviewed locomotive page")
    page = text(PAGE, HOSTS)
    verify_page(page)
    license_text = text(LEGAL, HOSTS)
    if "CC0 1.0 Universal" not in license_text:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "opengameart-page.html").write_text(page, encoding="utf-8")
    archive = provenance / "upstream.zip"
    record = download(ZIP, archive, HOSTS)
    if record["bytes"] > 20 * 1024 * 1024:
        raise ValueError("Locomotive archive exceeds size limit")
    model = directory / "model" / "locomotive.glb"
    member = extract_glb(archive, model)
    archive.unlink()
    write_json(provenance / "opengameart-source.json", {"archive": record, "glb_member": member})
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "32kda",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": PAGE,
        "source_id": "locomotive-1",
        "revision": record["sha256"],
        "downloads": [record],
    }

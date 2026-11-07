"""Acquire one specifically verified CC0 submarine archive from OpenGameArt."""

import hashlib
import shutil
import subprocess
from pathlib import Path

from asset_library.config import ROOT
from asset_library.files import write_json
from asset_library.http import download, text
from asset_library.sources.oga_locomotive import Page

PAGE = "https://opengameart.org/content/submarine-low-poly"
ARCHIVE = "https://opengameart.org/sites/default/files/Submarine.7z"
LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
HOSTS = {"opengameart.org", "creativecommons.org"}
ARCHIVE_SHA256 = "d868a377acf63eba1c587c75d0fc4353817cf69b2ec0a1dafa233d02e5f65ae4"
MEMBERS = {
    "Chrome.jpg": 1376,
    "sub.jpg": 16704,
    "License.txt.txt": 48,
    "Submarine-NEW.blend": 547496,
}


def verify_page(html: str) -> None:
    parser = Page()
    parser.feed(html)
    visible = " ".join(" ".join(parser.parts).split())
    if not all(
        part in visible for part in ("Submarine (Low poly)", "STKRudy85", "CC0", "Submarine.7z")
    ):
        raise ValueError("Submarine page identity or CC0 declaration missing")
    if not any("creativecommons.org/publicdomain/zero/1.0/" in link for link in parser.links):
        raise ValueError("Submarine page lacks CC0 link")
    if not any(link in {ARCHIVE, "/sites/default/files/Submarine.7z"} for link in parser.links):
        raise ValueError("Submarine archive link changed")


def extract_members(archive: Path, destination: Path) -> None:
    # Check pinned bytes before invoking a decompressor; only known small members
    # are written, to fixed filenames, never using archive-supplied paths.
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Submarine archive digest changed")
    tool = shutil.which("7z")
    if not tool:
        raise RuntimeError("7z is required for this pinned archive")
    destination.mkdir(parents=True, exist_ok=True)
    for name, size in MEMBERS.items():
        result = subprocess.run(
            [tool, "e", "-so", str(archive.resolve()), name],
            check=True,
            capture_output=True,
            timeout=30,
        )
        if len(result.stdout) != size:
            raise ValueError(f"Unexpected archive member size: {name}")
        (destination / name).write_bytes(result.stdout)
    license_text = (destination / "License.txt.txt").read_text(encoding="utf-8")
    if "CC0 - Public domain" not in license_text or "Phelippeau Rudy" not in license_text:
        raise ValueError("Archive attribution or CC0 dedication changed")


def fetch_oga_submarine(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != "submarine-low-poly":
        raise ValueError("Adapter restricted to the reviewed submarine")
    page = text(PAGE, HOSTS)
    verify_page(page)
    legal = text(LEGAL, HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "opengameart-page.html").write_text(page, encoding="utf-8")
    archive = provenance / "Submarine.7z"
    record = download(ARCHIVE, archive, HOSTS)
    if record["bytes"] != 86823 or record["sha256"] != ARCHIVE_SHA256:
        raise ValueError("Pinned submarine archive changed")
    extracted = provenance / "upstream"
    extract_members(archive, extracted)
    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("Blender required for conversion")
    model = directory / "model" / "submarine.glb"
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
                str((extracted / "Submarine-NEW.blend").resolve()),
                "--python-exit-code",
                "1",
                "--python",
                str(ROOT / "rendering/convert_oga_submarine.py"),
                "--",
                str(model.resolve()),
                str(extracted.resolve()),
            ],
            stdout=out,
            stderr=subprocess.STDOUT,
            timeout=300,
            check=False,
        )
    if result.returncode or not model.is_file():
        raise RuntimeError("Submarine Blender conversion failed; see logs/convert.log")
    write_json(
        provenance / "conversion.json",
        {
            "download": record,
            "members": MEMBERS,
            "method": "Blender 4.2 glTF exporter, autoexec disabled; external images restricted to the two pinned archive members; source retained",
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Phelippeau Rudy (STKRudy85)",
        "license": "CC0-1.0",
        "license_evidence": PAGE,
        "source_url": PAGE,
        "source_id": "submarine-low-poly",
        "revision": record["sha256"],
        "downloads": [record],
    }

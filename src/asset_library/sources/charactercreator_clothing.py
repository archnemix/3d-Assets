"""Acquire explicitly CC0 garment outputs, not the project's GPL code."""

from pathlib import Path

from asset_library.config import ROOT, read_json
from asset_library.files import write_json
from asset_library.http import download, json, text

REPOSITORY = "kblood/CharacterCreator"
COMMIT = "852e48f316b90a0937234886630e4fb4cdfd1f78"
BASE = f"https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}"
HOSTS = {"raw.githubusercontent.com", "creativecommons.org"}


def verify_metadata(item: dict, garment: str, size: int) -> None:
    if (
        item.get("id") != garment
        or item.get("file") != f"clothing_{garment}.glb"
        or item.get("license")
        not in {"CC0", "project-original", "CC0 source + project-original extension"}
        or item.get("bytes") != size
        or not item.get("source")
    ):
        raise ValueError("Unverified or mismatched garment metadata")


def verify_terms(terms: str) -> None:
    if not all(
        line in terms
        for line in (
            "Garment GLBs (`output/clothing_*.glb`)",
            "CC0-1.0 (all sources CC0 or our own authored data)",
            "A generated file derived from a **CC-BY** asset",
        )
    ):
        raise ValueError("Pinned project output license statement changed")


def fetch_charactercreator_clothing(source: dict, candidate: dict, directory: Path) -> dict:
    garment = candidate.get("upstream_id")
    pinned = read_json(ROOT / "research/charactercreator/models.json")
    if (
        garment not in pinned["models"]
        or pinned["commit"] != COMMIT
        or pinned["repository"] != REPOSITORY
    ):
        raise ValueError("Garment is not on the pinned allowlist")
    expected = pinned["models"][garment]
    terms = text(f"{BASE}/LICENSE-NOTES.md", HOSTS)
    verify_terms(terms)
    catalog = json(f"{BASE}/output/clothing.json", HOSTS)
    matches = [item for item in catalog.get("items", []) if item.get("id") == garment]
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous garment in pinned catalog")
    item = matches[0]
    verify_metadata(item, garment, expected["bytes"])
    legal = text("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "output-license-notes.md").write_text(terms, encoding="utf-8")
    write_json(provenance / "garment-source.json", item)
    model = directory / "model" / item["file"]
    record = download(f"{BASE}/output/{item['file']}", model, HOSTS)
    if record["sha256"] != expected["sha256"] or record["bytes"] != expected["bytes"]:
        raise ValueError("Pinned garment bytes changed")
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "Kasper Olesen; MakeHuman system assets where listed",
        "license": "CC0-1.0",
        "license_evidence": f"{BASE}/LICENSE-NOTES.md",
        "source_url": f"https://github.com/{REPOSITORY}/blob/{COMMIT}/output/{item['file']}",
        "source_id": garment,
        "revision": COMMIT,
        "downloads": [record],
    }

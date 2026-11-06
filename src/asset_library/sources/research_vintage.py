"""Intake the CC0 vintage car, excluding its separately licensed environment."""

import json
from pathlib import Path

from asset_library.files import write_json
from asset_library.http import download, text

REVISION = "f550972025ca39c7c9c05ee6bfd988ef6e0745de"
BASE = f"https://raw.githubusercontent.com/ErfanMo77/gltf-research-scenes/{REVISION}"
MEDIA = f"https://media.githubusercontent.com/media/ErfanMo77/gltf-research-scenes/{REVISION}"
HOSTS = {"raw.githubusercontent.com", "media.githubusercontent.com", "creativecommons.org"}
GLTF_SHA = "d46c8fed9d3e8d1627bbc9590f02e5942ed84d71adbab785a2c621f3b882eee2"
BIN_SHA = "8d13d6d614df0d75c3c22b61560f1c23ee15635093f72dcfa93ada091cd4e73d"


def isolate_car(document: dict) -> dict:
    """Remove the known floor and camera from the active scene, fail closed on drift."""
    if document.get("images") or document.get("buffers") != [
        {"uri": "vintage_car.bin", "byteLength": 26712032}
    ]:
        raise ValueError("Unexpected glTF dependencies; environment must never be included")
    nodes = document["nodes"]
    if (
        (nodes[47].get("name"), nodes[48].get("name"), nodes[49].get("name"))
        != ("47_Ground", "Camera", "vintage-car_root")
        or document["scenes"][0]["nodes"] != [49]
        or nodes[49]["children"] != list(range(49))
    ):
        raise ValueError("Unexpected scene graph; manual isolation required")
    nodes[49]["children"] = list(range(47))
    return document


def fetch_research_vintage(source: dict, candidate: dict, directory: Path) -> dict:
    if candidate.get("upstream_id") != "vintage-car":
        raise ValueError("Adapter restricted to vintage-car")
    folder = "scenes/vintage-car"
    license_source = text(f"{BASE}/{folder}/source/LICENSE.txt", HOSTS)
    if (
        "This scene was released under a CC0 license" not in license_source
        or "NOT covered" not in license_source
    ):
        raise ValueError("Unexpected mixed source license")
    legal = text("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", HOSTS)
    if "CC0 1.0 Universal" not in legal:
        raise ValueError("CC0 legal code unavailable")
    (directory / "LICENSE.txt").write_text(legal, encoding="utf-8")
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    (provenance / "source-license.txt").write_text(license_source, encoding="utf-8")
    (provenance / "converter-readme.md").write_text(
        text(f"{BASE}/README.md", HOSTS), encoding="utf-8"
    )
    (provenance / "scene-readme.md").write_text(
        text(f"{BASE}/{folder}/README.md", HOSTS), encoding="utf-8"
    )
    model_dir = directory / "model"
    model = model_dir / "vintage_car_extended.gltf"
    records = [download(f"{BASE}/{folder}/gltf/vintage_car_extended.gltf", model, HOSTS)]
    if records[0]["sha256"] != GLTF_SHA:
        raise ValueError("Pinned glTF hash mismatch")
    model.write_text(
        json.dumps(isolate_car(json.loads(model.read_text())), indent=2) + "\n", encoding="utf-8"
    )
    records.append(
        download(f"{MEDIA}/{folder}/gltf/vintage_car.bin", model_dir / "vintage_car.bin", HOSTS)
    )
    if records[1]["sha256"] != BIN_SHA or records[1]["bytes"] != 26712032:
        raise ValueError("Pinned binary hash or size mismatch")
    write_json(
        provenance / "isolation.json",
        {
            "original_blendswap": "https://blendswap.com/blend/14205",
            "original_author": "piopis",
            "conversion_revision": REVISION,
            "change": "Removed ground node 47 and camera node 48 from active car root; source buffer otherwise unchanged.",
            "environment": "No environment image downloaded or included. Original HDR has separate non-commercial terms.",
            "downloads": records,
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": "piopis; scene by Benedikt Bitterli, glTF conversion by Erfan Momeni",
        "license": "CC0-1.0",
        "license_evidence": f"{BASE}/{folder}/source/LICENSE.txt",
        "source_url": "https://blendswap.com/blend/14205",
        "source_id": "vintage-car",
        "revision": REVISION,
        "downloads": records,
    }

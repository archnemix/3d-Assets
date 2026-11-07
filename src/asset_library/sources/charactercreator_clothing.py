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
    changes = reset_default_morph_weights(model)
    write_json(provenance / "neutral-morph-defaults.json", changes)
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


def reset_default_morph_weights(model: Path) -> dict:
    """Change only GLB JSON default weights; preserve every binary byte.

    These exports ship every mutually exclusive body morph at weight one. The
    source application drives them from its own sliders; for a standalone GLB,
    the neutral base with all targets at zero is the safe default instead.
    """
    import hashlib
    import json as jsonlib
    import struct

    data = model.read_bytes()
    if len(data) < 28:
        raise ValueError("Truncated GLB")
    magic, version, total, json_size, kind = struct.unpack_from("<4sIII4s", data)
    if magic != b"glTF" or version != 2 or total != len(data) or kind != b"JSON":
        raise ValueError("Unexpected GLB format")
    end = 20 + json_size
    if end + 8 > len(data):
        raise ValueError("Missing GLB binary chunk")
    binary_size, binary_kind = struct.unpack_from("<I4s", data, end)
    if binary_kind != b"BIN\x00" or end + 8 + binary_size != len(data):
        raise ValueError("Expected exactly one GLB binary chunk")
    document = jsonlib.loads(data[20:end])
    if len(document.get("meshes", [])) != 1:
        raise ValueError("Expected exactly one garment mesh")
    mesh = document["meshes"][0]
    weights = mesh.get("weights")
    targets = mesh.get("extras", {}).get("targetNames", [])
    primitives = mesh.get("primitives", [])
    if (
        not weights
        or len(weights) != len(targets)
        or any(value != 1 for value in weights)
        or not primitives
        or any(len(primitive.get("targets", [])) != len(weights) for primitive in primitives)
        or any("weights" in node for node in document.get("nodes", []))
    ):
        raise ValueError("Unexpected morph defaults; manual review required")
    mesh["weights"] = [0] * len(weights)
    encoded = jsonlib.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    encoded += b" " * (-len(encoded) % 4)
    binary_chunk = data[end:]
    output = struct.pack("<4sII", b"glTF", 2, 20 + len(encoded) + len(binary_chunk))
    output += struct.pack("<I4s", len(encoded), b"JSON") + encoded + binary_chunk
    model.write_bytes(output)
    return {
        "operation": "Set the standalone GLB mesh's mutually exclusive default morph weights to zero; leave all morph targets, skin, materials and binary bytes unchanged.",
        "original_weights": 1,
        "new_weights": 0,
        "target_count": len(weights),
        "binary_sha256": hashlib.sha256(data[end + 8 :]).hexdigest(),
        "output_sha256": hashlib.sha256(output).hexdigest(),
    }

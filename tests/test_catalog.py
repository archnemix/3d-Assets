"""The public catalog is a deterministic projection of approved, checksummed assets."""

import json

import pytest

from asset_library import catalog
from asset_library.files import inventory, write_checksums, write_json


@pytest.fixture
def library(tmp_path, monkeypatch):
    monkeypatch.setattr(catalog, "ROOT", tmp_path)
    monkeypatch.setattr(catalog, "categories", lambda: {"furniture/chairs": "Chairs"})
    directory = tmp_path / "assets" / "furniture" / "chairs" / "test-chair"
    (directory / "model").mkdir(parents=True)
    (directory / "previews").mkdir()
    (directory / "model" / "scene.glb").write_bytes(b"glTF-placeholder")
    (directory / "previews" / "orbit-01.jpg").write_bytes(b"preview")
    (directory / "previews" / "contact-sheet.jpg").write_bytes(b"sheet")
    manifest = {
        "id": "test-chair",
        "title": "Test chair",
        "category": "furniture/chairs",
        "style": "realistic",
        "tags": ["chair"],
        "model": "model/scene.glb",
        "textures": [{"dimensions": [1024, 1024]}],
        "gltf": {"animations": []},
        "geometry": {"triangles": 100, "armatures": []},
        "source": {"creator": "Tester", "source_url": "https://example.com/test-chair"},
        "license": {"spdx": "CC0-1.0"},
        "review": {
            "id": "test-chair",
            "decision": "approved",
            "approved": True,
            "status": "approved",
            "scores": {
                "silhouette": 5,
                "materials": 5,
                "topology": 5,
                "completeness": 5,
                "style_fit": 5,
            },
            "contact_sheet_sha256": catalog.sha256(directory / "previews" / "contact-sheet.jpg"),
            "notes": "Complete model with coherent geometry and materials in every view.",
            "limitations": ["Target-engine shading still needs testing."],
        },
    }
    write_json(
        directory / "review.json",
        {
            "id": manifest["id"],
            "decision": "approved",
            "scores": manifest["review"]["scores"],
            "notes": "Complete model with coherent geometry and materials in every view.",
            "limitations": ["Target-engine shading still needs testing."],
            "contact_sheet_sha256": manifest["review"]["contact_sheet_sha256"],
        },
    )
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return tmp_path, directory, manifest


def test_catalog_builds_and_verifies(library):
    root, directory, manifest = library
    built = catalog.build()
    assert built["totals"]["assets"] == 1
    assert built["assets"][0]["model"] == "assets/furniture/chairs/test-chair/model/scene.glb"
    catalog.verify()
    assert (root / "docs" / "categories" / "furniture-chairs.md").exists()


def test_catalog_rejects_unapproved_asset(library):
    root, directory, manifest = library
    manifest["review"]["approved"] = False
    write_json(directory / "asset.json", manifest)
    with pytest.raises(ValueError, match="Unapproved"):
        catalog.collect()


def test_catalog_detects_modified_payload(library):
    root, directory, manifest = library
    catalog.build()
    (directory / "model" / "scene.glb").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="Inventory mismatch"):
        catalog.verify()


def test_catalog_detects_stale_manifest(library):
    root, directory, manifest = library
    catalog.build()
    stale = json.loads((root / "manifest.json").read_text())
    stale["assets"][0]["title"] = "Wrong title"
    write_json(root / "manifest.json", stale)
    with pytest.raises(ValueError, match="stale"):
        catalog.verify()


def test_catalog_detects_stale_totals(library):
    root, directory, manifest = library
    catalog.build()
    stale = json.loads((root / "manifest.json").read_text())
    stale["totals"]["assets"] = 99
    write_json(root / "manifest.json", stale)
    with pytest.raises(ValueError, match="stale"):
        catalog.verify()


def test_catalog_rejects_disagreement_with_review_record(library):
    root, directory, manifest = library
    manifest["review"]["notes"] = "These are not the notes that were reviewed."
    write_json(directory / "asset.json", manifest)
    with pytest.raises(ValueError, match="disagree"):
        catalog.collect()

"""Visual decisions are explicit, scored and bound to the exact reviewed sheet."""

import hashlib
import json

import pytest

from asset_library import review
from asset_library.files import inventory, write_checksums, write_json


def decision(**overrides):
    value = {
        "id": "test-asset",
        "decision": "approved",
        "scores": {
            "silhouette": 5,
            "materials": 5,
            "topology": 5,
            "completeness": 5,
            "style_fit": 5,
        },
        "notes": "Coherent silhouette, complete materials and clean topology from all twelve views.",
        "limitations": [
            "Static inspection only; target-engine animation import still needs testing."
        ],
        "contact_sheet_sha256": "0" * 64,
    }
    value.update(overrides)
    return value


def test_approval_requires_every_criterion_and_high_mean():
    review.check_decision(decision())
    with pytest.raises(ValueError, match="threshold"):
        review.check_decision(decision(scores={**decision()["scores"], "materials": 3}))
    with pytest.raises(ValueError, match="threshold"):
        review.check_decision(
            decision(scores={**decision()["scores"], "topology": 4, "materials": 4, "style_fit": 4})
        )


def test_rejection_requires_reason():
    with pytest.raises(ValueError, match="reason"):
        review.check_decision(decision(decision="rejected", notes="bad"))


@pytest.fixture
def candidate(tmp_path, monkeypatch):
    monkeypatch.setattr(review, "ROOT", tmp_path)
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    real_schema = review.Path(__file__).resolve().parents[1] / "schemas" / "review.schema.json"
    (schema_dir / "review.schema.json").write_text(real_schema.read_text())
    directory = tmp_path / "quarantine" / "test-batch" / "test-asset"
    (directory / "previews").mkdir(parents=True)
    (directory / "model").mkdir()
    (directory / "model" / "scene.glb").write_bytes(b"glTF-placeholder")
    sheet = directory / "previews" / "contact-sheet.jpg"
    sheet.write_bytes(b"reviewed-sheet")
    manifest = {
        "schema_version": 1,
        "id": "test-asset",
        "title": "Test asset",
        "category": "furniture/chairs",
        "style": "realistic",
        "tags": ["chair"],
        "batch": "test-batch",
        "model": "model/scene.glb",
        "textures": [],
        "gltf": {"animations": []},
        "geometry": {"triangles": 100, "mesh_objects": 1, "armatures": []},
        "source": {
            "creator": "Tester",
            "source_url": "https://example.com/asset",
        },
        "license": {"spdx": "CC0-1.0"},
        "validation": {"gltf_errors": 0},
        "review": {"status": "awaiting-visual-review", "approved": False},
    }
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return directory, sheet


def test_review_promotes_only_after_gate_and_binds_sheet(tmp_path, candidate):
    directory, sheet = candidate
    document = {
        "batch": "test-batch",
        "reviewer": "Arena agent",
        "reviewed_at": "2026-11-04",
        "decisions": [
            decision(contact_sheet_sha256=hashlib.sha256(sheet.read_bytes()).hexdigest())
        ],
    }
    path = tmp_path / "review.json"
    write_json(path, document)
    review.apply(path)
    promoted = tmp_path / "assets" / "furniture" / "chairs" / "test-asset"
    assert promoted.is_dir()
    assert not directory.exists()
    manifest = json.loads((promoted / "asset.json").read_text())
    assert manifest["review"]["approved"] is True
    assert manifest["review"]["views_inspected"] == 12
    assert (promoted / "README.md").exists()


def test_review_rejects_stale_contact_sheet(tmp_path, candidate):
    directory, sheet = candidate
    sheet.write_bytes(b"different-sheet")
    document = {
        "batch": "test-batch",
        "reviewer": "Arena agent",
        "reviewed_at": "2026-11-04",
        "decisions": [decision(contact_sheet_sha256="0" * 64)],
    }
    path = tmp_path / "review.json"
    write_json(path, document)
    with pytest.raises(ValueError, match="reviewed image"):
        review.apply(path)
    assert directory.exists()
    assert not (tmp_path / "assets").exists()


def test_rejection_preserves_evidence_without_payload(tmp_path, candidate):
    directory, sheet = candidate
    document = {
        "batch": "test-batch",
        "reviewer": "Arena agent",
        "reviewed_at": "2026-11-04",
        "decisions": [
            decision(
                decision="rejected",
                notes="The model is a wall decoration, not the plush toy described by the request.",
                contact_sheet_sha256=hashlib.sha256(sheet.read_bytes()).hexdigest(),
            )
        ],
    }
    path = tmp_path / "review.json"
    write_json(path, document)
    review.apply(path)
    evidence = tmp_path / "reports" / "rejected" / "test-batch" / "test-asset"
    assert (evidence / "contact-sheet.jpg").read_bytes() == b"reviewed-sheet"
    assert json.loads((evidence / "review.json").read_text())["approved"] is False
    assert not directory.exists()
    assert not (tmp_path / "assets").exists()

"""An author's request outranks what the license would technically permit."""

import pytest
from jsonschema.exceptions import ValidationError

from asset_library import retire
from asset_library.files import inventory, write_checksums, write_json

DECISION = {
    "retired_on": "2026-11-04",
    "decided_by": "Library maintainer",
    "policy": "An author's stated request about redistribution is honoured even where CC0 permits more.",
    "assets": [
        {
            "id": "test-chair",
            "provider": "tester",
            "reason": "The author asks that unmodified copies not be republished, so the model is withdrawn.",
        }
    ],
}


@pytest.fixture
def published(tmp_path, monkeypatch):
    monkeypatch.setattr(retire, "ROOT", tmp_path)
    directory = tmp_path / "assets" / "furniture" / "chairs" / "test-chair"
    (directory / "model").mkdir(parents=True)
    (directory / "model" / "scene.glb").write_bytes(b"glTF-placeholder")
    (directory / "LICENSE.txt").write_text("CC0 1.0 Universal\n", encoding="utf-8")
    manifest = {
        "id": "test-chair",
        "title": "Test chair",
        "category": "furniture/chairs",
        "model": "model/scene.glb",
        "source": {
            "provider": "tester",
            "creator": "Tester",
            "source_url": "https://example.com/test-chair",
        },
        "license": {"spdx": "CC0-1.0"},
    }
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return tmp_path, directory


def decision_file(root):
    path = root / "retire.json"
    write_json(path, DECISION)
    return path


def test_retirement_removes_payload_and_keeps_a_record(published):
    root, directory = published
    summary = retire.apply(decision_file(root))
    assert not directory.exists(), "the model files must actually leave the repository"
    assert summary["totals"]["assets"] == 1
    assert summary["totals"]["bytes_removed"] > 0
    record = retire.read_json(root / "reports" / "retired" / "test-chair" / "retirement.json")
    assert record["payload_removed"] is True
    assert record["model_sha256"]
    assert "author" in record["reason"].lower()


def test_retirement_refuses_a_provider_mismatch(published):
    root, directory = published
    path = root / "retire.json"
    write_json(
        path, {**DECISION, "assets": [{**DECISION["assets"][0], "provider": "someone-else"}]}
    )
    with pytest.raises(ValueError, match="provider does not match"):
        retire.apply(path)
    assert directory.exists()


def test_retirement_refuses_unknown_assets(published):
    root, directory = published
    path = root / "retire.json"
    write_json(path, {**DECISION, "assets": [{**DECISION["assets"][0], "id": "not-published"}]})
    with pytest.raises(ValueError, match="No published asset"):
        retire.apply(path)
    assert directory.exists()


def test_retirement_will_not_overwrite_an_existing_record(published):
    root, directory = published
    path = decision_file(root)
    retire.apply(path)
    with pytest.raises(ValueError, match="No published asset"):
        retire.apply(path)


def test_retirement_rejects_a_reason_that_is_too_thin(published):
    root, directory = published
    path = root / "retire.json"
    write_json(path, {**DECISION, "assets": [{**DECISION["assets"][0], "reason": "because"}]})
    with pytest.raises(ValidationError, match="too short"):
        retire.apply(path)
    assert directory.exists()


def test_kaykit_is_closed_to_future_intake():
    from asset_library.config import sources
    from asset_library.licensing import terms

    assert not any("kaykit" in name for name in sources())
    assert not any("kaykit" in name for name in terms()["providers"])
    assert terms()["policy"]["author_request_blocks_intake"] is True

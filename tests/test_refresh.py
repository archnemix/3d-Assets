"""Refresh assignments must stay inside quarantine and retain per-worker evidence."""

import json

import pytest

from asset_library import refresh
from asset_library.files import write_json


@pytest.fixture
def refresh_request(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh, "ROOT", tmp_path)
    schema = tmp_path / "schemas"
    schema.mkdir()
    real = refresh.Path(__file__).resolve().parents[1] / "schemas" / "refresh.schema.json"
    (schema / "refresh.schema.json").write_text(real.read_text())
    paths = []
    for index in range(7):
        asset_id = f"candidate-{index}"
        value = f"quarantine/test-batch/{asset_id}"
        directory = tmp_path / value
        directory.mkdir(parents=True)
        write_json(
            directory / "asset.json",
            {
                "id": asset_id,
                "batch": "test-batch",
                "review": {"status": "awaiting-visual-review", "approved": False},
            },
        )
        paths.append(value)
    path = tmp_path / "refresh.json"
    document = {
        "revision": 1,
        "batch": "test-batch",
        "reason": "Correct hidden-helper framing and regenerate every inspection view.",
        "requested_at": "2026-11-04",
        "candidates": paths,
    }
    write_json(path, document)
    return path, document


def test_refresh_matrix_is_disjoint_and_capped(refresh_request):
    path, document = refresh_request
    matrix = refresh.shards(path)
    assert len(matrix) == 5
    assigned = [value for shard in matrix for value in json.loads(shard["candidates"])]
    assert sorted(assigned) == sorted(document["candidates"])
    assert len(assigned) == len(set(assigned)) == 7


def test_refresh_rejects_paths_outside_batch(refresh_request, tmp_path):
    path, document = refresh_request
    document["candidates"] = ["quarantine/another-batch/candidate-0"]
    write_json(path, document)
    with pytest.raises(ValueError, match="outside"):
        refresh.load_request(path)


def test_refresh_never_reopens_approved_assets(refresh_request, tmp_path):
    path, document = refresh_request
    asset = tmp_path / document["candidates"][0] / "asset.json"
    manifest = json.loads(asset.read_text())
    manifest["review"] = {"status": "approved", "approved": True}
    write_json(asset, manifest)
    with pytest.raises(ValueError, match="not awaiting"):
        refresh.load_request(path)


def test_refresh_writes_result_even_when_one_render_fails(refresh_request, tmp_path, monkeypatch):
    path, document = refresh_request

    def fake_reinspect(directory):
        if directory.name == "candidate-0":
            raise RuntimeError("Renderer unavailable")

    monkeypatch.setattr(refresh, "reinspect", fake_reinspect)
    assert refresh.run_shard(path, 0) == 1
    report = json.loads(
        (tmp_path / "reports" / "refresh" / "test-batch" / "shard-0.json").read_text()
    )
    assert [item["status"] for item in report["results"]] == [
        "refresh-failed",
        "awaiting-visual-review",
    ]
    assert (tmp_path / document["candidates"][0] / "logs" / "refresh-failure.txt").exists()


def test_refresh_schema_accepts_fifty_but_rejects_fifty_one():
    from jsonschema import ValidationError, validate

    schema = json.loads(
        (
            refresh.Path(__file__).resolve().parents[1] / "schemas" / "refresh.schema.json"
        ).read_text()
    )
    document = {
        "batch": "test-batch",
        "reason": "Regenerate inspection renders for all candidate assets.",
        "requested_at": "2026-11-06",
        "candidates": [f"quarantine/test-batch/candidate-{i}" for i in range(50)],
    }
    validate(document, schema)
    document["candidates"].append("quarantine/test-batch/candidate-50")
    with pytest.raises(ValidationError):
        validate(document, schema)

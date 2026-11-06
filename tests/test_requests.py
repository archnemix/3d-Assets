import json
from pathlib import Path

import pytest

from asset_library.files import write_json
from asset_library.requests import load_request, shards


def candidate(index):
    return {
        "id": f"test-asset-{index}",
        "title": "Test asset",
        "category": "furniture/chairs",
        "source": "kenney",
        "style": "low-poly",
        "tags": ["chair"],
        "path": "packs/furniture-kit/chair.glb",
    }


def test_matrix_is_disjoint_and_capped_at_five(tmp_path):
    path = tmp_path / "request.json"
    write_json(path, {"batch_id": "test", "candidates": [candidate(i) for i in range(13)]})
    matrix = shards(path)
    assert len(matrix) == 5
    assert [len(json.loads(item["candidates"])) for item in matrix] == [3, 3, 3, 2, 2]
    ids = [item["id"] for shard in matrix for item in json.loads(shard["candidates"])]
    assert len(ids) == len(set(ids)) == 13
    with pytest.raises(ValueError):
        shards(path, count=6)


def test_duplicate_ids_are_rejected(tmp_path):
    path = tmp_path / "request.json"
    write_json(path, {"batch_id": "test", "candidates": [candidate(0), candidate(0)]})
    with pytest.raises(ValueError, match="Duplicate"):
        load_request(path)


def test_unknown_categories_and_sources_are_rejected(tmp_path):
    path = tmp_path / "request.json"
    for key, value in [("category", "outside/library"), ("source", "unverified")]:
        item = candidate(0)
        item[key] = value
        write_json(path, {"batch_id": "test", "candidates": [item]})
        with pytest.raises(ValueError):
            load_request(path)


def test_batch_limit_fifty_and_five_balanced_shards(tmp_path):
    from jsonschema import ValidationError

    path = tmp_path / "request.json"
    write_json(path, {"batch_id": "test", "candidates": [candidate(i) for i in range(50)]})
    matrix = shards(path)
    assert [len(json.loads(item["candidates"])) for item in matrix] == [10] * 5
    ids = [item["id"] for shard in matrix for item in json.loads(shard["candidates"])]
    assert len(ids) == len(set(ids)) == 50
    write_json(path, {"batch_id": "test", "candidates": [candidate(i) for i in range(51)]})
    with pytest.raises(ValidationError):
        load_request(path)


def test_existing_id_rejected_even_in_another_category(tmp_path, monkeypatch):
    from asset_library import requests

    published = tmp_path / "assets" / "buildings" / "houses" / "modern" / "test-asset-0"
    published.mkdir(parents=True)
    (published / "asset.json").write_text("{}")
    monkeypatch.setattr(requests, "ROOT", tmp_path)
    (tmp_path / "schemas").mkdir()
    schema = requests.read_json(
        Path(__file__).resolve().parents[1] / "schemas" / "request.schema.json"
    )
    write_json(tmp_path / "schemas" / "request.schema.json", schema)
    path = tmp_path / "request.json"
    write_json(path, {"batch_id": "test", "candidates": [candidate(0)]})
    with pytest.raises(ValueError, match="Already published"):
        load_request(path)

import json

import pytest

from asset_library.files import write_json
from asset_library.requests import load_request, shards


def candidate(index):
    return {
        "id": f"test-asset-{index}",
        "title": "Test asset",
        "category": "furniture/chairs",
        "source": "kaykit-furniture",
        "style": "stylized",
        "tags": ["chair"],
        "path": "addons/kaykit_furniture_bits/Assets/gltf/chair_A.gltf",
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

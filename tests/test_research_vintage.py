import copy

import pytest

from asset_library.sources.research_vintage import isolate_car


def scene():
    nodes = [{"name": str(i)} for i in range(47)]
    nodes.extend(
        [
            {"name": "47_Ground"},
            {"name": "Camera"},
            {"name": "vintage-car_root", "children": list(range(49))},
        ]
    )
    return {
        "nodes": nodes,
        "meshes": [{"name": str(i)} for i in range(47)] + [{"name": "47_Ground"}],
        "cameras": [{"type": "perspective"}],
        "scenes": [{"nodes": [49]}],
        "buffers": [{"uri": "vintage_car.bin", "byteLength": 26712032}],
    }


def test_isolate_removes_floor_and_camera_from_active_scene():
    data = isolate_car(scene())
    assert data["nodes"][47]["children"] == list(range(47))
    assert data["scenes"][0]["nodes"] == [47]
    assert len(data["nodes"]) == 48
    assert len(data["meshes"]) == 47
    assert "cameras" not in data


def test_fail_closed_on_external_images_or_changed_scene():
    data = scene()
    data["images"] = [{"uri": "envmap.pfm"}]
    with pytest.raises(ValueError):
        isolate_car(data)
    data = scene()
    data["nodes"][47]["name"] = "different"
    with pytest.raises(ValueError):
        isolate_car(data)
    data = scene()
    data["buffers"] = copy.deepcopy(data["buffers"])
    data["buffers"][0]["uri"] = "../other.bin"
    with pytest.raises(ValueError):
        isolate_car(data)

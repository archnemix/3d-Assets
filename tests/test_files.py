import json

import pytest

from asset_library.files import destination, inventory, safe_relative_path, sha256


@pytest.mark.parametrize(
    "value", ["../secret.png", "/etc/passwd", "a/../../b", "https://example.com/a", "a\\b", ""]
)
def test_rejects_unsafe_dependency_paths(value):
    with pytest.raises(ValueError):
        safe_relative_path(value)


def test_accepts_relative_texture_paths(tmp_path):
    assert safe_relative_path("textures/wood%20diffuse.jpg").name == "wood diffuse.jpg"
    assert (
        destination(tmp_path, safe_relative_path("textures/wood.jpg")).parent
        == tmp_path / "textures"
    )


def test_inventory_excludes_self_referential_manifest(tmp_path):
    (tmp_path / "model").mkdir()
    (tmp_path / "model" / "scene.gltf").write_text("{}")
    (tmp_path / "asset.json").write_text("{}")
    (tmp_path / "SHA256SUMS").write_text("old")
    records = inventory(tmp_path)
    assert [item["path"] for item in records] == ["model/scene.gltf"]
    assert records[0]["sha256"] == sha256(tmp_path / "model" / "scene.gltf")
    assert json.loads((tmp_path / "model" / "scene.gltf").read_text()) == {}

import json
import zipfile

import pytest

from asset_library.files import destination, extract_zip, inventory, safe_relative_path, sha256


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


def test_extract_zip_writes_regular_files(tmp_path):
    archive = tmp_path / "pack.zip"
    with zipfile.ZipFile(archive, "w") as package:
        package.writestr("clothes/test.txt", "cc0")
    target = tmp_path / "extracted"
    result = extract_zip(archive, target)
    assert result == {"files": 1, "bytes": 3}
    assert (target / "clothes" / "test.txt").read_text() == "cc0"


def test_extract_zip_rejects_traversal(tmp_path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as package:
        package.writestr("../escape.txt", "no")
    with pytest.raises(ValueError, match="Unsafe"):
        extract_zip(archive, tmp_path / "extracted")
    assert not (tmp_path / "escape.txt").exists()

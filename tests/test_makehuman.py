"""Human recipes are pinned data; generation itself is exercised by CI Blender."""

import json

import pytest
from jsonschema import validate

from asset_library.config import ROOT, read_json
from asset_library.sources import makehuman


@pytest.mark.parametrize("recipe_id", ["adult-casual-male", "adult-casual-female"])
def test_shipped_recipes_are_valid_and_reference_pack_entries(recipe_id):
    recipe = read_json(ROOT / "config" / "human-recipes" / f"{recipe_id}.json")
    validate(recipe, read_json(ROOT / "schemas" / "human-recipe.schema.json"))
    pack = read_json(ROOT / "research" / "makehuman-system-pack.json")
    entries = {entry["path"] for entry in pack["entries"]}
    assert set(makehuman.selected_paths(recipe)) <= entries
    assert makehuman.recipe_path({"recipe": recipe_id}).name == f"{recipe_id}.json"


def test_recipe_id_must_match_filename(tmp_path, monkeypatch):
    monkeypatch.setattr(makehuman, "ROOT", tmp_path)
    (tmp_path / "config" / "human-recipes").mkdir(parents=True)
    (tmp_path / "schemas").mkdir()
    schema = ROOT / "schemas" / "human-recipe.schema.json"
    (tmp_path / "schemas" / "human-recipe.schema.json").write_text(schema.read_text())
    recipe = read_json(ROOT / "config" / "human-recipes" / "adult-casual-male.json")
    recipe["id"] = "wrong-id"
    (tmp_path / "config" / "human-recipes" / "adult-casual-male.json").write_text(
        json.dumps(recipe)
    )
    with pytest.raises(ValueError, match="does not match"):
        makehuman.recipe_path({"recipe": "adult-casual-male"})


def test_pinned_archive_rejects_checksum_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr(makehuman, "ROOT", tmp_path)

    def fake_download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"not the pinned pack")
        return {"url": url, "bytes": path.stat().st_size, "sha256": "0" * 64}

    monkeypatch.setattr(makehuman, "download", fake_download)
    with pytest.raises(ValueError, match="checksum mismatch"):
        makehuman.pinned_archive("https://files2.makehumancommunity.org/pack.zip", "1" * 64)


def test_preserve_descriptors_copies_only_small_source_records(tmp_path):
    pack = tmp_path / "pack"
    asset = pack / "clothes" / "test"
    asset.mkdir(parents=True)
    (asset / "test.mhclo").write_text("name test\n")
    (asset / "test.mhmat").write_text("diffuseTexture test.png\n")
    (asset / "test.png").write_bytes(b"large texture is embedded by the exporter instead")
    recipe = {
        "skin": "clothes/test/test.mhmat",
        "clothes": ["clothes/test/test.mhclo"],
        "bodyparts": {},
    }
    directory = tmp_path / "candidate"
    records = makehuman.preserve_descriptors(pack, recipe, directory)
    assert records[0]["path"] == "clothes/test/test.mhclo"
    assert (directory / "provenance" / "makehuman" / "clothes" / "test" / "test.mhmat").exists()
    assert not (directory / "provenance" / "makehuman" / "clothes" / "test" / "test.png").exists()

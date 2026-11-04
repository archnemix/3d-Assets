"""Tests for the mechanical-animation retrofit planner."""

import json

from asset_library import animate


def write_asset(tmp_path, identifier, category="tools/storage", **extra):
    root = tmp_path / "assets" / category / identifier
    root.mkdir(parents=True)
    manifest = {"id": identifier, "model": "model/a.glb", **extra}
    (root / "asset.json").write_text(json.dumps(manifest))
    return root


def test_targets_skips_assets_that_already_carry_authored_motion(tmp_path, monkeypatch):
    write_asset(tmp_path, "plain")
    write_asset(tmp_path, "done", animated_model="model/a-animated.glb")
    monkeypatch.setattr(animate, "ROOT", tmp_path)
    found = animate.targets({"batch": "b"})
    assert [json.loads(p.read_text())["id"] for p in found] == ["plain"]


def test_force_reauthors_assets_that_already_have_an_animated_model(tmp_path, monkeypatch):
    write_asset(tmp_path, "done", animated_model="model/a-animated.glb")
    monkeypatch.setattr(animate, "ROOT", tmp_path)
    assert animate.targets({"batch": "b"}) == []
    assert len(animate.targets({"batch": "b", "force": True})) == 1


def test_ids_narrows_the_batch_to_the_named_assets(tmp_path, monkeypatch):
    write_asset(tmp_path, "wanted")
    write_asset(tmp_path, "other")
    monkeypatch.setattr(animate, "ROOT", tmp_path)
    found = animate.targets({"batch": "b", "force": True, "ids": ["wanted"]})
    assert [json.loads(p.read_text())["id"] for p in found] == ["wanted"]
    assert animate.targets({"batch": "b", "force": True, "ids": ["absent"]}) == []


def test_shards_never_exceed_five_workers(tmp_path, monkeypatch):
    for index in range(12):
        write_asset(tmp_path, f"asset-{index}")
    monkeypatch.setattr(animate, "ROOT", tmp_path)
    assert animate.shards({"batch": "b"}) == {"shard": [0, 1, 2, 3, 4]}
    assert animate.shards({"batch": "b", "ids": ["absent"]}) == {"shard": [0]}


def test_no_clip_assets_still_get_their_inventory_refreshed(tmp_path, monkeypatch):
    """The authoring pass writes animations.json even when nothing is animatable.

    Skipping the inventory refresh on that path left untracked files behind and
    broke the catalog gate for every asset the pass looked at.
    """
    root = write_asset(tmp_path, "plain")
    monkeypatch.setattr(animate, "ROOT", tmp_path)
    monkeypatch.setattr(animate.shutil, "which", lambda _: "/usr/bin/blender")

    def fake_author(directory, model, blender):
        (directory / "provenance").mkdir(exist_ok=True)
        (directory / "provenance" / "animations.json").write_text("{}")
        return {"authored": []}

    monkeypatch.setattr(animate, "author_animations", fake_author)
    assert animate.run_shard({"batch": "b"}, 0) == 0
    manifest = json.loads((root / "asset.json").read_text())
    assert "provenance/animations.json" in {f["path"] for f in manifest["files"]}
    assert "animated_model" not in manifest

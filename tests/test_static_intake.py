import json

from asset_library import inspection


def test_static_intake_skips_authored_clips_but_inspects_model(tmp_path, monkeypatch):
    (tmp_path / "model").mkdir()
    (tmp_path / "model" / "model.glb").write_bytes(b"test")
    (tmp_path / "previews").mkdir()
    (tmp_path / "previews" / "geometry.json").write_text("{}")
    (tmp_path / "provenance").mkdir()
    (tmp_path / "provenance" / "gltf-validator.json").write_text(
        json.dumps({"issues": {"numErrors": 0, "numWarnings": 0}})
    )
    monkeypatch.setattr(inspection, "validate_local", lambda _: {"animations": []})
    monkeypatch.setattr(inspection, "extract_textures", lambda *_: [])
    monkeypatch.setattr(inspection.shutil, "which", lambda _: "blender")
    monkeypatch.setattr(inspection, "run", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(inspection, "build", lambda *_args: None)
    monkeypatch.setattr(inspection, "ROOT", tmp_path)
    validator = tmp_path / "node_modules/gltf-validator/index.js"
    validator.parent.mkdir(parents=True)
    validator.write_text("")

    def should_not_author(*_args):
        raise AssertionError("Authored animations must be skipped")

    monkeypatch.setattr(inspection, "author_animations", should_not_author)
    manifest = {"model": "model/model.glb", "skip_authored_animation": True}
    result = inspection.inspect(tmp_path, {"title": "test"}, manifest)
    assert result["validation"]["gltf_errors"] == 0
    assert result["gltf"]["animations"] == []
    assert "authored_animations" not in result
    assert "animated_model" not in result

"""Grab3D packages are accepted only with their own CC0 manifest and license."""

import pytest

from asset_library.sources import grab3d

SOURCE = {
    "download_base": "https://grab3d.com/dl",
    "page": "https://grab3d.com/models",
    "page_sections": {"default": "characters", "vehicles": "vehicles", "weapons": "weapons"},
    "license_page": "https://grab3d.com/license/",
    "creator": "Grab3D",
}
MANIFEST = {
    "slug": "man-base-character-rigged",
    "extras": {"license": "CC0-1.0"},
    "files": {"glb": {"name": "man-base-character-rigged.glb", "bytes": 4}},
    "origin": {"method": "ai-assisted", "ai_content": True},
}
LICENSE = "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"


def test_page_url_uses_the_human_model_page_for_rigged_packages():
    assert (
        grab3d.page_url(SOURCE, "man-base-character-rigged", "characters/humans")
        == "https://grab3d.com/models/characters/man-base-character/"
    )


def test_page_url_follows_the_candidate_category_section():
    assert (
        grab3d.page_url(SOURCE, "muscle-car", "vehicles/cars")
        == "https://grab3d.com/models/vehicles/muscle-car/"
    )
    assert (
        grab3d.page_url(SOURCE, "broadsword", "weapons/melee")
        == "https://grab3d.com/models/weapons/broadsword/"
    )


def test_page_url_falls_back_to_characters_for_unmapped_roots():
    assert (
        grab3d.page_url(SOURCE, "android-rigged", "unmapped/thing")
        == "https://grab3d.com/models/characters/android/"
    )


def test_verify_cc0_requires_both_manifest_and_package_dedication():
    grab3d.verify_cc0(MANIFEST, LICENSE)
    with pytest.raises(ValueError, match="manifest"):
        grab3d.verify_cc0({"extras": {"license": "MIT"}}, LICENSE)
    with pytest.raises(ValueError, match="license"):
        grab3d.verify_cc0(MANIFEST, "All rights reserved")


REPAIR = {
    "repair": "normalize-skin-weights",
    "normalized_vertices": 0,
    "repaired_sha256": "a" * 64,
}


def test_fetch_preserves_license_manifest_and_origin(tmp_path, monkeypatch):
    monkeypatch.setattr(grab3d, "json", lambda url, hosts: MANIFEST)
    monkeypatch.setattr(grab3d, "text", lambda url, hosts: LICENSE)
    monkeypatch.setattr(grab3d, "normalize_skin_weights", lambda path: REPAIR)

    def fake_download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"glb!")
        return {"url": url, "bytes": 4, "sha256": "a" * 64}

    monkeypatch.setattr(grab3d, "download", fake_download)
    result = grab3d.fetch_grab3d(
        SOURCE,
        {"upstream_id": "man-base-character-rigged", "category": "characters/humans"},
        tmp_path,
    )
    assert result["model"] == "model/man-base-character-rigged.glb"
    assert result["license"] == "CC0-1.0"
    assert result["origin"]["ai_content"] is True
    assert (tmp_path / "LICENSE.txt").read_text() == LICENSE
    assert (tmp_path / "provenance" / "grab3d-manifest.json").exists()
    assert (tmp_path / "provenance" / "grab3d-package.json").exists()


def test_fetch_rejects_changed_package_size(tmp_path, monkeypatch):
    monkeypatch.setattr(grab3d, "json", lambda url, hosts: MANIFEST)
    monkeypatch.setattr(grab3d, "text", lambda url, hosts: LICENSE)
    monkeypatch.setattr(grab3d, "normalize_skin_weights", lambda path: REPAIR)

    def fake_download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"changed")
        return {"url": url, "bytes": 7, "sha256": "b" * 64}

    monkeypatch.setattr(grab3d, "download", fake_download)
    with pytest.raises(ValueError, match="size changed"):
        grab3d.fetch_grab3d(
            SOURCE,
            {"upstream_id": "man-base-character-rigged", "category": "characters/humans"},
            tmp_path,
        )


def test_page_url_prefers_a_full_category_override_over_the_root():
    source = {
        **SOURCE,
        "page_sections": {
            **SOURCE["page_sections"],
            "nature": "animals",
            "nature/creatures": "creatures",
        },
    }
    assert (
        grab3d.page_url(source, "crystal-dragon", "nature/creatures")
        == "https://grab3d.com/models/creatures/crystal-dragon/"
    )
    assert (
        grab3d.page_url(source, "lynx", "nature/wildlife")
        == "https://grab3d.com/models/animals/lynx/"
    )


def test_light_variant_is_a_file_key_in_the_base_manifest(tmp_path, monkeypatch):
    """`<slug>-light` is not a package. The light build is files.glb_light."""
    manifest = {
        **MANIFEST,
        "slug": "crystal-dragon",
        "files": {
            "glb": {"name": "crystal-dragon.glb", "bytes": 31},
            "glb_light": {"name": "crystal-dragon-light.glb", "bytes": 4},
        },
    }
    seen = []
    monkeypatch.setattr(grab3d, "json", lambda url, hosts: seen.append(url) or manifest)
    monkeypatch.setattr(grab3d, "text", lambda url, hosts: LICENSE)
    monkeypatch.setattr(grab3d, "normalize_skin_weights", lambda path: REPAIR)

    def fake_download(url, path, hosts):
        seen.append(url)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"glb!")
        return {"url": url, "bytes": 4, "sha256": "a" * 64}

    monkeypatch.setattr(grab3d, "download", fake_download)
    result = grab3d.fetch_grab3d(
        SOURCE,
        {
            "upstream_id": "crystal-dragon",
            "category": "nature/creatures",
            "variant": "light",
        },
        tmp_path,
    )
    assert result["model"] == "model/crystal-dragon-light.glb"
    assert any(u.endswith("/crystal-dragon/manifest.json") for u in seen)
    assert not any("-light/manifest.json" in u for u in seen)


def test_missing_light_build_fails_with_the_key_it_looked_for(tmp_path, monkeypatch):
    import pytest

    monkeypatch.setattr(grab3d, "json", lambda url, hosts: MANIFEST)
    monkeypatch.setattr(grab3d, "text", lambda url, hosts: LICENSE)
    with pytest.raises(ValueError, match="glb_light"):
        grab3d.fetch_grab3d(
            SOURCE,
            {
                "upstream_id": "man-base-character-rigged",
                "category": "characters/humans",
                "variant": "light",
            },
            tmp_path,
        )


def test_spacecraft_use_sci_fi_source_pages():
    source = {**SOURCE, "page_sections": {**SOURCE["page_sections"], "vehicles/spacecraft": "sci-fi"}}
    assert (
        grab3d.page_url(source, "space-capsule", "vehicles/spacecraft")
        == "https://grab3d.com/models/sci-fi/space-capsule/"
    )

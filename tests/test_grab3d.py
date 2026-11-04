"""Grab3D packages are accepted only with their own CC0 manifest and license."""

import pytest

from asset_library.sources import grab3d

SOURCE = {
    "download_base": "https://grab3d.com/dl",
    "page": "https://grab3d.com/models/characters",
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
        grab3d.page_url(SOURCE, "man-base-character-rigged")
        == "https://grab3d.com/models/characters/man-base-character/"
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
    result = grab3d.fetch_grab3d(SOURCE, {"upstream_id": "man-base-character-rigged"}, tmp_path)
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
        grab3d.fetch_grab3d(SOURCE, {"upstream_id": "man-base-character-rigged"}, tmp_path)

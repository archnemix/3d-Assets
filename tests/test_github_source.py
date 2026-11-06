"""Pinned source terms and model paths are verified before intake."""

import pytest

from asset_library.sources import github

SOURCE = {
    "repository": "test/kit",
    "commit": "abc123",
    "license_path": "LICENSE",
    "terms_path": "README.md",
    "creator": "Test Creator",
    "page": "https://github.com/test/kit",
}


def test_pinned_terms_are_preserved_and_model_downloaded(tmp_path, monkeypatch):
    def text(url, hosts):
        return "CC0 1.0 Universal" if url.endswith("LICENSE") else "All kit models are CC0."

    def download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"glb")
        return {"url": url, "sha256": "a" * 64, "bytes": 3}

    monkeypatch.setattr(github, "text", text)
    monkeypatch.setattr(github, "download", download)
    result = github.fetch_github(SOURCE, {"path": "exports/model.glb"}, tmp_path)
    assert result["model"] == "model/model.glb"
    assert "CC0" in (tmp_path / "provenance" / "upstream-terms.md").read_text()
    assert "abc123" in result["license_evidence"]


def test_unverified_terms_and_unsafe_paths_are_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(
        github,
        "text",
        lambda url, hosts: "CC0 1.0 Universal" if url.endswith("LICENSE") else "unknown",
    )
    with pytest.raises(ValueError, match="terms"):
        github.fetch_github(SOURCE, {"path": "exports/model.glb"}, tmp_path)
    monkeypatch.setattr(github, "text", lambda url, hosts: "CC0 1.0 Universal")
    with pytest.raises(ValueError, match="Unsafe"):
        github.fetch_github(SOURCE, {"path": "../model.glb"}, tmp_path)
    with pytest.raises(ValueError, match="GLB or glTF"):
        github.fetch_github(SOURCE, {"path": "exports/readme.txt"}, tmp_path)

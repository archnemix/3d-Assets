"""Release models are bound to a pinned catalog, URL, license, size and hash."""

import json

import pytest

from asset_library.sources import github_release

SOURCE = {
    "repository": "author/studio",
    "commit": "abc123",
    "release_tag": "v1.0.0",
    "license_path": "LICENSE.txt",
    "terms_path": "README.md",
    "catalog_path": "downloads.json",
    "creator": "Author",
}
ENTRY = {
    "id": "Hut",
    "filename": "hut.glb",
    "url": "https://github.com/author/studio/releases/download/v1.0.0/hut.glb",
    "sha256": "a" * 64,
    "bytes": 3,
}


def mock_source(monkeypatch, entry=ENTRY, downloaded_sha="a" * 64):
    def get_text(url, hosts):
        if url.endswith("LICENSE.txt"):
            return "CC0 1.0 Universal"
        if url.endswith("README.md"):
            return "All assets CC0. Attribution is not required."
        return json.dumps({"license": "CC0-1.0", "assets": [entry]})

    def download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"glb")
        return {"sha256": downloaded_sha, "bytes": 3, "url": url}

    monkeypatch.setattr(github_release, "text", get_text)
    monkeypatch.setattr(github_release, "download", download)


def test_release_evidence_and_pinned_model(tmp_path, monkeypatch):
    mock_source(monkeypatch)
    result = github_release.fetch_github_release(SOURCE, {"upstream_id": "Hut"}, tmp_path)
    assert result["model"] == "model/hut.glb"
    assert (tmp_path / "provenance" / "release-catalog.json").is_file()
    assert (tmp_path / "provenance" / "upstream-terms.md").is_file()


def test_release_refuses_url_substitution(tmp_path, monkeypatch):
    mock_source(monkeypatch, {**ENTRY, "url": "https://evil.example/hut.glb"})
    with pytest.raises(ValueError, match="Release URL"):
        github_release.fetch_github_release(SOURCE, {"upstream_id": "Hut"}, tmp_path)


def test_release_rejects_mismatched_hash_and_removes_payload(tmp_path, monkeypatch):
    mock_source(monkeypatch, downloaded_sha="b" * 64)
    with pytest.raises(ValueError, match="checksum"):
        github_release.fetch_github_release(SOURCE, {"upstream_id": "Hut"}, tmp_path)
    assert not (tmp_path / "model" / "hut.glb").exists()

import pytest

from asset_library.sources.oga_submarine import extract_members, fetch_oga_submarine, verify_page


def test_individual_page_verification():
    html = """<p>Submarine (Low poly) STKRudy85 CC0</p>
    <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
    <a href="/sites/default/files/Submarine.7z">Submarine.7z</a>"""
    verify_page(html)
    for altered in [
        html.replace("STKRudy85", "other"),
        html.replace("publicdomain/zero/1.0/", "licenses/by/4.0/"),
        html.replace("Submarine.7z", "other.7z"),
    ]:
        with pytest.raises(ValueError):
            verify_page(altered)


def test_wrong_source_id_and_archive_are_rejected(tmp_path):
    with pytest.raises(ValueError):
        fetch_oga_submarine({}, {"upstream_id": "other"}, tmp_path)
    archive = tmp_path / "evil.7z"
    archive.write_bytes(b"not the pinned archive")
    with pytest.raises(ValueError, match="digest"):
        extract_members(archive, tmp_path / "out")
    assert not (tmp_path / "out").exists()

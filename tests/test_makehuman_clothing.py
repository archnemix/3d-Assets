"""Safety checks for the standalone CC0 garment source."""

from pathlib import Path

import pytest

from asset_library.sources.makehuman_clothing import (
    descriptor_field,
    local_dependency,
    verify_index,
)


def test_index_requires_exact_clothing_row_author_and_cc0():
    page = "<table><tr><td>clothes</td><td></td><td>dress_id</td><td>Artist</td><td>asset repo</td><td>CC0</td></tr></table>"
    assert verify_index(page, "dress_id", "Artist")[-1] == "CC0"
    for text, ident, author in [
        (page.replace("CC0", "CC-BY"), "dress_id", "Artist"),
        (page, "dress", "Artist"),
        (page, "dress_id", "Someone Else"),
    ]:
        with pytest.raises(ValueError):
            verify_index(text, ident, author)


def test_fields_reject_ambiguous_or_missing():
    assert (
        descriptor_field("name Example\nobj_file dress.obj\nverts 0\n", "obj_file") == "dress.obj"
    )
    with pytest.raises(ValueError):
        descriptor_field("obj_file a\nobj_file b\n", "obj_file")
    with pytest.raises(ValueError):
        descriptor_field("name foo\n", "material")


def test_dependency_refuses_escape_and_missing(tmp_path: Path):
    (tmp_path / "texture.png").write_bytes(b"x")
    assert local_dependency(tmp_path, "texture.png") == tmp_path / "texture.png"
    for name in ("../evil.png", "/etc/passwd", "https://evil/texture.png", "missing.png"):
        with pytest.raises(ValueError):
            local_dependency(tmp_path, name)

from zipfile import ZipFile

import pytest

from asset_library.sources.oga_locomotive import extract_glb, verify_page

PAGE = """<h1>Locomotive</h1><span>32kda</span>
<a href="http://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
<p>decided to do it myself. CC0, do whatever you want.</p>
<a href="/sites/default/files/locomotive00.zip">locomotive00.zip</a>"""


def test_original_page_requires_all_evidence():
    verify_page(PAGE)
    with pytest.raises(ValueError):
        verify_page(PAGE.replace("decided to do it myself", "found it online"))
    with pytest.raises(ValueError):
        verify_page(PAGE.replace("creativecommons.org/publicdomain/zero/1.0/", "example.org"))


def test_extract_single_glb_without_extracting_other_archive_paths(tmp_path):
    archive = tmp_path / "x.zip"
    with ZipFile(archive, "w") as z:
        z.writestr("../somewhere/model.glb", b"glb")
        z.writestr("../evil.txt", b"evil")
    target = tmp_path / "model" / "locomotive.glb"
    assert extract_glb(archive, target) == "../somewhere/model.glb"
    assert target.read_bytes() == b"glb"
    assert not (tmp_path.parent / "evil.txt").exists()
    with ZipFile(archive, "a") as z:
        z.writestr("other.glb", b"glb")
    with pytest.raises(ValueError, match="exactly one"):
        extract_glb(archive, target)

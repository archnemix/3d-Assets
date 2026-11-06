import pytest

from asset_library.sources.oga_submersible import verify_page


def test_individual_page_verification():
    html = """<p>Yellow Submersible weirdybeardyman CC0</p>
    <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
    <a href="/sites/default/files/sub2.blend">sub2.blend</a>"""
    verify_page(html)
    for change in [
        html.replace("weirdybeardyman", "other"),
        html.replace("sub2.blend", "other.blend"),
        html.replace("publicdomain/zero/1.0/", "licenses/by/4.0/"),
    ]:
        with pytest.raises(ValueError):
            verify_page(change)

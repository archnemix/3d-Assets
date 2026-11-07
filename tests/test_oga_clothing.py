"""OpenGameArt clothing intake must bind page license and exact archives."""

import pytest

from asset_library.sources.oga_clothing import verify_page


def test_verified_page_requires_creator_cc0_and_selected_archive():
    page = '<h1>Hats / Clothing / Props</h1> Teh_Bucket <a href="http://creativecommons.org/publicdomain/zero/1.0/">CC0</a><a href="/sites/default/files/sweatshirt_e.zip">sweatshirt_e.zip</a>'
    verify_page(page, "sweatshirt_e.zip")
    for html, archive in [
        (page.replace("Teh_Bucket", "Other"), "sweatshirt_e.zip"),
        (page.replace("CC0", "CC-BY"), "sweatshirt_e.zip"),
        (page, "other.zip"),
    ]:
        with pytest.raises(ValueError):
            verify_page(html, archive)

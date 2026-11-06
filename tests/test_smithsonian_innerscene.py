import pytest

from asset_library.sources.smithsonian_innerscene import GLB, ORIGINAL, verify_page


def test_page_requires_explicit_creator_and_specific_cc0():
    page = f'<a href="{GLB}">Download</a><a href="{ORIGINAL}">Original</a> 1903 Wright Flyer Smithsonian Institution (NASM) Public domain (CC0) Added from Smithsonian Open Access under its CC0 dedication'
    verify_page(page)
    for fragment in (ORIGINAL, GLB, "Smithsonian Institution (NASM)", "Public domain (CC0)"):
        with pytest.raises(ValueError):
            verify_page(page.replace(fragment, ""))

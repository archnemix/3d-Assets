import pytest

from asset_library.sources.smithsonian_flyer import verify_page


def test_only_individually_verified_3d_media():
    page = (
        "1903 Wright Flyer CC0 Smithsonian c91467735c6743af872e65107a79beda.glb Objaverse Sketchfab"
    )
    verify_page(page)
    for fragment in (
        "CC0",
        "Smithsonian",
        "c91467735c6743af872e65107a79beda.glb",
        "Objaverse",
    ):
        with pytest.raises(ValueError):
            verify_page(page.replace(fragment, ""))

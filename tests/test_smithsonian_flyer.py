import pytest

from asset_library.sources.smithsonian_flyer import verify_page


def test_only_individually_verified_3d_media():
    page = "1903 Wright Flyer CC0 This media file is in the public domain 1903WrightFlyer-150k-4096_std.glb scale in cm"
    verify_page(page)
    for fragment in (
        "CC0",
        "This media file is in the public domain",
        "1903WrightFlyer-150k-4096_std.glb",
        "scale in cm",
    ):
        with pytest.raises(ValueError):
            verify_page(page.replace(fragment, ""))

import pytest

from asset_library.sources.oga_triplane import fetch_oga_triplane, verify_page


def test_individual_page_verification():
    html = """<p>low poly fokker triplane mujtaba-io CC0</p>
    <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
    <a href="/sites/default/files/fokker-triplane-v2.blend">fokker-triplane-v2.blend</a>"""
    verify_page(html)
    for change in [
        html.replace("mujtaba-io", "other"),
        html.replace("fokker-triplane-v2.blend", "other.blend"),
        html.replace("publicdomain/zero/1.0/", "licenses/by/4.0/"),
    ]:
        with pytest.raises(ValueError):
            verify_page(change)


def test_wrong_source_id_is_rejected_before_network(tmp_path):
    with pytest.raises(ValueError):
        fetch_oga_triplane({}, {"upstream_id": "other"}, tmp_path)

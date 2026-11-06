"""The library contains multiple rights regimes, so failures must remain closed."""

import pytest

from asset_library.sources import innerscene


@pytest.fixture(autouse=True)
def clear_terms_cache():
    innerscene._license_cache.clear()
    yield
    innerscene._license_cache.clear()


def test_invalid_terms_are_not_cached(monkeypatch, tmp_path):
    calls = []

    def fetch(url, hosts):
        calls.append(url)
        return "not a CC0 dedication"

    monkeypatch.setattr(innerscene, "text", fetch)
    source = {"license_page": "https://www.innerscene.com/terms"}
    for _ in range(2):
        with pytest.raises(ValueError, match="terms do not confirm"):
            innerscene.fetch_innerscene(source, {"upstream_id": "test"}, tmp_path)
    assert len(calls) == 2
    assert not innerscene._license_cache


def test_government_or_other_items_are_not_treated_as_original_cc0(monkeypatch, tmp_path):
    monkeypatch.setattr(
        innerscene,
        "text",
        lambda url, hosts: "CC0 1.0 Universal" if url.endswith("terms") else "NASA public domain",
    )
    source = {
        "license_page": "https://www.innerscene.com/terms",
        "page": "https://www.innerscene.com/models",
    }
    with pytest.raises(ValueError, match="does not identify"):
        innerscene.fetch_innerscene(source, {"upstream_id": "test"}, tmp_path)
    assert not (tmp_path / "LICENSE.txt").exists()


def test_allowed_storage_host_is_explicit():
    assert "files.innerscene.com" in innerscene.HOSTS
    assert "example.com" not in innerscene.HOSTS


def test_page_gate_does_not_accept_recommended_models_or_scripts():
    good = "<main>Public domain (CC0) <p>Innerscene - original model</p>Original Innerscene model, released CC0</main>"
    assert innerscene.original_model_page(good)
    assert not innerscene.original_model_page(
        "<main>NASA public domain<h2>More like this</h2>" + good + "</main>"
    )
    assert not innerscene.original_model_page("<script>" + good + "</script>NASA public domain")

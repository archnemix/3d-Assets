"""Resolution fallback keeps quality high without letting one texture set dominate."""

import pytest

from asset_library.sources.polyhaven import package_bytes, select_package


def package(size, includes=()):
    return {
        "url": "https://dl.polyhaven.org/model.gltf",
        "size": size,
        "include": {name: {"size": value} for name, value in includes},
    }


def files():
    return {
        "gltf": {
            "4k": {"gltf": package(1000, [("textures/diff.jpg", 40_000_000)])},
            "2k": {"gltf": package(1000, [("textures/diff.jpg", 6_000_000)])},
            "1k": {"gltf": package(1000, [("textures/diff.jpg", 1_500_000)])},
        }
    }


def test_package_bytes_counts_every_dependency():
    assert package_bytes(package(10, [("a", 20), ("b", 30)])) == 60


def test_preferred_resolution_is_used_when_it_fits():
    resolution, chosen = select_package(files(), "2k", 12 * 1024**2)
    assert resolution == "2k"
    assert package_bytes(chosen) == 6_001_000


def test_oversized_package_falls_back_to_a_smaller_resolution():
    resolution, chosen = select_package(files(), "4k", 12 * 1024**2)
    assert resolution == "2k"
    assert package_bytes(chosen) <= 12 * 1024**2


def test_fallback_stops_at_the_lowest_available_resolution():
    resolution, _ = select_package(files(), "4k", 2 * 1024**2)
    assert resolution == "1k"


def test_nothing_fitting_is_an_error_not_a_silent_empty_asset():
    with pytest.raises(ValueError, match="fits"):
        select_package(files(), "4k", 100)


def test_missing_gltf_format_reports_what_is_available():
    with pytest.raises(ValueError, match="No glTF package at 2k"):
        select_package({"blend": {"2k": {}}}, "2k", 12 * 1024**2)

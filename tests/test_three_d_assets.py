"""3DAssets.dev intake fails closed on rights, provenance and immutable URLs."""

from copy import deepcopy

import pytest

from asset_library.sources.three_d_assets import validate_item

ITEM = {
    "id": "123",
    "slug": "example-car",
    "status": "published",
    "license": {"slug": "cc0-1.0", "attributionRequired": False},
    "contributor": {"username": "3dassets"},
    "aiGenerated": True,
    "cdnUrl": "https://cdn.3dassets.dev/assets/123/v1/model.glb",
    "stats": {"fileSize": 1234},
}


def test_valid_source_metadata():
    validate_item(ITEM, "example-car")


@pytest.mark.parametrize(
    "key,value",
    [
        ("status", "draft"),
        ("license", {"slug": "cc-by-4.0", "attributionRequired": True}),
        ("contributor", {"username": "someone-else"}),
        ("aiGenerated", None),
        ("cdnUrl", "https://other.example/assets/123/v1/model.glb"),
        ("cdnUrl", "https://cdn.3dassets.dev/assets/456/v1/model.glb"),
        ("cdnUrl", "https://cdn.3dassets.dev/assets/123/model.glb"),
        ("stats", {"fileSize": 0}),
    ],
)
def test_refuses_unsafe_metadata(key, value):
    item = deepcopy(ITEM)
    item[key] = value
    with pytest.raises(ValueError):
        validate_item(item, "example-car")


def test_rejects_mismatched_or_unsafe_slug():
    with pytest.raises(ValueError):
        validate_item(ITEM, "../other")
    with pytest.raises(ValueError):
        validate_item(ITEM, "other")


def test_fetch_records_item_rights_origin_and_checks_model_size(monkeypatch, tmp_path):
    from asset_library.sources import three_d_assets

    item = {**deepcopy(ITEM), "contributor": {"username": "3dassets", "name": "3D Assets"}}
    item["stats"]["fileSize"] = 4
    monkeypatch.setattr(three_d_assets, "json", lambda url, hosts: {"data": item})
    monkeypatch.setattr(
        three_d_assets,
        "text",
        lambda url, hosts: "sale of the models themselves"
        if "3dassets.dev" in url
        else "CC0 1.0 Universal",
    )

    def fake_download(url, path, hosts):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"glb!")
        return {"url": url, "bytes": 4, "sha256": "a" * 64}

    monkeypatch.setattr(three_d_assets, "download", fake_download)
    result = three_d_assets.fetch_three_d_assets(
        {"api": "https://3dassets.dev/api/v1", "license_page": "https://3dassets.dev/license"},
        {"upstream_id": "example-car"},
        tmp_path,
    )
    assert result["origin"]["ai_content"] is True
    assert result["license_evidence"].endswith("/example-car")
    assert (tmp_path / "provenance" / "3dassets-metadata.json").is_file()
    assert (tmp_path / "LICENSE.txt").is_file()

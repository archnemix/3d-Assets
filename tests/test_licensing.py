"""The license audit must fail loudly, not quietly bless an asset."""

import pytest

from asset_library import licensing
from asset_library.files import inventory, write_checksums, write_json

TERMS = {
    "schema_version": 1,
    "checked_on": "2026-11-04",
    "policy": {
        "accepted_spdx": ["CC0-1.0"],
        "attribution_required": False,
        "commercial_use": True,
        "standalone_use": True,
        "redistribution_allowed": True,
        "public_display": True,
    },
    "universal_caveats": ["CC0 does not waive trademark or patent rights held by the affirmer."],
    "providers": {
        "tester": {
            "name": "Tester",
            "spdx": "CC0-1.0",
            "status": "verified",
            "free_of_charge": True,
            "terms_url": "https://example.com/terms",
            "evidence_url": "https://example.com/license.txt",
            "resale_as_is": {
                "permitted": True,
                "explicit": True,
                "note": "The provider explicitly allows reselling the models themselves.",
            },
            "asset_notes": [],
            "caveats": ["Only the provider's own rights are waived by this dedication."],
        }
    },
}


@pytest.fixture
def asset(tmp_path, monkeypatch):
    monkeypatch.setattr(licensing, "ROOT", tmp_path)
    monkeypatch.setattr(licensing, "REPORT", tmp_path / "reports" / "license-audit.json")
    monkeypatch.setattr(licensing, "PAGE", tmp_path / "docs" / "licenses.md")
    directory = tmp_path / "assets" / "furniture" / "chairs" / "test-chair"
    (directory / "model").mkdir(parents=True)
    (directory / "textures").mkdir()
    (directory / "model" / "scene.glb").write_bytes(b"glTF-placeholder")
    (directory / "textures" / "diffuse.jpg").write_bytes(b"texture")
    (directory / "LICENSE.txt").write_text(
        "This work is dedicated under CC0 1.0 Universal.\n", encoding="utf-8"
    )
    manifest = {
        "id": "test-chair",
        "title": "Test chair",
        "category": "furniture/chairs",
        "textures": [{"path": "textures/diffuse.jpg"}],
        "source": {
            "provider": "tester",
            "creator": "Tester",
            "license": "CC0-1.0",
            "license_evidence": "https://example.com/license.txt",
            "source_url": "https://example.com/test-chair",
        },
        "license": {
            "spdx": "CC0-1.0",
            "attribution_required": False,
            "commercial_use": True,
            "redistribution_allowed": True,
            "evidence": "https://example.com/license.txt",
        },
        "review": {"approved": True},
    }
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return directory, manifest


def save(directory, manifest):
    write_json(directory / "asset.json", manifest)


def test_audit_passes_a_complete_cc0_asset(asset, monkeypatch):
    directory, manifest = asset
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    assert report["totals"] == {
        "assets": 1,
        "passed": 1,
        "failed": 0,
        "by_provider": {"tester": 1},
    }
    assert report["assets"][0]["failed_checks"] == []
    licensing.verify()
    assert "Not required" in licensing.PAGE.read_text(encoding="utf-8")


def test_audit_flags_attribution_requirement(asset, monkeypatch):
    directory, manifest = asset
    manifest["license"]["attribution_required"] = True
    save(directory, manifest)
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    assert report["assets"][0]["pass"] is False
    assert "no_attribution_required" in report["assets"][0]["failed_checks"]
    with pytest.raises(ValueError, match="failing the license policy"):
        licensing.verify()


def test_audit_flags_non_cc0_metadata(asset, monkeypatch):
    directory, manifest = asset
    manifest["license"]["spdx"] = "CC-BY-4.0"
    save(directory, manifest)
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    assert "cc0_spdx" in report["assets"][0]["failed_checks"]


def test_audit_flags_edited_license_text(asset, monkeypatch):
    directory, manifest = asset
    (directory / "LICENSE.txt").write_text("All rights reserved.\n", encoding="utf-8")
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    failed = report["assets"][0]["failed_checks"]
    assert "cc0_text_present" in failed
    assert "license_file_checksummed" in failed


def test_audit_flags_missing_texture(asset, monkeypatch):
    directory, manifest = asset
    (directory / "textures" / "diffuse.jpg").unlink()
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    assert "textures_included" in report["assets"][0]["failed_checks"]


def test_audit_flags_trademark_warning(asset, monkeypatch):
    directory, manifest = asset
    provenance = directory / "provenance"
    provenance.mkdir()
    write_json(provenance / "api-info.json", {"tmwarn": "Brand name visible on the model."})
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    report = licensing.build()
    assert "no_trademark_warning" in report["assets"][0]["failed_checks"]


def test_audit_rejects_provider_without_recorded_terms(asset, monkeypatch):
    directory, manifest = asset
    manifest["source"]["provider"] = "unknown-mirror"
    save(directory, manifest)
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    with pytest.raises(ValueError, match="No recorded license terms"):
        licensing.build()


def test_audit_detects_stale_report(asset, monkeypatch):
    directory, manifest = asset
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    licensing.build()
    stale = licensing.read_json(licensing.REPORT)
    stale["totals"]["passed"] = 99
    write_json(licensing.REPORT, stale)
    with pytest.raises(ValueError, match="license-audit.json is stale"):
        licensing.verify()


def test_audit_detects_stale_page(asset, monkeypatch):
    directory, manifest = asset
    monkeypatch.setattr(licensing, "terms", lambda: TERMS)
    licensing.build()
    licensing.PAGE.write_text("hand-edited\n", encoding="utf-8")
    with pytest.raises(ValueError, match="licenses.md is stale"):
        licensing.verify()


def test_recorded_terms_match_the_schema():
    assert licensing.terms()["policy"]["attribution_required"] is False

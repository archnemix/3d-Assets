"""Audit every approved asset against the recorded CC0 terms of its source.

The license question is answered per asset, from files on disk plus the pinned
evidence recorded at acquisition time. A provider label alone is never enough.
"""

from collections import Counter

from jsonschema import FormatChecker, validate

from .config import ROOT, read_json
from .files import sha256, write_json
from .license_report import render

CC0_MARKERS = ("cc0", "creativecommons.org/publicdomain/zero", "public domain")
REPORT = ROOT / "reports" / "license-audit.json"
PAGE = ROOT / "docs" / "licenses.md"


def terms() -> dict:
    document = read_json(ROOT / "config" / "license-terms.json")
    schema = read_json(ROOT / "schemas" / "license-terms.schema.json")
    validate(document, schema, format_checker=FormatChecker())
    return document


def license_text(directory) -> str:
    path = directory / "LICENSE.txt"
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def texture_files_present(directory, manifest: dict) -> bool:
    return all((directory / texture["path"]).is_file() for texture in manifest["textures"])


def trademark_flag(directory) -> bool:
    """Poly Haven marks a few assets with a trademark warning; none may be approved."""
    path = directory / "provenance" / "api-info.json"
    return bool(read_json(path).get("tmwarn")) if path.is_file() else False


def checks(directory, manifest: dict, provider: dict) -> dict[str, bool]:
    license_block = manifest["license"]
    source = manifest["source"]
    text = license_text(directory).lower()
    recorded = {item["path"]: item["sha256"] for item in manifest["files"]}
    return {
        "free_of_charge": provider["free_of_charge"] is True,
        "cc0_spdx": license_block["spdx"] == "CC0-1.0" and source["license"] == "CC0-1.0",
        "cc0_text_present": any(marker in text for marker in CC0_MARKERS),
        "license_file_checksummed": recorded.get("LICENSE.txt") == sha256(directory / "LICENSE.txt")
        if (directory / "LICENSE.txt").is_file()
        else False,
        "no_attribution_required": license_block["attribution_required"] is False,
        "commercial_use_allowed": license_block["commercial_use"] is True,
        "redistribution_allowed": license_block["redistribution_allowed"] is True,
        "evidence_recorded": license_block.get("evidence", "").startswith("https://")
        and license_block["evidence"] == source["license_evidence"],
        "source_terms_verified": provider["status"] == "verified",
        "standalone_resale_permitted": provider["resale_as_is"]["permitted"] is True,
        "textures_included": texture_files_present(directory, manifest),
        "no_trademark_warning": not trademark_flag(directory),
        "visually_approved": manifest["review"]["approved"] is True,
    }


def record(directory, manifest: dict, provider: dict) -> dict:
    results = checks(directory, manifest, provider)
    base = directory.relative_to(ROOT).as_posix()
    return {
        "id": manifest["id"],
        "title": manifest["title"],
        "category": manifest["category"],
        "creator": manifest["source"]["creator"],
        "provider": manifest["source"]["provider"],
        "spdx": manifest["license"]["spdx"],
        "directory": base,
        "source_url": manifest["source"]["source_url"],
        "license_evidence": manifest["license"]["evidence"],
        "license_file": f"{base}/LICENSE.txt",
        "license_file_sha256": sha256(directory / "LICENSE.txt"),
        "ai_assisted": bool(manifest["source"].get("origin", {}).get("ai_content")),
        "notes": provider["asset_notes"],
        "checks": results,
        "failed_checks": sorted(name for name, ok in results.items() if not ok),
        "pass": all(results.values()),
    }


def collect(terms_document: dict) -> list[dict]:
    records = []
    for path in sorted((ROOT / "assets").rglob("asset.json")):
        manifest = read_json(path)
        name = manifest["source"]["provider"]
        provider = terms_document["providers"].get(name)
        if provider is None:
            raise ValueError(f"No recorded license terms for provider {name!r}: {path}")
        records.append(record(path.parent, manifest, provider))
    return records


def document(terms_document: dict, records: list[dict]) -> dict:
    used = sorted({item["provider"] for item in records})
    return {
        "schema_version": 1,
        "checked_on": terms_document["checked_on"],
        "scope": "approved assets under assets/ only",
        "policy": terms_document["policy"],
        "totals": {
            "assets": len(records),
            "passed": sum(item["pass"] for item in records),
            "failed": sum(not item["pass"] for item in records),
            "by_provider": dict(sorted(Counter(item["provider"] for item in records).items())),
        },
        "providers": {name: terms_document["providers"][name] for name in used},
        "universal_caveats": terms_document["universal_caveats"],
        "assets": records,
    }


def build() -> dict:
    recorded = terms()
    report = document(recorded, collect(recorded))
    write_json(REPORT, report)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(render(report), encoding="utf-8")
    totals = report["totals"]
    print(f"License audit: {totals['passed']}/{totals['assets']} assets pass every check")
    return report


def verify() -> None:
    recorded = terms()
    expected = document(recorded, collect(recorded))
    if not REPORT.is_file() or read_json(REPORT) != expected:
        raise ValueError("reports/license-audit.json is stale; run license-audit")
    if not PAGE.is_file() or PAGE.read_text(encoding="utf-8") != render(expected):
        raise ValueError("docs/licenses.md is stale; run license-audit")
    failed = [item["id"] for item in expected["assets"] if not item["pass"]]
    if failed:
        raise ValueError(f"Assets failing the license policy: {', '.join(failed)}")
    print(f"Verified license terms for {expected['totals']['assets']} approved assets")

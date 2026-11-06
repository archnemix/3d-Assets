"""Withdraw a published asset and record why, without keeping its payload.

Retirement is deliberately destructive to the model files. When an author asks
that their work not be redistributed, honouring that means the files leave the
repository, not that they move to another folder.
"""

import shutil
from pathlib import Path

from jsonschema import FormatChecker, validate

from .config import ROOT, read_json
from .files import write_json
from .inspection import validate_inventory

# Schemas are code, not library data: resolve them beside the package so the
# retirement logic can be pointed at a different asset root.
SCHEMA = Path(__file__).resolve().parents[2] / "schemas" / "retirement.schema.json"


def load(path: Path) -> dict:
    document = read_json(path)
    validate(document, read_json(SCHEMA), format_checker=FormatChecker())
    seen = set()
    for entry in document["assets"]:
        if entry["id"] in seen:
            raise ValueError(f"Duplicate retirement: {entry['id']}")
        seen.add(entry["id"])
    return document


def locate(asset_id: str) -> Path:
    matches = sorted((ROOT / "assets").glob(f"*/*/{asset_id}/asset.json"))
    if not matches:
        raise ValueError(f"No published asset with id {asset_id!r}")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous asset id {asset_id!r}: {len(matches)} folders")
    return matches[0].parent


def apply(path: Path) -> dict:
    document = load(path)
    prepared = []
    for entry in document["assets"]:
        directory = locate(entry["id"])
        manifest = read_json(directory / "asset.json")
        validate_inventory(directory, manifest)
        if manifest["source"]["provider"] != entry["provider"]:
            raise ValueError(f"{entry['id']}: provider does not match the published asset")
        evidence = ROOT / "reports" / "retired" / entry["id"]
        if evidence.exists():
            raise ValueError(f"Refusing to overwrite retirement record: {evidence}")
        prepared.append((directory, manifest, entry, evidence))
    records = []
    for directory, manifest, entry, evidence in prepared:
        record = {
            "id": manifest["id"],
            "title": manifest["title"],
            "category": manifest["category"],
            "creator": manifest["source"]["creator"],
            "provider": manifest["source"]["provider"],
            "source_url": manifest["source"]["source_url"],
            "license": manifest["license"]["spdx"],
            "retired_on": document["retired_on"],
            "decided_by": document["decided_by"],
            "reason": entry["reason"],
            "payload_removed": True,
            "removed_files": len(manifest["files"]),
            "removed_bytes": sum(item["bytes"] for item in manifest["files"]),
            "model_sha256": next(
                (item["sha256"] for item in manifest["files"] if item["path"] == manifest["model"]),
                None,
            ),
        }
        evidence.mkdir(parents=True, exist_ok=True)
        write_json(evidence / "retirement.json", record)
        shutil.rmtree(directory)
        records.append(record)
        print(f"retired: {record['id']} ({record['removed_bytes']:,} bytes removed)")
    summary = {
        "retired_on": document["retired_on"],
        "policy": document["policy"],
        "assets": records,
        "totals": {
            "assets": len(records),
            "bytes_removed": sum(item["removed_bytes"] for item in records),
        },
    }
    write_json(ROOT / "reports" / "retired" / f"{document['retired_on']}-summary.json", summary)
    return summary

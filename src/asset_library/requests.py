"""Validate an intake request and split it into at most five disjoint shards."""

import json
from pathlib import Path

from jsonschema import validate

from .config import ROOT, asset_directory, categories, read_json, sources


def load_request(path: Path) -> dict:
    value = read_json(path)
    validate(value, read_json(ROOT / "schemas" / "request.schema.json"))
    seen = set()
    registered = sources()
    for candidate in value["candidates"]:
        if candidate["id"] in seen:
            raise ValueError(f"Duplicate candidate: {candidate['id']}")
        seen.add(candidate["id"])
        asset_directory(ROOT / "assets", candidate["category"], candidate["id"])
        if candidate["source"] not in registered and candidate["source"] != "makehuman":
            raise ValueError(f"Unregistered source: {candidate['source']}")
        if (ROOT / "assets" / candidate["category"] / candidate["id"]).exists():
            raise ValueError(f"Already published; use a new revision request: {candidate['id']}")
    return value


def shards(path: Path, count: int = 5) -> list[dict]:
    if not 1 <= count <= 5:
        raise ValueError("The workflow supports one to five parallel workers")
    request = load_request(path)
    groups = [[] for _ in range(min(count, len(request["candidates"])))]
    for index, candidate in enumerate(request["candidates"]):
        groups[index % len(groups)].append(candidate)
    return [
        {
            "shard": index,
            "batch_id": request["batch_id"],
            "candidates": json.dumps(group, separators=(",", ":")),
        }
        for index, group in enumerate(groups)
    ]


def describe(path: Path) -> None:
    request = load_request(path)
    counts = {category: 0 for category in categories()}
    for candidate in request["candidates"]:
        counts[candidate["category"]] += 1
    print(f"{request['batch_id']}: {len(request['candidates'])} candidates")
    for category, count in counts.items():
        if count:
            print(f"  {category}: {count}")

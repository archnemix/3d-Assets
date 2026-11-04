"""Refresh quarantine evidence without downloading or approving assets again."""

import json
import traceback
from datetime import UTC, datetime
from pathlib import Path

from jsonschema import FormatChecker, validate

from .config import ROOT, read_json, require_slug
from .files import write_json
from .inspection import reinspect
from .requests import partition


def load_request(path: Path) -> dict:
    document = read_json(path)
    validate(
        document,
        read_json(ROOT / "schemas" / "refresh.schema.json"),
        format_checker=FormatChecker(),
    )
    batch = require_slug(document["batch"])
    for value in document["candidates"]:
        directory = Path(value)
        require_slug(directory.name)
        if directory.parent != Path("quarantine") / batch:
            raise ValueError(f"Refresh path is outside the requested batch: {value}")
        manifest = read_json(ROOT / directory / "asset.json")
        if manifest["batch"] != batch or manifest["id"] != directory.name:
            raise ValueError(f"Candidate identity does not match its path: {value}")
        if manifest["review"]["status"] not in {"awaiting-visual-review", "intake-failed"}:
            raise ValueError(f"Candidate is not awaiting inspection: {value}")
    return document


def shards(path: Path, count: int = 5) -> list[dict]:
    document = load_request(path)
    return [
        {"shard": index, "candidates": json.dumps(group)}
        for index, group in enumerate(partition(document["candidates"], count))
    ]


def describe(path: Path) -> None:
    document = load_request(path)
    print(f"{document['batch']}: refresh {len(document['candidates'])} candidates")
    print(document["reason"])


def run_shard(path: Path, shard: int) -> int:
    document = load_request(path)
    assignment = shards(path)[shard]
    results = []
    for value in json.loads(assignment["candidates"]):
        print(f"[shard {shard}] refreshing {value}", flush=True)
        try:
            reinspect(ROOT / value)
            result = {"path": value, "status": "awaiting-visual-review"}
        except Exception as error:
            log = ROOT / value / "logs" / "refresh-failure.txt"
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_text(traceback.format_exc(), encoding="utf-8")
            result = {"path": value, "status": "refresh-failed", "error": str(error)}
        print(f"[shard {shard}] {result['status']}: {value}", flush=True)
        results.append(result)
    write_json(
        ROOT / "reports" / "refresh" / document["batch"] / f"shard-{shard}.json",
        {
            "batch": document["batch"],
            "shard": shard,
            "reason": document["reason"],
            "results": results,
            "completed_at": datetime.now(UTC).isoformat(),
        },
    )
    return int(any(result["status"] == "refresh-failed" for result in results))

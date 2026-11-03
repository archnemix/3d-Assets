"""Acquire one shard into quarantine. Acquisition success is not approval."""

import shutil
import traceback
from datetime import UTC, datetime

from .config import ROOT, sources
from .files import write_json
from .inspection import inspect
from .sources import fetch


def candidate(candidate: dict, batch: str) -> dict:
    directory = ROOT / "quarantine" / batch / candidate["id"]
    if directory.exists():
        raise ValueError(f"Quarantine destination already exists: {directory}")
    directory.mkdir(parents=True)
    started = datetime.now(UTC).isoformat()
    manifest = {
        "schema_version": 1,
        "id": candidate["id"],
        "title": candidate["title"],
        "category": candidate["category"],
        "style": candidate["style"],
        "tags": candidate["tags"],
        "batch": batch,
        "acquired_at": started,
        "review": {"status": "pending", "approved": False},
    }
    try:
        if candidate["source"] == "makehuman":
            from .sources.makehuman import fetch_makehuman

            provenance = fetch_makehuman(candidate, directory)
        else:
            provenance = fetch(sources()[candidate["source"]], candidate, directory)
        manifest["source"] = {"provider": candidate["source"], **provenance}
        manifest["license"] = {
            "spdx": "CC0-1.0",
            "attribution_required": False,
            "commercial_use": True,
            "redistribution_allowed": True,
            "evidence": provenance["license_evidence"],
        }
        manifest["model"] = provenance["model"]
        inspect(directory, candidate, manifest)
        manifest["review"]["status"] = "awaiting-visual-review"
        write_json(directory / "asset.json", manifest)
        return {
            "id": candidate["id"],
            "status": manifest["review"]["status"],
            "path": str(directory.relative_to(ROOT)),
        }
    except Exception as error:
        manifest["review"]["status"] = "intake-failed"
        manifest["error"] = str(error)
        (directory / "logs").mkdir(exist_ok=True)
        (directory / "logs" / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        write_json(directory / "asset.json", manifest)
        return {
            "id": candidate["id"],
            "status": "intake-failed",
            "error": str(error),
            "path": str(directory.relative_to(ROOT)),
        }


def run_shard(batch: str, candidates: list[dict], shard: int) -> int:
    results = [candidate(item, batch) for item in candidates]
    report = {
        "batch": batch,
        "shard": shard,
        "results": results,
        "completed_at": datetime.now(UTC).isoformat(),
    }
    write_json(ROOT / "reports" / "intake" / batch / f"shard-{shard}.json", report)
    return int(any(item["status"] == "intake-failed" for item in results))


def discard_failed(batch: str) -> None:
    """Keep failed-candidate evidence, but never retain unidentified partial downloads."""
    for path in (ROOT / "quarantine" / batch).glob("*/asset.json"):
        import json

        manifest = json.loads(path.read_text())
        if manifest["review"]["status"] == "intake-failed":
            for child in path.parent.iterdir():
                if child.name in {"asset.json", "logs"}:
                    continue
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()

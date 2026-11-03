"""Load repository configuration without coupling adapters to CLI code."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def sources() -> dict:
    return read_json(ROOT / "config" / "sources.json")


def categories() -> dict[str, str]:
    return read_json(ROOT / "config" / "categories.json")


def require_slug(value: str) -> str:
    if not SLUG.fullmatch(value):
        raise ValueError(f"Expected a lowercase hyphenated slug, got {value!r}")
    return value


def asset_directory(base: Path, category: str, asset_id: str) -> Path:
    if category not in categories():
        raise ValueError(f"Unknown category: {category}")
    require_slug(asset_id)
    return base / category / asset_id

"""List unrepresented Poly Haven models from its public API for manual selection."""

import json
from pathlib import Path

from asset_library.config import ROOT, read_json
from asset_library.http import json as get_json
from asset_library.sources.polyhaven import HOSTS


def main():
    source = read_json(ROOT / "config" / "sources.json")["polyhaven"]
    headers = {"User-Agent": source["user_agent"], "Referer": source["user_agent"]}
    upstream = get_json(f"{source['api']}/assets?type=models", HOSTS, headers)
    existing = set()
    for path in (ROOT / "assets").rglob("asset.json"):
        asset = read_json(path)
        if asset["source"]["provider"] == "polyhaven":
            existing.add(asset["source"]["source_id"].lower())
    result = []
    for identifier, asset in upstream.items():
        if identifier.lower() in existing or asset.get("tmwarn"):
            continue
        result.append(
            {
                "id": identifier,
                "name": asset.get("name", identifier),
                "category": asset.get("category", ""),
                "categories": asset.get("categories", []),
                "authors": list(asset.get("authors", {})),
                "tags": asset.get("tags", []),
                "description": asset.get("description", ""),
                "polycount": asset.get("polycount"),
            }
        )
    result.sort(key=lambda item: (item["category"], item["name"]))
    output = Path("reports/research/polyhaven-unrepresented.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Found {len(result)} unrepresented models with no API trademark warning")
    print("This is a discovery list, not license or visual approval.")


if __name__ == "__main__":
    main()

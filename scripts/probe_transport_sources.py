"""Probe conversion of two unapproved, item-specific sources; publish no assets."""

import json
import tempfile
from pathlib import Path

from asset_library.sources.oga_submarine import fetch_oga_submarine
from asset_library.sources.oga_triplane import fetch_oga_triplane

probes = [
    ("fokker-triplane", fetch_oga_triplane, "low-poly-fokker-triplane"),
    ("submarine", fetch_oga_submarine, "submarine-low-poly"),
]
results = []
with tempfile.TemporaryDirectory(prefix="vehicle-conversion-probe-") as temp:
    for name, adapter, upstream in probes:
        directory = Path(temp) / name
        directory.mkdir()
        try:
            result = adapter({}, {"upstream_id": upstream}, directory)
            results.append({"id": name, "status": "converted-not-reviewed", "source": result})
        except Exception as error:
            log = directory / "logs/convert.log"
            results.append(
                {
                    "id": name,
                    "status": "failed-not-approved",
                    "error": str(error),
                    "conversion_log_tail": log.read_text(encoding="utf-8", errors="replace")[
                        -12000:
                    ]
                    if log.exists()
                    else "",
                }
            )
output = Path("reports/research/vehicle-conversion-probe.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({"probes": results}, indent=2) + "\n", encoding="utf-8")

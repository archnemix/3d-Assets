"""Inspect official CC0 clothing packs without publishing any candidates."""

import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

PACKS = ("dress01", "pants01", "shirts01", "skirts01", "suits01")
ROOT = "https://files2.makehumancommunity.org/asset_packs"


def main():
    result = {}
    for pack in PACKS:
        url = f"{ROOT}/{pack}/{pack}_cc0.zip"
        path = Path("/tmp") / f"{pack}_cc0.zip"
        req = urllib.request.Request(url, headers={"User-Agent": "3d-Assets-Curator/0.1"})
        digest = hashlib.sha256()
        size = 0
        with urllib.request.urlopen(req, timeout=120) as r, path.open("wb") as output:
            while block := r.read(1024 * 1024):
                size += len(block)
                if size > 200 * 1024**2:
                    raise ValueError("Archive too large")
                digest.update(block)
                output.write(block)
        entries, descriptors = [], {}
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                entries.append({"path": info.filename, "bytes": info.file_size})
                if (
                    info.filename.lower().endswith((".mhmat", ".mhclo", ".json"))
                    and info.file_size < 100_000
                ):
                    try:
                        content = z.read(info).decode("utf-8")
                    except UnicodeDecodeError:
                        continue
                    # Descriptors may contain thousands of vertex mappings. Keep headers only.
                    if info.filename.lower().endswith(".mhclo"):
                        content = content.split("\nverts\n", 1)[0]
                    descriptors[info.filename] = content
        result[pack] = {
            "url": url,
            "sha256": digest.hexdigest(),
            "bytes": size,
            "entries": entries,
            "descriptors": descriptors,
        }
        print(pack, size, digest.hexdigest(), len(entries), flush=True)
    Path("research/clothing-packs.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )


if __name__ == "__main__":
    main()

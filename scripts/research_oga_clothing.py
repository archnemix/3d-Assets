"""Record bounded archive contents for two CC0 OpenGameArt garment leads."""

import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

URLS = {
    name: "https://opengameart.org/sites/default/files/" + name
    for name in ("cargo_pants_e.zip", "sweatshirt_e.zip")
}


def main():
    result = {}
    for name, url in URLS.items():
        request = urllib.request.Request(url, headers={"User-Agent": "3d-Assets-Curator/0.1"})
        output = Path("/tmp") / name
        digest = hashlib.sha256()
        size = 0
        with urllib.request.urlopen(request, timeout=120) as stream, output.open("wb") as file:
            while block := stream.read(1024 * 1024):
                size += len(block)
                if size > 50 * 1024**2:
                    raise ValueError("Archive too large")
                digest.update(block)
                file.write(block)
        entries = []
        with zipfile.ZipFile(output) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                item = {"path": info.filename, "bytes": info.file_size}
                if info.file_size < 50_000 and info.filename.lower().endswith(
                    (".txt", ".mtl", ".json", ".md")
                ):
                    item["text"] = archive.read(info).decode("utf-8", errors="replace")
                entries.append(item)
        result[name] = {
            "url": url,
            "bytes": size,
            "sha256": digest.hexdigest(),
            "entries": entries,
            "source": "https://opengameart.org/content/hats-clothing-props",
            "creator": "Teh_Bucket",
            "license": "CC0 (as indexed on source page; inspect embedded dependencies)",
        }
        print(name, size, digest.hexdigest(), len(entries), flush=True)
    path = Path("reports/research/oga-clothing-archives.json")
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()

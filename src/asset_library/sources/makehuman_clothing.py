"""Acquire named, indexed CC0 garments from immutable MakeHuman community packs."""

import json
import re
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image

from asset_library.config import ROOT, read_json
from asset_library.files import destination, safe_relative_path, sha256, write_json
from asset_library.http import text
from asset_library.inspection import run
from asset_library.sources.makehuman import extracted, pinned_archive

HOSTS = {"static.makehumancommunity.org"}


class PackIndex(HTMLParser):
    """Capture only visible per-row identity, creator, and license evidence."""

    def __init__(self):
        super().__init__()
        self.in_row = False
        self.cells = None
        self.cell = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row, self.cells = True, []
        elif tag in ("td", "th") and self.in_row:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.cells.append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.in_row:
            self.rows.append(self.cells)
            self.in_row = False


def verify_index(html: str, asset_id: str, author: str) -> list[str]:
    parser = PackIndex()
    parser.feed(html)
    matches = [row for row in parser.rows if asset_id in row]
    if (
        len(matches) != 1
        or author not in matches[0]
        or "CC0" not in matches[0]
        or "clothes" not in matches[0]
    ):
        raise ValueError(f"Missing or changed CC0 clothing index row for {asset_id}")
    return matches[0]


def descriptor_field(contents: str, key: str, required=True) -> str | None:
    matches = [
        line.split(None, 1)[1].strip()
        for line in contents.splitlines()
        if line.strip().startswith(key + " ")
    ]
    if len(matches) > 1 or (required and not matches):
        raise ValueError(f"Missing or ambiguous descriptor field: {key}")
    return matches[0] if matches else None


def verify_descriptor_license(header: str) -> None:
    """Fail closed when the packaged garment explicitly names a non-CC0 license."""
    for line in header.splitlines():
        match = re.match(r"\s*#\s*license\s+(.+)", line, re.IGNORECASE)
        if match and not re.match(r"CC0(?:\b|[- ])", match.group(1), re.IGNORECASE):
            raise ValueError("Garment descriptor conflicts with the CC0 pack index")


def local_dependency(folder: Path, name: str) -> Path:
    path = destination(folder, safe_relative_path(name))
    if not path.is_file():
        raise ValueError(f"Missing garment dependency: {name}")
    return path


def fetch_makehuman_clothing(source: dict, candidate: dict, directory: Path) -> dict:
    upstream = candidate["upstream_id"]
    if upstream not in source["garments"]:
        raise ValueError("Garment is not in the reviewed source allowlist")
    item = source["garments"][upstream]
    pack_name = item["pack"]
    if not re.fullmatch(r"[a-z0-9_-]+", upstream):
        raise ValueError("Invalid garment identity")
    evidence = read_json(ROOT / "research" / "clothing-packs.json")[pack_name]
    index_url = f"https://static.makehumancommunity.org/assets/assetpacks/{pack_name}.html"
    row = verify_index(text(index_url, HOSTS), upstream, item["author"])
    archive, download_record = pinned_archive(
        evidence["url"], evidence["sha256"], evidence["bytes"]
    )
    pack = extracted(archive, evidence["sha256"], f"clothing-{pack_name}")
    folder = destination(pack, safe_relative_path(f"clothes/{upstream}"))
    descriptor = local_dependency(folder, upstream + ".mhclo")
    mhclo = descriptor.read_text(encoding="utf-8")
    # Mapping records can be enormous; fields occur before the verts section.
    header = mhclo.split("\nverts", 1)[0]
    verify_descriptor_license(header)
    obj = local_dependency(folder, descriptor_field(header, "obj_file"))
    mat = local_dependency(folder, descriptor_field(header, "material"))
    material = mat.read_text(encoding="utf-8")
    diffuse = local_dependency(mat.parent, descriptor_field(material, "diffuseTexture"))
    normal_name = descriptor_field(material, "normalmapTexture", required=False)
    normal = local_dependency(mat.parent, normal_name) if normal_name else None
    with Image.open(diffuse) as im:
        has_alpha = "A" in im.getbands() and im.getchannel("A").getextrema()[0] < 255
        size = list(im.size)
    provenance = directory / "provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    shutil.copy2(descriptor, provenance / "source.mhclo")
    shutil.copy2(mat, provenance / "source.mhmat")
    source_evidence = {
        "index_url": index_url,
        "index_row": row,
        "pack": pack_name,
        "archive": download_record,
        "original_obj": obj.relative_to(pack).as_posix(),
        "original_obj_sha256": sha256(obj),
        "diffuse": diffuse.relative_to(pack).as_posix(),
        "diffuse_sha256": sha256(diffuse),
        "diffuse_size": size,
        "alpha": has_alpha,
        "normal": normal.relative_to(pack).as_posix() if normal else None,
        "normal_sha256": sha256(normal) if normal else None,
        "conversion_limitations": "Diffuse and declared normal maps are exported; legacy specular, bump, AO and material parameters are not reproduced.",
    }
    write_json(provenance / "clothing-source.json", source_evidence)
    (directory / "LICENSE.txt").write_text(
        text(
            "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt",
            {"creativecommons.org"},
        ),
        encoding="utf-8",
    )
    model = directory / "model" / "garment.glb"
    model.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="clothing-") as tmp:
        clean_obj = Path(tmp) / "garment.obj"
        # Suppress OBJ's material-file references, then build the material from the verified mhmat.
        clean_obj.write_text(
            "\n".join(
                line
                for line in obj.read_text(encoding="utf-8").splitlines()
                if not line.lstrip().lower().startswith("mtllib ")
            )
            + "\n",
            encoding="utf-8",
        )
        args = {
            "obj": str(clean_obj),
            "diffuse": str(diffuse),
            "normal": str(normal) if normal else None,
            "alpha": has_alpha,
            "output": str(model.resolve()),
        }
        args_file = Path(tmp) / "args.json"
        args_file.write_text(json.dumps(args), encoding="utf-8")
        run(
            [
                "blender",
                "--background",
                "--factory-startup",
                "--disable-autoexec",
                "--python-exit-code",
                "1",
                "--python",
                str(ROOT / "rendering/convert_makehuman_clothing.py"),
                "--",
                str(args_file),
            ],
            directory / "logs" / "convert.log",
            timeout=300,
        )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": item["author"],
        "license": "CC0-1.0",
        "license_evidence": index_url,
        "source_url": index_url,
        "source_id": upstream,
        "revision": evidence["sha256"],
        "downloads": [download_record],
    }

"""Filesystem operations shared by acquisition and catalog publication."""

import hashlib
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        temporary = Path(tmp.name)
    os.replace(temporary, path)


def safe_relative_path(value: str) -> Path:
    decoded = unquote(value)
    path = Path(decoded)
    if path.is_absolute() or ".." in path.parts or "\\" in decoded:
        raise ValueError(f"Unsafe asset dependency path: {value!r}")
    if urlparse(decoded).scheme or decoded.startswith("//"):
        raise ValueError(f"Remote asset dependencies are not allowed: {value!r}")
    if not path.parts:
        raise ValueError("Empty asset dependency path")
    return path


def destination(root: Path, relative: Path) -> Path:
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes asset directory: {relative}")
    return target


def inventory(root: Path) -> list[dict]:
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in {"asset.json", "SHA256SUMS"}:
            continue
        relative = path.relative_to(root).as_posix()
        folder = path.parent.relative_to(root).parts
        role = folder[0] if folder else "documentation"
        if path.name.startswith("LICENSE"):
            role = "license"
        records.append(
            {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path), "role": role}
        )
    return records


def write_checksums(root: Path, records: list[dict]) -> None:
    lines = [f"{item['sha256']}  {item['path']}" for item in records]
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")

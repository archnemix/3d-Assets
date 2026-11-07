"""glTF dependency checks and lossless extraction of embedded texture images."""

import json
import struct
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

from .files import destination, safe_relative_path


def dependencies(document: dict) -> set[str]:
    paths = set()
    for item in document.get("buffers", []) + document.get("images", []):
        if "uri" in item and not item["uri"].startswith("data:"):
            paths.add(item["uri"])
    return paths


def read_model(path: Path) -> tuple[dict, bytes | None]:
    data = path.read_bytes()
    if path.suffix.lower() == ".glb":
        magic, version, length = struct.unpack_from("<4sII", data)
        if magic != b"glTF" or version != 2 or length != len(data):
            raise ValueError(f"Invalid GLB header: {path}")
        document = None
        binary = None
        offset = 12
        while offset < len(data):
            size, kind = struct.unpack_from("<I4s", data, offset)
            offset += 8
            chunk = data[offset : offset + size]
            if len(chunk) != size:
                raise ValueError("Truncated GLB chunk")
            if kind == b"JSON":
                document = json.loads(chunk)
            elif kind == b"BIN\x00":
                binary = chunk
            offset += size
        if document is None:
            raise ValueError("GLB has no JSON chunk")
        return document, binary
    return json.loads(data), None


def validate_local(path: Path) -> dict:
    document, binary = read_model(path)
    if not document.get("meshes"):
        raise ValueError("Model contains no meshes")
    missing = []
    for uri in dependencies(document):
        target = destination(path.parent, safe_relative_path(uri))
        if not target.is_file():
            missing.append(uri)
    if missing:
        raise ValueError(f"Missing glTF dependencies: {missing}")
    for buffer in document.get("buffers", []):
        if "uri" not in buffer and binary is None:
            raise ValueError("GLB buffer has no binary chunk")
        if "uri" not in buffer and len(binary) < buffer["byteLength"]:
            raise ValueError("GLB binary buffer is truncated")
    return {
        "format": path.suffix.lstrip("."),
        "meshes": len(document["meshes"]),
        "materials": len(document.get("materials", [])),
        "images": len(document.get("images", [])),
        "skins": len(document.get("skins", [])),
        "animations": sorted(
            {a.get("name", f"animation-{i}") for i, a in enumerate(document.get("animations", []))}
        ),
        "extensions": document.get("extensionsUsed", []),
        "missing_dependencies": [],
    }


def extract_textures(model: Path, texture_root: Path) -> list[dict]:
    """Copy image bytes, never recompress normal or color maps.

    GLB files remain self-contained. Their sidecar images are convenience copies;
    the manifest identifies them as such rather than pretending they are linked.
    """
    document, binary = read_model(model)
    buffers = [binary]
    for buffer in document.get("buffers", []):
        if "uri" in buffer:
            if buffer["uri"].startswith("data:"):
                raise ValueError("Embedded data-URI buffers must be decoded before extraction")
            buffers.append((model.parent / safe_relative_path(buffer["uri"])).read_bytes())
        elif binary is None:
            raise ValueError("Missing GLB binary chunk")
    result = []
    for index, image in enumerate(document.get("images", [])):
        name = image.get("name") or f"texture-{index:02d}"
        extension = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(
            image.get("mimeType"), ".png"
        )
        if "uri" in image and not image["uri"].startswith("data:"):
            source = model.parent / safe_relative_path(image["uri"])
            relative = safe_relative_path(image["uri"])
            payload = source.read_bytes()
            linked = True
        else:
            view = document["bufferViews"][image["bufferView"]]
            start = view.get("byteOffset", 0)
            payload = buffers[view.get("buffer", 0)][start : start + view["byteLength"]]
            stem = Path(name).name.replace(" ", "-")
            relative = Path(f"{stem}{extension}")
            linked = False
        if linked:
            # Preserve the original glTF layout; do not store a second copy of every PBR map.
            target = source
            recorded_path = target.relative_to(texture_root.parent).as_posix()
        else:
            target = destination(texture_root, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            recorded_path = target.relative_to(texture_root.parent).as_posix()
        with Image.open(target) as pixels:
            dimensions = list(pixels.size)
            pixels.verify()
        result.append(
            {
                "path": recorded_path,
                "dimensions": dimensions,
                "embedded_in_glb": not linked,
                "linked_sidecar": linked,
                "name": unquote(name),
            }
        )
    return result


def embedded_image_bytes(model: Path, index: int) -> bytes:
    """Return a self-contained GLB image exactly as stored, without re-encoding."""
    document, binary = read_model(model)
    if binary is None or not isinstance(index, int) or index < 0:
        raise ValueError("Invalid embedded image index or missing GLB binary")
    images = document.get("images", [])
    if index >= len(images) or "bufferView" not in images[index]:
        raise ValueError("Image is not embedded in a GLB buffer view")
    view = document["bufferViews"][images[index]["bufferView"]]
    if view.get("buffer", 0) != 0:
        raise ValueError("Embedded image is not in the GLB binary buffer")
    start, length = view.get("byteOffset", 0), view["byteLength"]
    if start < 0 or length <= 0 or start + length > len(binary):
        raise ValueError("Invalid image buffer range")
    return binary[start : start + length]


def compact_embedded_textures(directory: Path, manifest: dict) -> None:
    """Avoid storing a second copy of images already embedded in the GLB.

    Retain an index and checksum for lossless extraction and independent auditing.
    External image dependencies are never removed.
    """
    import hashlib

    model = directory / manifest["model"]
    for index, texture in enumerate(manifest["textures"]):
        if texture.get("embedded_in_glb") and not texture.get("linked_sidecar"):
            sidecar = directory / texture["path"]
            data = embedded_image_bytes(model, index)
            if sidecar.read_bytes() != data:
                raise ValueError("Embedded image does not match its extracted sidecar")
            texture.update(
                path=manifest["model"],
                embedded_image_index=index,
                embedded_sha256=hashlib.sha256(data).hexdigest(),
            )
            sidecar.unlink()

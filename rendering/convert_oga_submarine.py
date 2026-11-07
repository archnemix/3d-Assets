"""Convert the pinned submarine scene, allowing only its archived image files."""

import sys
from pathlib import Path

import bpy

args = sys.argv[sys.argv.index("--") + 1 :]
target, source_dir = args
allowed = {"chrome.jpg": "Chrome.jpg", "sub.jpg": "sub.jpg"}
for image in bpy.data.images:
    if image.source == "FILE" and image.filepath and not image.packed_file:
        name = image.filepath.replace("\\", "/").rsplit("/", 1)[-1].lower()
        if name not in allowed:
            raise ValueError(f"Unexpected image dependency: {image.name}: {image.filepath}")
        image.filepath = str(Path(source_dir) / allowed[name])
        image.reload()
        image.pack()
for obj in list(bpy.data.objects):
    if obj.type in {"CAMERA", "LIGHT"}:
        bpy.data.objects.remove(obj, do_unlink=True)
if not any(obj.type == "MESH" for obj in bpy.context.scene.objects):
    raise ValueError("Source scene has no mesh objects")
bpy.ops.export_scene.gltf(filepath=target, export_format="GLB", export_animations=False)

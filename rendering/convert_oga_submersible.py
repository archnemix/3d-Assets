"""Convert an item-specific trusted-rights Blender source with autoexec disabled."""

import sys

import bpy

# Refuse unbundled image dependencies: no unlicensed local files or silent missing textures.
for image in bpy.data.images:
    if image.source == "FILE" and image.filepath and not image.packed_file:
        raise ValueError(f"Unpacked image dependency: {image.name}: {image.filepath}")

# Scene lights and cameras are not part of the vehicle.
for obj in list(bpy.data.objects):
    if obj.type in {"CAMERA", "LIGHT"}:
        bpy.data.objects.remove(obj, do_unlink=True)
if not any(obj.type == "MESH" for obj in bpy.context.scene.objects):
    raise ValueError("Source scene has no mesh objects")
target = sys.argv[sys.argv.index("--") + 1]
bpy.ops.export_scene.gltf(filepath=target, export_format="GLB", export_animations=False)

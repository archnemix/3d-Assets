"""Convert the individually reviewed Fokker triplane with autoexec disabled."""

import sys

import bpy

# This exact unbundled file is an author's modeling reference, not a redistributable
# texture. Drop it only if its users are image-empty reference objects. Never
# silently discard an image used by materials, modifiers, worlds or other data.
for image in list(bpy.data.images):
    if image.source == "FILE" and image.filepath and not image.packed_file:
        name = image.filepath.replace("\\", "/").rsplit("/", 1)[-1].lower()
        if name != "fokker-dri.jpg":
            raise ValueError(f"Unpacked image dependency: {image.name}: {image.filepath}")
        for obj in list(bpy.data.objects):
            if obj.type == "EMPTY" and obj.data == image:
                bpy.data.objects.remove(obj, do_unlink=True)
        if image.users:
            raise ValueError(f"Reference image still has non-empty users: {image.name}")
        bpy.data.images.remove(image)

for obj in list(bpy.data.objects):
    if obj.type in {"CAMERA", "LIGHT"}:
        bpy.data.objects.remove(obj, do_unlink=True)
if not any(obj.type == "MESH" for obj in bpy.context.scene.objects):
    raise ValueError("Source scene has no mesh objects")
target = sys.argv[sys.argv.index("--") + 1]
bpy.ops.export_scene.gltf(filepath=target, export_format="GLB", export_animations=False)

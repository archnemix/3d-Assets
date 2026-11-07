"""Convert a single known garment mesh, resolving only its pinned texture."""

import sys
from pathlib import Path

import bpy

output, image_path, object_name = sys.argv[sys.argv.index("--") + 1 :]
if bpy.data.libraries:
    raise ValueError("Linked external Blender libraries are not allowed")
obj = bpy.data.objects.get(object_name)
if obj is None or obj.type != "MESH" or not obj.data.uv_layers:
    raise ValueError("Expected UV-mapped garment mesh missing")
allowed_image = Path(image_path).name
used = set()
for material in obj.data.materials:
    if material is None or not material.use_nodes:
        raise ValueError("Unexpected garment material")
    for node in material.node_tree.nodes:
        if node.bl_idname == "ShaderNodeTexImage" and node.image:
            image = node.image
            if image.name != allowed_image or image.source != "FILE":
                raise ValueError("Unexpected garment image reference")
            image.filepath = str(Path(image_path).resolve())
            image.reload()
            image.pack()
            used.add(image.name)
if used != {allowed_image}:
    raise ValueError("Expected texture not used by garment material")
for modifier in list(obj.modifiers):
    if modifier.type != "ARMATURE":
        raise ValueError(f"Unexpected modifier: {modifier.type}")
    obj.modifiers.remove(modifier)
world = obj.matrix_world.copy()
obj.parent = None
obj.matrix_world = world
bpy.ops.object.select_all(action="DESELECT")
obj.hide_render = False
obj.hide_set(False)
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(
    filepath=output, export_format="GLB", use_selection=True, export_animations=False
)

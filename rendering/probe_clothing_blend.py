"""Read basic object/material dependencies from a quarantined Blender garment file."""

import json
import sys

import bpy

output = sys.argv[sys.argv.index("--") + 1]
objects = []
for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    objects.append(
        {
            "name": obj.name,
            "vertices": len(obj.data.vertices),
            "polygons": len(obj.data.polygons),
            "materials": [m.name if m else None for m in obj.data.materials],
            "modifiers": [{"type": mod.type, "name": mod.name} for mod in obj.modifiers],
            "hidden": obj.hide_render,
            "uv_layers": [uv.name for uv in obj.data.uv_layers],
        }
    )
images = [
    {
        "name": image.name,
        "filepath": image.filepath,
        "packed": bool(image.packed_file),
        "source": image.source,
        "dimensions": list(image.size),
    }
    for image in bpy.data.images
]
materials = []
for mat in bpy.data.materials:
    nodes = []
    if mat.use_nodes:
        for node in mat.node_tree.nodes:
            nodes.append(
                {
                    "name": node.name,
                    "type": node.bl_idname,
                    "image": node.image.name
                    if node.bl_idname == "ShaderNodeTexImage" and node.image
                    else None,
                }
            )
    materials.append({"name": mat.name, "use_nodes": mat.use_nodes, "nodes": nodes})
with open(output, "w", encoding="utf-8") as file:
    json.dump(
        {
            "objects": objects,
            "images": images,
            "materials": materials,
            "libraries": [lib.filepath for lib in bpy.data.libraries],
        },
        file,
        indent=2,
    )

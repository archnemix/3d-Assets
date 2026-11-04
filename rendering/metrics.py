"""Geometry measurements; these are evidence, not an automatic beauty score."""

import json
import math
import sys
from pathlib import Path

import bpy
from scene import visible_meshes


def collect(output: str) -> None:
    all_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    meshes = visible_meshes(all_meshes)
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    triangles = 0
    vertices = 0
    zero_area = 0
    unweighted = 0
    no_uv = 0
    for obj in meshes:
        evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        vertices += len(mesh.vertices)
        zero_area += sum(triangle.area < 1e-12 for triangle in mesh.loop_triangles)
        no_uv += int(not mesh.uv_layers)
        if obj.vertex_groups and any(mod.type == "ARMATURE" for mod in obj.modifiers):
            unweighted += sum(not vertex.groups for vertex in mesh.vertices)
        evaluated.to_mesh_clear()
    images = []
    for image in bpy.data.images:
        if image.source in {"FILE", "GENERATED"} and image.name not in {
            "Render Result",
            "Viewer Node",
        }:
            images.append(
                {
                    "name": image.name,
                    "dimensions": list(image.size),
                    "packed": bool(image.packed_file),
                    "filepath": image.filepath,
                }
            )
    report = {
        "blender_version": bpy.app.version_string,
        "mesh_objects": len(meshes),
        "hidden_mesh_objects": len(all_meshes) - len(meshes),
        "vertices": vertices,
        "triangles": triangles,
        "material_slots": sum(len(obj.material_slots) for obj in meshes),
        "meshes_without_uv": no_uv,
        "zero_area_triangles": zero_area,
        "unweighted_skinned_vertices": unweighted,
        "armatures": [{"name": obj.name, "bones": len(obj.data.bones)} for obj in armatures],
        "actions": sorted(action.name for action in bpy.data.actions),
        "images": images,
        "finite_mesh_coordinates": all(
            math.isfinite(component)
            for obj in meshes
            for vertex in obj.data.vertices
            for component in vertex.co
        ),
    }
    Path(output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    collect(sys.argv[sys.argv.index("--") + 1])

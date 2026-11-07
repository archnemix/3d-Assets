"""Convert a single MakeHuman OBJ to a static GLB with its declared texture maps."""

import json
import sys

import bpy

args = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.wm.obj_import(filepath=args["obj"], forward_axis="NEGATIVE_Z", up_axis="Y")
objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
if not objects or not any(len(obj.data.uv_layers) for obj in objects):
    raise ValueError("No UV-mapped garment mesh was imported")
mat = bpy.data.materials.new("Garment")
mat.use_nodes = True
nodes, links = mat.node_tree.nodes, mat.node_tree.links
shader = nodes.get("Principled BSDF")
shader.inputs["Roughness"].default_value = 0.8
diffuse = nodes.new("ShaderNodeTexImage")
diffuse.image = bpy.data.images.load(args["diffuse"], check_existing=False)
links.new(diffuse.outputs["Color"], shader.inputs["Base Color"])
if args["alpha"]:
    mat.blend_method = "BLEND"
    links.new(diffuse.outputs["Alpha"], shader.inputs["Alpha"])
if args["normal"]:
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(args["normal"], check_existing=False)
    texture.image.colorspace_settings.name = "Non-Color"
    normal = nodes.new("ShaderNodeNormalMap")
    links.new(texture.outputs["Color"], normal.inputs["Color"])
    links.new(normal.outputs["Normal"], shader.inputs["Normal"])
for obj in objects:
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for polygon in obj.data.polygons:
        polygon.material_index = 0
bpy.ops.export_scene.gltf(filepath=args["output"], export_format="GLB", export_animations=False)

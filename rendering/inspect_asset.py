"""Blender entry point: eight azimuths, top/bottom, clay and triangle wireframe.

Run with Blender --background --python inspect_asset.py -- MODEL OUTPUT_DIR.
The source file is never overwritten. Diagnostic materials exist only in memory.
"""

import json
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).parent))
from mathutils import Vector
from metrics import collect  # noqa: E402
from scene import (  # noqa: E402
    add_studio_lights,
    bounds,
    camera_view,
    fit_camera,
    import_model,
    reset_scene,
    world_points,
)


def neutral_material(name: str, color: tuple) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Roughness"].default_value = 0.78
    return material


def wire_material() -> bpy.types.Material:
    material = neutral_material("Diagnostic triangles", (0.55, 0.6, 0.65, 1))
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    shader = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")
    wire = nodes.new("ShaderNodeWireframe")
    wire.use_pixel_size = True
    wire.inputs["Size"].default_value = 0.8
    dark = nodes.new("ShaderNodeBsdfDiffuse")
    dark.inputs["Color"].default_value = (0.015, 0.025, 0.035, 1)
    mix = nodes.new("ShaderNodeMixShader")
    links.new(wire.outputs[0], mix.inputs[0])
    links.new(shader.outputs[0], mix.inputs[1])
    links.new(dark.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    return material


def portrait_views(objects, low, high, points, directory) -> list[str]:
    """Render close-up head shots for humanoid characters.

    The standard 640px full-body orbit reduces a head to roughly fifty pixels,
    which is not enough to judge facial detail such as scars, eye shading or
    skin texture. For rigged humanoids we add two 1024px portraits so those
    details can actually be reviewed.
    """
    height = high.z - low.z
    width = max(high.x - low.x, high.y - low.y)
    skinned = any(
        obj.find_armature() is not None
        or any(modifier.type == "ARMATURE" for modifier in obj.modifiers)
        for obj in objects
        if obj.type == "MESH"
    )
    if height <= 0 or not skinned or height < width * 1.4:
        return []
    head_low = low.z + height * 0.80
    head_points = [point for point in points if point.z >= head_low]
    if len(head_points) < 24:
        return []
    head_center = Vector(
        (
            sum(point.x for point in head_points) / len(head_points),
            sum(point.y for point in head_points) / len(head_points),
            sum(point.z for point in head_points) / len(head_points),
        )
    )
    head_radius = max((point - head_center).length for point in head_points)
    scene = bpy.context.scene
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    names = []
    for name, azimuth in (("portrait-front", 0), ("portrait-three-quarter", 40)):
        camera_view(name, head_center, head_radius, azimuth, 4)
        fit_camera(scene.camera, head_points, margin=1.25)
        scene.render.filepath = str(directory / f"{name}.jpg")
        bpy.ops.render.render(write_still=True)
        names.append(name)
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    return names


def main(model: str, output: str) -> None:
    directory = Path(output)
    directory.mkdir(parents=True, exist_ok=True)
    reset_scene()
    objects = import_model(model)
    low, high, radius = bounds(objects)
    center = (low + high) / 2
    points = world_points(objects)
    add_studio_lights(center, radius)
    collect(str(directory / "geometry.json"))
    views = [(f"orbit-{index:02d}", index * 45, 18) for index in range(8)]
    views += [("top", 0, 89.5), ("bottom", 0, -89.5), ("clay", 35, 18)]
    for name, azimuth, elevation in views:
        bpy.context.view_layer.material_override = (
            neutral_material("Clay inspection", (0.55, 0.6, 0.65, 1)) if name == "clay" else None
        )
        camera_view(name, center, radius, azimuth, elevation)
        fit_camera(bpy.context.scene.camera, points)
        bpy.context.scene.render.filepath = str(directory / f"{name}.jpg")
        bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.material_override = wire_material()
    camera_view("wireframe", center, radius, 35, 18)
    fit_camera(bpy.context.scene.camera, points)
    bpy.context.scene.render.filepath = str(directory / "wireframe.jpg")
    bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.material_override = None
    extra = portrait_views(objects, low, high, points, directory)
    (directory / "views.json").write_text(
        json.dumps(
            {
                "front_convention": "Orbit 00 looks toward glTF +Z; engine front may differ.",
                "orbit_elevation_degrees": 18,
                "orbit_step_degrees": 45,
                "views": [view[0] for view in views] + ["wireframe"] + extra,
                "portrait_views": extra,
                "render_engine": "Cycles",
                "samples": 24,
                "note": "Inspection renders, not a replacement for testing in the target engine.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    arguments = sys.argv[sys.argv.index("--") + 1 :]
    main(*arguments)

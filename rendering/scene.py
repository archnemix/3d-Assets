"""Consistent studio setup for inspecting downloaded assets in Blender."""

import math

import bpy
from mathutils import Vector


def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 6
    scene.cycles.transparent_max_bounces = 12
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    world = bpy.data.worlds.new("Inspection studio")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.65, 0.7, 0.8, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
    scene.world = world


def import_model(path: str) -> list:
    before = set(bpy.data.objects)
    if path.lower().endswith(".blend"):
        with bpy.data.libraries.load(path, link=False) as (source, target):
            target.objects = source.objects
        for obj in target.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    else:
        bpy.ops.import_scene.gltf(filepath=path)
    objects = [obj for obj in bpy.data.objects if obj not in before]
    meshes = [obj for obj in objects if obj.type == "MESH"]
    if not meshes:
        raise RuntimeError("Importer produced no mesh objects")
    for armature in [obj for obj in objects if obj.type == "ARMATURE"]:
        armature.data.pose_position = "REST"
        if armature.animation_data:
            armature.animation_data_clear()
    bpy.context.view_layer.update()
    return objects


def bounds(objects: list) -> tuple[Vector, Vector, float]:
    points = [
        obj.matrix_world @ Vector(corner)
        for obj in objects
        if obj.type == "MESH"
        for corner in obj.bound_box
    ]
    if not points:
        raise RuntimeError("Asset has no world-space bounds")
    low = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
    high = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
    radius = max((high - low).length / 2, 0.001)
    if not all(math.isfinite(value) for value in [*low, *high, radius]):
        raise RuntimeError("Asset has invalid coordinates")
    return low, high, radius


def add_studio_lights(center: Vector, radius: float) -> None:
    for name, offset, power, size in [
        ("Key", (-3, -4, 5), 650, 4),
        ("Fill", (4, -1, 2), 400, 3),
        ("Rim", (0, 4, 4), 750, 3),
    ]:
        data = bpy.data.lights.new(name, "AREA")
        data.energy = power * radius * radius
        data.shape = "DISK"
        data.size = size * radius
        obj = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(obj)
        obj.location = center + Vector(offset) * radius
        obj.rotation_euler = (center - obj.location).to_track_quat("-Z", "Y").to_euler()


def camera_view(
    name: str, center: Vector, radius: float, azimuth: float, elevation: float = 18
) -> None:
    scene = bpy.context.scene
    camera = bpy.data.objects.get("Inspection camera")
    if camera is None:
        data = bpy.data.cameras.new("Inspection camera")
        camera = bpy.data.objects.new("Inspection camera", data)
        bpy.context.collection.objects.link(camera)
        scene.camera = camera
    azimuth = math.radians(azimuth)
    elevation = math.radians(elevation)
    offset = Vector(
        (
            math.sin(azimuth) * math.cos(elevation),
            -math.cos(azimuth) * math.cos(elevation),
            math.sin(elevation),
        )
    )
    camera.location = center + offset * radius * 4
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = radius * 2.35
    camera.data.clip_start = radius / 100
    camera.data.clip_end = radius * 100

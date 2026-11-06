"""Render additional interior evidence for the quarantined ModKit outpost.

This is a non-destructive inspection: roof objects are hidden only for the cutaway,
then restored for two approximate eye-level views. The source GLB is never saved.
"""

import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene import import_model, reset_scene  # noqa: E402


def main():
    root = Path(__file__).resolve().parents[1]
    model = (
        root
        / "quarantine/modkit-industrial-01/modkit-industrial-outpost/model/ModKit_Industrial_Outpost.glb"
    )
    output = root / "reports/interior/modkit-industrial-outpost"
    output.mkdir(parents=True, exist_ok=True)
    reset_scene()
    objects = import_model(str(model))
    scene = bpy.context.scene
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.cycles.samples = 32
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7
    data = bpy.data.cameras.new("Interior inspection camera")
    camera = bpy.data.objects.new("Interior inspection camera", data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera
    data.clip_start = 0.03
    data.clip_end = 200

    def light(name, location, energy, size):
        lamp = bpy.data.lights.new(name, "AREA")
        lamp.energy = energy
        lamp.size = size
        obj = bpy.data.objects.new(name, lamp)
        bpy.context.collection.objects.link(obj)
        obj.location = location
        obj.rotation_euler = (Vector((6, 4, 0)) - obj.location).to_track_quat("-Z", "Y").to_euler()

    light("Large overhead light", (6, 4, 16), 3500, 15)
    light("Interior fill", (6, 4, 2.7), 400, 3)
    roofs = [obj for obj in objects if obj.name.startswith(("SM_Roof_", "SM_Ceiling_"))]
    if not roofs:
        raise RuntimeError("Could not identify roof objects for cutaway")

    def render(name, location, target, orthographic=False):
        camera.location = Vector(location)
        camera.rotation_euler = (
            (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
        )
        data.type = "ORTHO" if orthographic else "PERSP"
        data.ortho_scale = 18
        data.lens = 20
        scene.render.filepath = str(output / f"{name}.jpg")
        bpy.ops.render.render(write_still=True)

    for obj in roofs:
        obj.hide_render = True
    render("cutaway", (17, -6, 19), (6, 4, 1), orthographic=True)
    for obj in roofs:
        obj.hide_render = False
    render("interior-front", (3.5, 2.0, 1.65), (8, 5, 1.4))
    render("interior-rear", (9, 6, 1.65), (2, 2, 1.4))
    (output / "inspection.json").write_text(
        json.dumps(
            {
                "model": str(model.relative_to(root)),
                "model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
                "hidden_for_cutaway": [obj.name for obj in roofs],
                "note": "Roof and ceiling hidden for cutaway only; eye-level images use all original geometry. No walkability, collision or animation test was performed.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

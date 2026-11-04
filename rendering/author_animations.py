"""Author mechanical animation clips for models whose moving parts are separate nodes.

Many props and vehicles ship as a static assembly even though the parts that
should move are already separate objects with their origins on the correct
pivot. This script adds real glTF animation clips for those parts and writes a
self-contained animated GLB beside the untouched original.

Nothing here guesses a skeleton. Every rule below is keyed to an explicit
upstream contract (Grab3D documents "rotate around local X to roll" and "rotate
around local Z to articulate") or to an unambiguous hinge part name. Each
authored clip is rendered as a three-frame verification strip so a human can
confirm the motion before the asset is approved.

Run with Blender --background --python author_animations.py -- MODEL OUT_DIR
"""

import json
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).parent))
from scene import (  # noqa: E402
    add_studio_lights,
    bounds,
    camera_view,
    fit_camera,
    import_model,
    reset_scene,
    world_points,
)

FPS = 30

# clip name -> (part matcher, rotation axis, degrees, frames)
# Axes are local. Grab3D's vehicle manifests state the roll and steer axes
# explicitly; hinge parts rotate about the axis their name implies.
ROTATION_CLIPS = [
    ("wheel_roll", lambda n: "wheel" in n, "X", 360.0, 60),
    ("steer", lambda n: "wheel_f" in n or n.endswith("_fl") or n.endswith("_fr"), "Z", 32.0, 45),
    ("trailer_swing", lambda n: n.endswith("_trailer"), "Z", 35.0, 60),
    ("door_open", lambda n: n.endswith("_door"), "Z", -100.0, 60),
    ("lid_open", lambda n: n.endswith("_lid"), "X", -105.0, 60),
    ("crank_turn", lambda n: n.endswith("_crank"), "X", 360.0, 60),
    ("gear_spin", lambda n: "_cog" in n, "X", 360.0, 60),
    ("reel_spin", lambda n: "_spool" in n and "arm" not in n and "holder" not in n, "X", 360.0, 60),
]


def matching(objects, predicate):
    return [o for o in objects if o.type == "MESH" and predicate(o.name.lower())]


def build_clip(name, parts, axis, degrees, frames):
    """Keyframe parts from rest to the target angle and back, as one NLA track."""
    index = "XYZ".index(axis)
    for obj in parts:
        obj.animation_data_create()
        action = bpy.data.actions.new(f"{name}:{obj.name}")
        obj.animation_data.action = action
        obj.rotation_mode = "XYZ"
        base = list(obj.rotation_euler)
        for frame, factor in ((1, 0.0), (frames, 1.0)):
            obj.rotation_euler = base
            obj.rotation_euler[index] = base[index] + math.radians(degrees) * factor
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        for curve in action.fcurves:
            for point in curve.keyframe_points:
                point.interpolation = "LINEAR"
        track = obj.animation_data.nla_tracks.new()
        track.name = name
        track.strips.new(name, 1, action)
        obj.animation_data.action = None
        obj.rotation_euler = base
    return {
        "name": name,
        "parts": [o.name for o in parts],
        "axis": axis,
        "degrees": degrees,
        "frames": frames,
        "fps": FPS,
    }


def verification_strip(clips, directory, objects):
    """Render frame 1 / middle / last of each clip so the motion can be reviewed."""
    low, high, radius = bounds(objects)
    center = (low + high) / 2
    add_studio_lights(center, radius)
    points = world_points(objects)
    scene = bpy.context.scene
    scene.render.resolution_x = 320
    scene.render.resolution_y = 320
    scene.render.fps = FPS
    strips = []
    for clip in clips:
        scene.animation_data_create()
        track = scene.animation_data.nla_tracks.new()
        track.name = f"verify_{clip['name']}"
        frames = clip["frames"]
        names = []
        for label, frame in (("a", 1), ("b", frames // 2), ("c", frames)):
            scene.frame_set(frame)
            camera_view(f"verify_{clip['name']}_{label}", center, radius, 35, 16)
            fit_camera(scene.camera, points)
            path = directory / f"anim-{clip['name']}-{label}.jpg"
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            names.append(path.name)
        scene.animation_data.nla_tracks.remove(track)
        strips.append({"clip": clip["name"], "frames": names})
    scene.frame_set(1)
    return strips


def main(model: str, output: str) -> None:
    directory = Path(output)
    directory.mkdir(parents=True, exist_ok=True)
    reset_scene()
    objects = import_model(model)
    clips = []
    for name, predicate, axis, degrees, frames in ROTATION_CLIPS:
        parts = matching(objects, predicate)
        if parts:
            clips.append(build_clip(name, parts, axis, degrees, frames))
    report = {
        "source_model": Path(model).name,
        "authored": clips,
        "verification": [],
        "note": "Clips authored by this library, not upstream. Dedicated to CC0.",
    }
    if not clips:
        (directory / "animations.json").write_text(json.dumps(report, indent=2) + "\n")
        print("no separable moving parts; nothing authored")
        return
    target = Path(model).with_name(f"{Path(model).stem}-animated.glb")
    bpy.context.scene.render.fps = FPS
    bpy.ops.export_scene.gltf(
        filepath=str(target),
        export_format="GLB",
        use_selection=False,
        export_animations=True,
        export_animation_mode="NLA_TRACKS",
        export_frame_range=False,
        export_force_sampling=True,
    )
    report["animated_model"] = target.name
    report["verification"] = verification_strip(clips, directory, objects)
    (directory / "animations.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"authored {len(clips)} clips -> {target.name}")


if __name__ == "__main__":
    arguments = sys.argv[sys.argv.index("--") + 1 :]
    main(*arguments)

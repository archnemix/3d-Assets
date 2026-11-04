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
from mathutils import Vector

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
    ("crank_turn", lambda n: n.endswith("_crank"), "X", 360.0, 60),
    ("gear_spin", lambda n: "_cog" in n or "_gear_" in n, "X", 360.0, 60),
    ("bit_spin", lambda n: n.endswith("_bit"), "Z", 720.0, 60),
    ("reel_spin", lambda n: "_spool" in n and "arm" not in n and "holder" not in n, "X", 360.0, 60),
]

# Hinged parts need a calibrated swing, not a blanket angle. Several upstream
# models are modelled with the hinge ALREADY OPEN, so a clip that starts at the
# rest pose and rotates "open" swings straight through the body. Each entry below
# is (axis, start_degrees, end_degrees) relative to the rest pose and was checked
# against the rendered verification frames. Where the rest pose is open the clip
# runs from the closed offset back to rest, so it always plays closed -> open.
HINGE_CLIPS = [
    ("door_open", lambda n: n.endswith("_door"), "Z", 0.0, 100.0, 60),
    ("lid_open", lambda n: n.endswith("_lid") and "hinge" not in n, "X", 0.0, -105.0, 60),
]
HINGE_CALIBRATION = {
    # Measured from the upstream node quaternion: rest yaw is -109.2 deg, i.e. the
    # door is modelled already open. +109.2 brings it shut, so play that back to 0.
    "power_box_01_door": ("Z", 109.2, 0.0),
    # Rest pose is closed and the free edge swings toward -Y, which is +Z rotation.
    "painted_wooden_cabinet_02_door": ("Z", 0.0, 100.0),
    # Both of these are modelled with the cover already raised.
    "metal_tool_chest_lid": ("X", 100.0, 0.0),
    "drill_press_01_lid": ("X", 100.0, 0.0),
}

# Round removable lids are not hinged: rotating them about their centre flips
# them off the pot. They lift clear of the rim instead, then tilt slightly.
LIFT_CLIPS = [
    (
        "lid_lift",
        lambda n: n.endswith("_lid")
        and any(token in n for token in ("teapot", "sugar", "pot_enamel")),
        60,
    ),
]

# Parts that must travel with a hinged part instead of pivoting on their own
# origin. The lid-side half of a hinge is a sibling in these flat glTF graphs.
FOLLOWERS = {"metal_tool_chest_lid": ("metal_tool_chest_hinge_lid",)}


def matching(objects, predicate):
    return [o for o in objects if o.type == "MESH" and predicate(o.name.lower())]


def attach_followers(objects, parts):
    """Parent rigid followers to the moving part so they cannot be left behind."""
    by_name = {o.name.lower(): o for o in objects if o.type == "MESH"}
    for obj in parts:
        for token in FOLLOWERS.get(obj.name.lower(), ()):
            child = by_name.get(token)
            if child is None or child is obj:
                continue
            world = child.matrix_world.copy()
            child.parent = obj
            child.matrix_world = world


def build_clip(name, parts, axis, degrees, frames, start=0.0):
    """Keyframe parts from the start angle to the end angle as one NLA track."""
    index = "XYZ".index(axis)
    for obj in parts:
        obj.animation_data_create()
        action = bpy.data.actions.new(f"{name}:{obj.name}")
        obj.animation_data.action = action
        obj.rotation_mode = "XYZ"
        base = list(obj.rotation_euler)
        for frame, angle in ((1, start), (frames, degrees)):
            obj.rotation_euler = base
            obj.rotation_euler[index] = base[index] + math.radians(angle)
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
        "start_degrees": start,
        "degrees": degrees,
        "frames": frames,
        "fps": FPS,
    }


def build_lift_clip(name, parts, frames):
    """Lift a removable lid clear of its rim, then tilt it slightly aside."""
    records = []
    for obj in parts:
        obj.animation_data_create()
        action = bpy.data.actions.new(f"{name}:{obj.name}")
        obj.animation_data.action = action
        obj.rotation_mode = "XYZ"
        base_location = list(obj.location)
        base_rotation = list(obj.rotation_euler)
        corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        height = max(c.z for c in corners) - min(c.z for c in corners)
        rise = max(height * 1.6, 0.02)
        for frame, factor, tilt in ((1, 0.0, 0.0), (frames, 1.0, 18.0)):
            obj.location = base_location
            obj.location[2] = base_location[2] + rise * factor
            obj.rotation_euler = base_rotation
            obj.rotation_euler[0] = base_rotation[0] + math.radians(tilt)
            obj.keyframe_insert(data_path="location", frame=frame)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        for curve in action.fcurves:
            for point in curve.keyframe_points:
                point.interpolation = "BEZIER"
        track = obj.animation_data.nla_tracks.new()
        track.name = name
        track.strips.new(name, 1, action)
        obj.animation_data.action = None
        obj.location = base_location
        obj.rotation_euler = base_rotation
        records.append({"part": obj.name, "rise_metres": round(rise, 4)})
    return {
        "name": name,
        "parts": [o.name for o in parts],
        "motion": "lift",
        "detail": records,
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
        # Every object NLA track is live at once by default, which would show
        # steering on top of a wheel-roll check. Solo the clip under review.
        for obj in objects:
            if obj.animation_data:
                for track in obj.animation_data.nla_tracks:
                    track.mute = track.name != clip["name"]
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
        strips.append({"clip": clip["name"], "frames": names})
    for obj in objects:
        if obj.animation_data:
            for track in obj.animation_data.nla_tracks:
                track.mute = False
    scene.frame_set(1)
    return strips


def main(model: str, output: str) -> None:
    directory = Path(output)
    directory.mkdir(parents=True, exist_ok=True)
    reset_scene()
    objects = import_model(model)
    clips = []
    lifted = set()
    for name, predicate, frames in LIFT_CLIPS:
        parts = matching(objects, predicate)
        if parts:
            lifted.update(o.name for o in parts)
            clips.append(build_lift_clip(name, parts, frames))
    for name, predicate, axis, start, degrees, frames in HINGE_CLIPS:
        parts = [o for o in matching(objects, predicate) if o.name not in lifted]
        if not parts:
            continue
        attach_followers(objects, parts)
        used = {c["name"] for c in clips}
        for position, obj in enumerate(parts):
            clip_name = name if position == 0 or name not in used else f"{name}_{position + 1}"
            calibrated = HINGE_CALIBRATION.get(obj.name.lower())
            if calibrated:
                axis_i, start_i, degrees_i = calibrated
            else:
                axis_i, start_i, degrees_i = axis, start, degrees
            clips.append(build_clip(clip_name, [obj], axis_i, degrees_i, frames, start=start_i))
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

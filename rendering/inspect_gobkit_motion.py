"""Non-destructive sampled motion renders for a Gobkit candidate."""

import json
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene import (  # noqa: E402
    add_studio_lights,
    bounds,
    camera_view,
    fit_camera,
    reset_scene,
    world_points,
)


def main(identifier):
    root = Path(__file__).resolve().parents[1]
    candidate = root / "quarantine" / "gobkit-animals-01" / identifier
    metadata = json.loads((candidate / "asset.json").read_text())
    model = candidate / metadata["model"]
    output = root / "reports" / "motion" / "gobkit-animals-01" / identifier
    output.mkdir(parents=True, exist_ok=True)
    reset_scene()
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(model))
    objects = [obj for obj in bpy.data.objects if obj not in before]
    armatures = [obj for obj in objects if obj.type == "ARMATURE"]
    if not armatures or not bpy.data.actions:
        raise RuntimeError("No imported armature or animation action")
    for obj in armatures:
        obj.data.pose_position = "POSE"
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.cycles.samples = 12
    scene.frame_set(0)
    low, high, radius = bounds(objects)
    center = (low + high) / 2
    add_studio_lights(center, radius)
    camera_view("motion", center, radius, 35, 15)
    fit_camera(scene.camera, world_points(objects), margin=1.4)
    frames = list(range(0, 120, 10))
    for frame in frames:
        scene.frame_set(frame)
        scene.render.filepath = str(output / f"frame-{frame:03d}.jpg")
        bpy.ops.render.render(write_still=True)
    (output / "inspection.json").write_text(
        json.dumps(
            {
                "model": str(model.relative_to(root)),
                "sampled_frames": frames,
                "fps": 24,
                "actions": [action.name for action in bpy.data.actions],
                "note": "Samples of the one baked track, not separate clips or proof of seamless looping.",
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1])

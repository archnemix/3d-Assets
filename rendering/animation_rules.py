"""Mechanical-animation rule table.

This module is deliberately free of the Blender (`bpy`) import so the rule
table can be unit-tested in plain Python. ``author_animations`` imports it and
renders each rule into a real glTF animation clip.

Each entry is (clip_name, part matcher, axis, degrees, frames). The axis is
local to the part. The matcher is a predicate on the glTF node name; a rule
fires for every node whose name it accepts.
"""

import re

# Known hinged node names verified against rendered poses. A generic `_lid`
# can be a screw cap, and an already-open hinged lid can have a different pivot.
HINGED_LIDS = frozenset({"drill_press_01_lid", "medical_box_lid", "metal_tool_chest_lid"})
HINGED_DOORS = frozenset(
    {
        "fantasy-mushroom-house_front_door",
        "large_iron_gate_left_door",
        "large_iron_gate_right_door",
        "painted_wooden_cabinet_02_door",
        "power_box_01_door",
        "witch-cottage_door",
    }
)


# Grab3D vehicle manifests document "rotate around local X to roll" and
# "rotate around local Z to articulate"; hinge parts rotate about the axis their
# name implies.
ROTATION_CLIPS = [
    ("wheel_roll", lambda n: bool(re.search(r"(?:^|[_-])wheel(?:$|[_-])", n)), "X", 360.0, 60),
    (
        "steer",
        lambda n: "wheel_f" in n
        or n.endswith("_fl")
        or n.endswith("_fr")
        or n.endswith("_steering"),
        "Z",
        32.0,
        45,
    ),
    ("trailer_swing", lambda n: n.endswith("_trailer"), "Z", 35.0, 60),
    ("crank_turn", lambda n: n.endswith("_crank"), "X", 360.0, 60),
    ("gear_spin", lambda n: "_cog" in n or "_gear_" in n, "X", 360.0, 60),
    ("bit_spin", lambda n: n.endswith("_bit"), "Z", 720.0, 60),
    (
        "reel_spin",
        lambda n: ("_spool" in n or n.endswith("_reel")) and "arm" not in n and "holder" not in n,
        "X",
        360.0,
        60,
    ),
    # Grab3D names the spinning element of a mechanical assembly `<slug>_rotor`
    # (camshaft, flywheel, differential, turbofan) and ships it as its own node.
    ("rotor_spin", lambda n: "_rotor" in n, "X", 360.0, 60),
    ("propeller_spin", lambda n: n.endswith("_propeller"), "X", 720.0, 60),
]

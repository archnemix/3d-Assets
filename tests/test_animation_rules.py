"""Tests for the mechanical-animation rule table (no Blender required)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rendering"))

from animation_rules import ROTATION_CLIPS  # noqa: E402

RULES = {name: matcher for name, matcher, _axis, _deg, _frames in ROTATION_CLIPS}


def test_wheel_roll_matches_grab3d_wheel_nodes():
    match = RULES["wheel_roll"]
    assert match("mountain-bike_wheel_front")
    assert match("moped_wheel_rear")
    assert match("farm-trailer_wheel_fl")
    assert match("wheel-front-left")
    assert not match("mountain-bike_body")
    assert not match("wheelchair_01")
    assert not match("flywheel_rotor")


def test_steer_matches_fl_fr_and_steering_nodes():
    match = RULES["steer"]
    assert match("mountain-bike_steering")
    assert match("moped_steering")
    assert match("farm-trailer_wheel_fl")
    assert match("farm-trailer_wheel_fr")
    assert not match("farm-trailer_wheel_rl")


def test_reel_spin_matches_spool_and_reel_but_not_arm():
    match = RULES["reel_spin"]
    assert match("combine-harvester_reel")
    assert match("hay_spool")
    assert not match("hay_spool_arm")
    assert not match("hay_spool_holder")


def test_rotor_spin_matches_grab3d_rotor_assemblies():
    match = RULES["rotor_spin"]
    assert match("camshaft_rotor")
    assert match("flywheel_rotor")
    assert match("differential_rotor_a")
    assert match("jet-engine_rotor")
    assert not match("flywheel")


def test_propeller_spin_matches_grab3d_propeller():
    match = RULES["propeller_spin"]
    assert match("cargo-ship_propeller")
    assert not match("cargo-ship_body")


def test_crank_and_gear_and_bit_rules():
    assert RULES["crank_turn"]("mountain-bike_crank")
    assert RULES["crank_turn"]("moped_crank")
    assert RULES["gear_spin"]("flywheel_gear_ring")
    assert RULES["bit_spin"]("drill_bit")

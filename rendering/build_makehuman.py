"""Blender entry point: build one CC0 MakeHuman candidate from a pinned recipe.

Run with Blender --background --python build_makehuman.py -- RECIPE PACK_DATA MPFB_SRC OUTPUT_GLB.
The script imports MPFB2 as a build tool, assembles CC0 assets, bakes export geometry,
and writes a GLB plus a small build report. It never modifies the source pack.
"""

import importlib
import importlib.util
import json
import shutil
import sys
import types
from pathlib import Path

import bpy

# MPFB 2.0.18 expects Blender 4.2 extension package naming. Loading it as plain
# `mpfb` makes LocationService call extension_path_user("mpfb"), which Blender
# rejects. We load the pinned source under a valid extension module name instead.
MPFB_PACKAGE = "bl_ext.user_default.mpfb"


def load_mpfb_extension(mpfb_src: Path):
    if MPFB_PACKAGE in sys.modules:
        return sys.modules[MPFB_PACKAGE]
    for name in ("bl_ext", "bl_ext.user_default"):
        if name not in sys.modules:
            parent = types.ModuleType(name)
            parent.__path__ = []
            sys.modules[name] = parent
    init = mpfb_src / "mpfb" / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        MPFB_PACKAGE, init, submodule_search_locations=[str(init.parent)]
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[MPFB_PACKAGE] = module
    spec.loader.exec_module(module)
    return module


def mpfb_services():
    return importlib.import_module(f"{MPFB_PACKAGE}.services")


def setup_mpfb(mpfb_src: Path, pack_data: Path):
    if hasattr(bpy.context.preferences.system, "use_online_access"):
        bpy.context.preferences.system.use_online_access = False
    print("Loading MPFB as Blender extension package", flush=True)
    module = load_mpfb_extension(mpfb_src)
    bpy.utils.extension_path_user(MPFB_PACKAGE, create=True)
    module.register()
    print("MPFB registered; installing CC0 system pack", flush=True)
    services = mpfb_services()
    services.LocationService.ensure_relevant_directories_exist()
    user_data = Path(services.LocationService.get_user_data())
    shutil.copytree(pack_data, user_data, dirs_exist_ok=True)
    # Recipes load explicit pack paths, so the UI asset-list cache is unnecessary.
    return module


def add_assets(recipe: dict, pack: Path, human):
    HumanService = mpfb_services().HumanService

    rig = HumanService.add_builtin_rig(human, "game_engine", import_weights=True)
    for part, relative in recipe["bodyparts"].items():
        smooth = (
            0
            if part in {"eyes", "eyebrows", "eyelashes", "teeth", "tongue"}
            else recipe["subdivision"]
        )
        HumanService.add_mhclo_asset(
            str(pack / relative),
            human,
            asset_type=part,
            subdiv_levels=smooth,
            material_type="GAMEENGINE",
        )
    for relative in recipe["clothes"]:
        HumanService.add_mhclo_asset(
            str(pack / relative),
            human,
            asset_type="clothes",
            subdiv_levels=recipe["subdivision"],
            material_type="GAMEENGINE",
        )
    HumanService.set_character_skin(str(pack / recipe["skin"]), human, skin_type="GAMEENGINE")
    return rig


def bake_export_meshes(root, human, subdivision: int):
    TargetService = mpfb_services().TargetService

    TargetService.bake_targets(human)
    meshes = [obj for obj in [root, *root.children_recursive] if obj.type == "MESH"]
    for obj in meshes:
        if obj == human and subdivision and not any(mod.type == "SUBSURF" for mod in obj.modifiers):
            modifier = obj.modifiers.new("Export subdivision", "SUBSURF")
            modifier.levels = subdivision
            modifier.render_levels = subdivision
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        for modifier in list(obj.modifiers):
            if modifier.type == "SUBSURF":
                modifier.levels = modifier.render_levels
            if modifier.type == "ARMATURE":
                bpy.ops.object.modifier_move_to_index(
                    modifier=modifier.name, index=len(obj.modifiers) - 1
                )
        for modifier in list(obj.modifiers):
            if modifier.type != "ARMATURE":
                bpy.ops.object.modifier_apply(modifier=modifier.name)
    return meshes


def tune_materials(meshes: list):
    transparent_tokens = ("short", "bob", "ponytail", "eyebrow", "eyelash", "hair")
    for obj in meshes:
        transparent = any(token in obj.name.lower() for token in transparent_tokens)
        for slot in obj.material_slots:
            material = slot.material
            if not material or not material.use_nodes:
                continue
            principled = next(
                (node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED"), None
            )
            if not principled:
                continue
            alpha = principled.inputs.get("Alpha")
            if transparent:
                if hasattr(material, "surface_render_method"):
                    material.surface_render_method = "BLENDED"
                if hasattr(material, "blend_method"):
                    material.blend_method = "BLEND"
                material.use_backface_culling = False
            elif alpha:
                for link in list(alpha.links):
                    material.node_tree.links.remove(link)
                alpha.default_value = 1.0
                if hasattr(material, "surface_render_method"):
                    material.surface_render_method = "DITHERED"


def export_glb(root, output: Path):
    bpy.ops.object.select_all(action="DESELECT")
    objects = [root, *root.children_recursive]
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = root
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(output),
        export_format="GLB",
        use_selection=True,
        export_apply=False,
        export_skins=True,
        export_morph=False,
        export_animations=False,
        export_yup=True,
        export_image_format="AUTO",
        export_cameras=False,
        export_lights=False,
    )
    return objects


def main(recipe_path: str, pack_data: str, mpfb_src: str, output: str) -> None:
    recipe_file = Path(recipe_path)
    pack = Path(pack_data)
    recipe = json.loads(recipe_file.read_text(encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_mpfb(Path(mpfb_src), pack)
    HumanService = mpfb_services().HumanService

    print("Creating base human", flush=True)
    human = HumanService.create_human(
        mask_helpers=True,
        detailed_helpers=False,
        extra_vertex_groups=False,
        feet_on_ground=True,
        scale=0.1,
        macro_detail_dict=recipe["macro"],
    )
    human.name = recipe["id"]
    print("Adding rig, body parts, clothes and skin", flush=True)
    rig = add_assets(recipe, pack, human)
    print("Baking export meshes", flush=True)
    meshes = bake_export_meshes(rig, human, recipe["subdivision"])
    tune_materials(meshes)
    print("Exporting GLB", flush=True)
    objects = export_glb(rig, Path(output))
    report = {
        "blender_version": bpy.app.version_string,
        "recipe": recipe["id"],
        "rig": rig.name,
        "bones": len(rig.data.bones),
        "objects": [
            {
                "name": obj.name,
                "type": obj.type,
                "vertices": len(obj.data.vertices) if obj.type == "MESH" else None,
                "materials": [slot.material.name for slot in obj.material_slots if slot.material]
                if obj.type == "MESH"
                else [],
                "modifiers": [mod.type for mod in obj.modifiers],
            }
            for obj in objects
        ],
    }
    report_path = Path(output).parent.parent / "provenance" / "build-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Built {output} with {len(meshes)} meshes and {len(rig.data.bones)} bones", flush=True)


if __name__ == "__main__":
    arguments = sys.argv[sys.argv.index("--") + 1 :]
    main(*arguments)

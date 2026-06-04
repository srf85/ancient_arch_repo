"""
main.py -- Ancient Greek Architecture Prop Kit
==============================================
Assembles a complete prop kit from configuration data using BUILDERS dispatcher patterns. Handles bad input gracefully.
"""

import os
import sys
import maya.cmds as cmds

try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import prop_kit_geometry as geo
import prop_kit_materials as mat

# ---------------------------------------------------------------------------
# Configuration Data
# ---------------------------------------------------------------------------
# Each dict is a "recipe" for one architecture element.
# "type" tells the dispatcher WHICH function to call.
# The rest are parameters for that function.
# Add a new element = add one dict. No code changes needed.

WALL_LENGTH = 16 
WALL_HEIGHT = 5
HALF = WALL_LENGTH / 2.0

PROP_KIT_CONFIG = [
    # Wall layout
    {"type": "wall", "length": WALL_LENGTH, "height": WALL_HEIGHT,
     "position": (0, 0, HALF)},
    {"type": "wall", "length": WALL_LENGTH, "height": WALL_HEIGHT,
     "position": (0, 0, -HALF)}

    # pillar layout
    {"type": "pillar", "pillar_radius": 1.5, "pillar_height": 8,
     "position": (HALF, 0, HALF)},
    {"type": "pillar", "pillar_radius": 1.5, "pillar_height": 8,
     "position": (-HALF, 0, HALF)},
]

MATERIAL_PALETTE = {
    "walls": ("wall_stone", (0.00, 0.00, 0.00)),
    "pillars": ("pillar_marble", (0.00, 0.00, 0.00)),
    "arches": ("arch_marble", (0.00, 0.00, 0.00)),
}

BUILDERS = {
    "wall":        geo.create_wall,
    "pillar":      geo.create_pillar,
    "arch":        geo.create_arch,
}

TYPE_MATERIALS = {
    "wall":        "walls",
    "pillar":      "pillars",
    "arch":        "arches",
}

# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def create_element(data):
    """Dispatch one config entry to the correct builder function.

    Looks up data["type"] in BUILDERS and calls the matching function
    with the remaining keys as ** keyword arguments.

    Args:
        data (dict): One entry from PROP_KIT_CONFIG. Must have a "type" key.

    Returns:
        str or None: The created Maya node name, or None if failed.
    """
    element_type = data.get("type")

    # Check: does the entry have a type?
    if not element_type:
        cmds.warning("Config entry missing 'type' key -- skipping.")
        return None

    # Check: do we have a builder for this type?
    builder = BUILDERS.get(element_type)
    if not builder:
        cmds.warning("Unknown type '()' --skipping.".format(element_type))
        return None

    # Strip "type" before ** unpacking -- it's not a function parameter
    params = {k: v for k, v in data.items() if k != "type"}

    try:
        return builder(**params)
    except TypeError as error:
        cmds.warning("Bad params for '{}': {}".format(element_type, error))
        return None
        
# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def build_prop_kit(config=None):
    """Build a complete prop kit from configuration data.

    Args:
        config (list): List of config dicts. Defaults to PROP_KIT_CONFIG.

    Returns:
        list: Names of all created Maya nodes.
    """
    if config is None:
        config = PROP_KIT_CONFIG

    cmds.file(new=True, force=True)

    # create materials
    shaders = {}
    for key, (name, color) in MATERIAL_PALETTE.items():
        shaders[key] = mat.create_material(name, color)

    # Process every entry in the config
    for entry in config:
        obj = create_element(entry)
        if obj:
            # Auto-assign material based on type
            mat_key = TYPE_MATERIALS.get(entry.get("type"))
            if mat_key and mat_key in shaders:
                mat.assign_material(obj, shaders[mat_key])
            results.append(obj)

    cmds.viewFit(allObjects=True)
    print("=== Prop Kit Complete ===")
    print("  {} elements from {} config entries.".format(
        len(results), len(config)))

    return results

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_prop_kit()

    # Bonus: test error handling with bad data
    print("\n--- Error handling tests ---")
    create_element({"type": "wall", "lenght": 16})  # Typo in key
    create_element({"length": 16, "height": 5})     # Missing type
    create_element({"type": "yoyo", "size": 10})    # Unknown type
    create_element({"type": "wall", "length": -1})  # Negative value
    print("--- All tests passed (warnings, not crashes) ---")

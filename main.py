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
HALF = WALL LENGTH / 2.0

PROP_KIT_CONFIG = [
    # Wall layout
    {"type": "wall", "length": WALL_LENGTH, "height": WALL_HEIGHT,
     "position": (0, 0, HALF)},
    {"type": "wall", "length": WALL_LENGTH, "height": WALL_HEIGHT,
     "position": (0, 0, -HALF)}

    # pillar layout
    {"type": "pillar", "pillar_radius": 1.5, "pillar_height": 8,
     "position":



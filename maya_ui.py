"""
maya_ui.py -- Ancient Greek Architecture Prop Kit
==================================================
Maya UI window for building the prop kit with adjustable elements.
Connects to prop_kit_geometry.py and prop_kit_materials.py.

Usage (Maya Script Editor, Python tab):
    import maya_ui
    maya_ui.show()
"""

import os
import sys
import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import prop_kit_geometry as geo
import prop_kit_materials as mat

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WINDOW_ID    = "AncientArchPropKit"
WINDOW_TITLE = "Arch Prop Kit Generator"

DEFAULT_COLORS = {
    "wall":   (0.75, 0.72, 0.65),
    "pillar": (0.90, 0.88, 0.84),
    "arch":   (0.82, 0.79, 0.74),
}

# ---------------------------------------------------------------------------
widgets = {}

def _float(key, default=0.0):
    try:
        return cmds.floatField(widgets[key], query=True, value=True)
    except Exception:
        return default

def _slider_float(key, default=1.0):
    try:
        return cmds.floatSliderGrp(widgets[key], query=True, value=True)
    except Exception:
        return default

def _slider_int(key, default=1):
    try:
        return cmds.intSliderGrp(widgets[key], query=True, value=True)
    except Exception:
        return default

def _color(key, default=(0.75, 0.72, 0.65)):
    try:
        return tuple(cmds.colorSliderGrp(widgets[key], query=True, rgbValue=True))
    except Exception:
        return default

def _menu(key, default=""):
    try:
        return cmds.optionMenu(widgets[key], query=True, value=True)
    except Exception:
        return default

def _make_material(obj, shader_name, color):
    """Create a shader and assign it to obj."""
    if obj is None:
        return
    shader = mat.create_material(shader_name, color)
    mat.assign_material(obj, shader)

# ---------------------------------------------------------------------------
# Pattern 5: named *args callbacks -- one per prop type
# ---------------------------------------------------------------------------

def build_wall(*args):
    """Read wall widgets and call geo.create_wall."""
    obj = geo.create_wall(
        length   = _float("wall_length",  10.0),
        height   = _slider_float("wall_height"),
        depth    = _float("wall_depth",    1.0),
        position = (
            _float("wall_pos_x"),
            _float("wall_pos_y"),
            _float("wall_pos_z"),
        ),
    )
    _make_material(obj, "wall_stone", _color("wall_color"))
    if obj:
        cmds.select(obj)
        print("[PropKit] Wall created: {}".format(obj))


def build_pillar(*args):
    """Read pillar widgets and call geo.create_pillar."""
    obj = geo.create_pillar(
        pillar_radius = _slider_float("pillar_radius"),
        pillar_height = _slider_float("pillar_height"),
        base_length   = _float("pillar_base_length", 1.5),
        base_height   = _float("pillar_base_height", 0.5),
        position      = (
            _float("pillar_pos_x"),
            _float("pillar_pos_y"),
            _float("pillar_pos_z"),
        ),
    )
    _make_material(obj, "pillar_marble", _color("pillar_color"))
    if obj:
        cmds.select(obj)
        print("[PropKit] Pillar created: {}".format(obj))


def build_arch(*args):
    """Read arch widgets and call geo.create_arch."""
    obj = geo.create_arch(
        length       = _float("arch_length", 6.0),
        height       = _float("arch_height", 5.0),
        depth        = _float("arch_depth",  1.0),
        subdivisionsX = _slider_int("arch_subX"),
        subdivisionsY = _slider_int("arch_subY"),
        position     = (
            _float("arch_pos_x"),
            _float("arch_pos_y"),
            _float("arch_pos_z"),
        ),
    )
    _make_material(obj, "arch_marble", _color("arch_color"))
    if obj:
        cmds.select(obj)
        print("[PropKit] Arch created: {}".format(obj))


def build_all(*args):
    """Create one of each prop at default positions."""
    build_wall()
    build_pillar()
    build_arch()
    cmds.viewFit(allObjects=True)
    print("[PropKit] Full prop kit built.")


# ---------------------------------------------------------------------------
# UI layout helpers
# ---------------------------------------------------------------------------

def _section(title):
    cmds.separator(height=8, style="none")
    cmds.text(label=title, align="left", font="boldLabelFont")
    cmds.separator(height=4, style="in")


def _float_row(label, key, default, lo=0.01, hi=999.0):
    """Label + floatField row. Stores control in widgets[key]."""
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(140, 80), adjustableColumn=2)
    cmds.text(label=label, align="right")
    widgets[key] = cmds.floatField(value=default, minValue=lo, maxValue=hi, precision=2)
    cmds.setParent("..")


def _pos_row(prefix):
    """Compact X / Y / Z floatField row for a given prefix (e.g. 'wall')."""
    cmds.text(label="Position  X / Y / Z", align="left")
    cmds.rowLayout(numberOfColumns=6, columnWidth6=(28, 55, 28, 55, 28, 55))
    for axis in ("x", "y", "z"):
        cmds.text(label=axis.upper(), align="right")
        widgets["{}_pos_{}".format(prefix, axis)] = cmds.floatField(
            value=0.0, minValue=-9999.0, maxValue=9999.0, precision=1)
    cmds.setParent("..")


# ---------------------------------------------------------------------------

def build_window():
    if cmds.window(WINDOW_ID, exists=True):
        cmds.deleteUI(WINDOW_ID)

    win = cmds.window(WINDOW_ID, title=WINDOW_TITLE,
                      widthHeight=(340, 700), sizeable=True)

    cmds.scrollLayout(horizontalScrollBarThickness=0, verticalScrollBarThickness=8)
    main_col = cmds.columnLayout(adjustableColumn=True, rowSpacing=3,
                                  columnOffset=("both", 8))
  
    # ---------------------------------------------------------------
  
    _section("WALL")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    # wall section in window

    _float_row("Length",  "wall_length", 10.0)
    _float_row("Depth",   "wall_depth",   1.0)

    widgets["wall_height"] = cmds.floatSliderGrp(
        label="Height:", field=True,
        minValue=0.1, maxValue=20.0, value=4.0,
        columnWidth3=(140, 50, 110))
    # float slider grp for the height

    _pos_row("wall")

    widgets["wall_color"] = cmds.colorSliderGrp(
        label="Material Color:",
        rgbValue=DEFAULT_COLORS["wall"],
        columnWidth3=(140, 30, 120))
    # color slider grp for the material

    cmds.separator(height=6, style="none")
    cmds.button(label="Create Wall", height=28,
                command=build_wall,
                backgroundColor=(0.30, 0.36, 0.44))
    cmds.setParent(main_col)

    # ---------------------------------------------------------------
  
    _section("PILLAR")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    # pillar section in window

    _float_row("Base Length",  "pillar_base_length", 1.5)
    _float_row("Base Height",  "pillar_base_height", 0.5)

    widgets["pillar_radius"] = cmds.floatSliderGrp(
        label="Shaft Radius:", field=True,
        minValue=0.1, maxValue=5.0, value=0.5,
        columnWidth3=(140, 50, 110))
    widgets["pillar_height"] = cmds.floatSliderGrp(
        label="Shaft Height:", field=True,
        minValue=0.1, maxValue=20.0, value=4.0,
        columnWidth3=(140, 50, 110))
    # float slider grp for radius and height

    _pos_row("pillar")

    widgets["pillar_color"] = cmds.colorSliderGrp(
        label="Material Color:",
        rgbValue=DEFAULT_COLORS["pillar"],
        columnWidth3=(140, 30, 120))

    cmds.separator(height=6, style="none")
    cmds.button(label="Create Pillar", height=28,
                command=build_pillar,
                backgroundColor=(0.30, 0.36, 0.44))
    cmds.setParent(main_col)

    # ------------------------------------------------------------------
  
    _section("ARCH")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    # arch section in window 

    _float_row("Length", "arch_length", 6.0)
    _float_row("Height", "arch_height", 5.0)
    _float_row("Depth",  "arch_depth",  1.0)

    widgets["arch_subX"] = cmds.intSliderGrp(
        label="Subdivisions X:", field=True,
        minValue=4, maxValue=32, value=12,
        columnWidth3=(140, 50, 110))
    widgets["arch_subY"] = cmds.intSliderGrp(
        label="Subdivisions Y:", field=True,
        minValue=1, maxValue=8, value=2,
        columnWidth3=(140, 50, 110))
    # slider grp for subdivisions

    _pos_row("arch")

    widgets["arch_color"] = cmds.colorSliderGrp(
        label="Material Color:",
        rgbValue=DEFAULT_COLORS["arch"],
        columnWidth3=(140, 30, 120))

    cmds.separator(height=6, style="none")
    cmds.button(label="Create Arch", height=28,
                command=build_arch,
                backgroundColor=(0.30, 0.36, 0.44))
    cmds.setParent(main_col)

    # --------------------------------------------------------------- 
  
    _section("SCENE")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=4)
    # scene builder section of the window

    cmds.button(label="Build Full Prop Kit  (Wall + Pillar + Arch)",
                height=32, command=build_all,
                backgroundColor=(0.44, 0.38, 0.28))

    cmds.button(label="Frame All",
                height=24,
                command=lambda *a: cmds.viewFit(allObjects=True))

    cmds.button(label="New Scene…",
                height=24,
                command=lambda *a: cmds.file(new=True, force=False),
                backgroundColor=(0.40, 0.24, 0.24))

    cmds.separator(height=10, style="none")

    return win


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def show():
    """Open the prop kit window. Call from Maya's Script Editor."""
    cmds.showWindow(build_window())   # Pattern 1: showWindow always last


if __name__ == "__main__":
    show()

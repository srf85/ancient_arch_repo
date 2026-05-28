"""
Data-Driven Scene Generator
===========================

Separating your scene DATA from the scene LOGIC. Defining scene elements in a data structure or dictionary 
and writing functions that read data and build the scene automatically.

"""

import maya.cmds as cmds

SCENE_DATA = [
    {"length": 5,  "height": 4, "depth": 1, "position": (0, 0, 5),  "name": "sm_wall", "type": "wall"},
    {"length": 10, "height": 4, "depth": 1, "position": (5, 0, 5),  "name": "md_wall", "type": "wall"},
    {"length": 10, "height": 6, "depth": 2, "position": (10, 0, 5), "name": "lg_wall", "type": "wall"},

    {"pillar_radius": 1, "pillar_height": 4, "base_length": 2, "base_height": 2, "position": (0, 0, 0),  "name": "sm_pillar", "type": "pillar"},
    {"pillar_radius": 2, "pillar_height": 6, "base_length": 4, "base_height": 4, "position": (5, 0, 0),  "name": "md_pillar", "type": "pillar"},
    {"pillar_radius": 3, "pillar_height": 8, "base_length": 6, "base_height": 6, "position": (10, 0, 0), "name": "lg_pillar", "type": "pillar"},  # was "sm_pillar" — likely a typo

    {"length": 6,  "height": 5,  "depth": 1, "position": (0, 0, 10),  "name": "sm_arch", "type": "arch"},
    {"length": 9,  "height": 8,  "depth": 4, "position": (5, 0, 10),  "name": "md_arch", "type": "arch"},
    {"length": 12, "height": 11, "depth": 7, "position": (10, 0, 10), "name": "lg_arch", "type": "arch"},
]

#dictionary for different prop kit objects (wall, pillar, and arch)

#----------------------------------------------------------------------------

for info in WALL:
    wall = create_wall(**info)
    print("Created wall: {}".format(wall))
# unpacking dictionary

for info in PILLAR:
    pillar = create_pillar(**info)
    print("Created pillar: {}".format(pillar))
# unpacking dictionary

for info in ARCH:
    arch = create_arch(**info)
    print("Created arch: {}".format(arch))
# unpacking dictionary

# ---------------------------------------------------------------------------
# Builder Functions
# ---------------------------------------------------------------------------

def create_wall(name="wall", length=10, height=4, depth=1, position=(0, 0, 0), **kwargs):
    """Create a wall element from a data dictionary.

    Args:
        data (dict): Must contain keys "name", "position", and optionally
            "width", "height", "depth".

    Returns:
        str: The name of the created Maya object.
    """
    length = data.get("length", 10)
    height = data.get("height", 4)
    depth = data.get("depth", 1)
    position = data.get("position", (0, 0, 0))
    name = data.get("name", "wall")
    # extracting values using .get with defaults
    
    wall = cmds.polyCube(length=length, height=height, depth=depth, name=name + "_wall")[0]
    # create wall from cube.

    cmds.move(position[0], position[1] + height / 2.0, position[2], wall)
    # move wall to the ground plane.

    return wall


def create_pillar(name="pillar", pillar_height=4, pillar_radius=0.5, base_length=1.5, base_height=1, position=(0, 0, 0), **kwargs):
    """Create a pillar element from a data dictionary.

    Args:
        data (dict): Must contain keys "name", "position", and optionally
            "pillar_height", "base_length".

    Returns:
        str: The name of the created Maya group.
    """
    pillar_height = data.get("pillar_height", 5)
    pillar_radius = data.get("pillar_radius", 1)
    base_length = data.get("base_length", 2)
    base_height = data.get("base_height", 2)
    position = data.get("position", (0, 0, 0))
    name = data.get("name", "pillar")
    # extracting values using .get with defaults

    pillar = cmds.polyCylinder(height=pillar_height, radius=pillar_radius, name=name + "_pillar")[0]
    cmds.move(0, pillar_height / 2.0, 0, pillar)
    # create pillar with poly cylinder + move pillar trunk to ground level

    base = cmds.polyCube(width=base_length, height=base_height, depth=base_length, name=name + "_base")[0]
    cmds.move(0, base_height / 2.0, 0, base)
    # create pillar base with poly cube + move to the bottom of the pillar

    top = cmds.polyCube(width=base_length, height=base_height, depth=base_length, name=name + "_top")[0]
    cmds.move(0, pillar_height + base_length, 0, base)
    # create pillar canopy with poly sphere + move to the height of the pillar

    pillar_group = cmds.group(pillar, base, top)
    cmds.move(position[0], position[1], position[2], pillar_group)
    # create group for all pillar elements+ move to position

    return pillar_group
    

def create_arch(name="arch", length=6, height=5, depth=1, subdivisionsX=6, subdivisionsY=2, position=(0, 0, 0), **kwargs):
    """Create a simple arch using a sliced poly torus, deleting the lower haft. 

    Args:
        length (float): Length of the arch opening along the X axis.
        height (float): Height from the base to the tip of the Arch.
        depth (float): Depth of the arch along the Z axis.

    Returns:
        str: The name of the arch transformed node.
    """
    length = data.get("length", 6)
    height = data.get("height", 5)
    depth = data.get("depth", 1)
    subdivisionsX = data.get("subdivisionsX", 6)
    subdivisionsY = data.get("subdivisionsY", 2)
    position = data.get("position", (0, 0, 0))
    name = data.get("name", "arch")
    
    arch = cmds.polyTorus(length=length, height=height, depth=depth, subdivisionsX=subdivisionsX, subdivisionsY=subdivisionsY, name=name + "_arch")[0]
    cmds.move(position[0], position[1], position[2], arch)
    #create arch with poly Torus, with subdivisions

    return arch
    

# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

# This dictionary maps a type name (string) to the function that builds it.
BUILDERS = {
    "wall": create_wall,
    "pillar": create_pillar,
    "arch": create_arch,
}

def create_element(data):
    """Create a single scene element by dispatching to the correct builder.

    Looks up data["type"] in the BUILDERS dictionary and calls the
    matching function.

    Args:
        data (dict): A dictionary from SCENE_DATA with at least a "type" key.

    Returns:
        str or None: The object name returned by the builder, or None if
            the type is unrecognized.
    """
    element_type = data.get("type")
    builder = BUILDERS.get(element_type)
    # read the type and look up the builder

    if builder is None:
        print("Warning: unknown element type '{}'".format(element_type))
        return None
    # warn and bail if unknown

    return builder(data)


def build_scene(scene_data):
    """Build the entire scene by iterating over a list of element dicts.

    Args:
        scene_data (list): A list of dictionaries, each describing one
            scene element.

    Returns:
        list: A list of created object/group names.
    """
    results = []

    for entry in scene_data:
        obj = create_element(entry)
        if obj is not None:
            results.append(obj)
    # loop through dictionaries and dispatch to builder

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.file(new=True, force=True)

    # Create a ground plane.
    cmds.polyPlane(name="ground", width=60, height=60,
                   subdivisionsX=1, subdivisionsY=1)

    # Build the scene from data.
    created_objects = build_scene(SCENE_DATA)
    print("Created {} objects: {}".format(len(created_objects), created_objects))

    cmds.viewFit(allObjects=True)
    print("Data-

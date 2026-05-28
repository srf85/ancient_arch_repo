prop_kit_geometry.py
====================
Geometry builder functions for the Ancient Greek Architecture Prop Kit.

Creates Maya polygon primitives shaped into architectural props:
walls, pillars, and arches.
====================

import maya.cmds as cmds

def create_wall(length=10, height=4, depth=1, position=(0, 0, 0)):
  
  """Create a simple rectangular stone wall segment as a Maya polyCube.

  The wall segment is a single scaled cube whose base sits at ground level 
  (y = 0) at the given position.

  Args:
      length (float): Length of the wall along the X axis.
      height (float): Height of the wall along the Y axis.
      depth (float): Depth of the wall along the Z axis.
      position (tuple): (x, y, z) ground-level position. The wall base will rest at this point; y is typically 0.

  Returns:
      str: The name of the created wall transform node.
  """
  wall = cmds.polyCube(length = length, height = height, depth = depth)[0]
  #create wall from cube.

  cmds.move(position[0], position[1] + height / 2.0, position[2], wall)
  #move wall to the ground plane.

  return wall

def create_pillar(pillar_radius=0.5, pillar_height=4, base_length=1.5, base_height=1,
                position=(0, 0, 0)):
    """Create a simple pillar using a cylinder shaft and a cube base and top.

    Args:
        pillar_radius (float): Radius of the cylindrical pillar.
        pillar_height (float): Height of the pillar cylinder.
        base_length (float): Length of the cube used for the base.
        base_height (float): Height of the cube used for the base
        position (tuple): (x, y, z) ground-level position for the pillar base.

    Returns:
        str: The name of a group node containing the pillar and base.
    """
    pillar = cmds.polyCylinder(radius=pillar_radius, height=pillar_height)[0]
    cmds.move(0, pillar_height / 2.0, 0, pillar)
    #create pillar with poly cylinder + move pillar to ground level

    base = cmds.polyCube(width=base_length, height=base_height, depth=base_length)[0]
    cmds.move(0, base_height / 2.0, 0, base)
    #create pillar base with poly cube + move to the ground plane

    top = cmds.polyCube(width=base_length, height=base_height, depth=base_length)[0]
    cmds.move(0, pillar_height + base_length, 0, top)
    #create pillar top with poly cube + move to the height of the pillar

    pillar_group = cmds.group(pillar, base, top)
    cmds.move(position[0], position[1], position[2], pillar_group)
    #create group for pillar, base, and top + move to position

    return pillar_group

def create_arch(length=6, height=5, depth=1, subdivisionsX=6, subdivisionsY=2, position=(0, 0, 0)):
    """Create a simple arch using a sliced poly torus, deleting the lower haft. 

    Args:
        length (float): Length of the arch opening along the X axis.
        height (float): Height from the base to the tip of the Arch.
        depth (float): Depth of the arch along the Z axis.

    Returns:
        str: The name of the arch transformed node.
    """
    arch = cmds.polyTorus(length=length, height=height, depth=depth, subdivisionsX=subdivisionsX, subdivisionsY=subdivisionsY)[0]
    cmds.move(0, 0, 0, arch)
    #create arch with poly Torus, with subdivisions

    cmds.select(f"{arch}.f[96:143]")
    cmds.delete
    #Select and delete bottom of the Torus

    return arch 



    

    

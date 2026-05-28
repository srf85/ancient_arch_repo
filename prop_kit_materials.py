"""
prop_kit_materials.py
=====================

Material creation and assignment utilities for the Ancient Greek Architecture Prop Kit.
Material utility functions for creating and assigning shaders in Maya.

This module provides helpers that create Lambert or Blinn shaders with
specified colors and assign them to objects.
"""

import maya.cmds as cmds

def create_material(name="stone_mat", color=(0.75, 0.72, 0.65), material_type="lambert"):
    """Create a Lambert shader with the given color and name. 
    The shading group is named "<name>_SG" and is wired up internally; 
    callers do not need to track it -- assign_material() looks it up
    from the shader name.

    Args:
        name (str): Name of the shader node.
        color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
        material_type (str): Type of shader to create, Supported values are "lambert" and "blinn".

    Returns:
        str: The name of the created shader node.
    """
    shader = cmds.shadingNode(material_type, aaShader=True, name=name)
    #create a shader node

    shader_grp = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG")
    #connect the shader to the group

    cmds.connectAttr(shader + ".outColor", shader_grp + ".surfaceShader", force=True)
    #connect the shader to the group

    cmds.setAttr(shader + ".color", *color, type="double3")
    #set the color attribute

    return shader

def assign_material(obj_name, shader_name):
    """Assign an existing shader to a Maya object.

    Looks up the shading group connected to the shader and adds the object to it. 
    Pass the shader name returned from create_material();
    you do not need to track the shading group yourself.

    Args:
        obj_name (str): The Maya object to receive the material.
        shader_name (str): The shader name returned from create_material().

    Returns:
        None
    """
    sgs = cmds.listConnections(shader_name + ".outColor", type="shadingEngine")
    #find the shading group

    cmds.sets(obj_name, edit=True, forceElement=sgs[0])
    #add the object to it

def create_and_assign(obj_name, name="auto_mat", color=(0.75, 0.72, 0.65), material_type="lambert"):
    """Convenience function: create a material and immediately assign it.

    Args:
        obj_name (str): The Maya object to receive the material.
        name (str): Name for the new shader.
        color (tuple): (r, g, b) color, values 0.0 to 1.0.
        material_type (str): "lambert" or "blinn"

    Returns:
        str: The name of the created shader node.
    """
    shader = create_material(name, color, material_type)
    #calling create_material

    assign_material(obj_name, shader)
    #assigning the material

    return shader
    

# Ancient Greek Architecture Prop Kit Generator

## What It Does
A Maya tool that generates an ancient greek achitectural prop kit from configuration parameters.
Artists can control wall dimensions, pillar dimensions, and materials without touching the creation logic.

## Planned Features
- [x] Core geometry functions (Week 6)
- [X] Data-driven configuration (Week 7)
- [X] Error handling + debug mode (Week 8)
- [X] Maya UI window + JSON save/load (Week 9)
- [X] Polish + documentation (Week 10)

## Project Structure
```
arch_prop_kit/
    prop_kit_geometry.py   # create_wall, create_pillar, create_arch
    prop_kit_materials.py  # create_material, assign_material
    main.py                # Entry point, config, build_fortress()
    date_driven_scene.py   # scene data in dict. and config
    maya_ui.py             # maya ui window builder
    README.md              # This file
```

## Functions

### prop_kit_geometry.py
- `create_wall(length, height, thickness, position)` — stone wall segment
- `create_pillar(height, radius, spacing, position, axis)` — Row of pillars
- `create_arch(length, height, thickness, position)` — arch

### prop_kit_materials.py
- `create_material(name, color)` — Lambert shader with RGB color
- `assign_material(obj_name, shader_name)` — Apply shader to object/

### maya_ui.py
- `show()` — Open the prop kit UI window

## How to Run
1. Copy this folder into your maya scripts folder (Documents > Maya > Scripts)
2. Open Maya
3. Open Script Editor (Windows > General Editors > Script Editor)
4. Run the following in the Python tab:

import maya_ui
maya_ui.show()

## Author
Sidney Ferrone | DIGM 131 | Drexel University

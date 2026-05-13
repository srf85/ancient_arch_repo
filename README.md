# Ancient Greek Architecture Prop Kit Generator

## What It Does
A Maya tool that generates an ancient greek achitectural prop kit from configuration parameters.
Artists can control wall dimensions, pillar dimensions, and materials without touching the creation logic.

## Planned Features
- [x] Core geometry functions (Week 6)
- [ ] Data-driven configuration (Week 7)
- [ ] Error handling + debug mode (Week 8)
- [ ] Maya UI window + JSON save/load (Week 9)
- [ ] Polish + documentation (Week 10)

## Project Structure
```
arch_prop_kit/
    prop_kit_geometry.py   # create_wall, create_pillar, create_arch
    prop_kit_materials.py  # create_material, assign_material
    main.py                # Entry point, config, build_fortress()
    README.md              # This file
```

## Functions

### prop_kit_geometry.py
- `create_wall(length, height, thickness, position)` — stone wall segment
- `create_pillar(height, radius, spacing, position, axis)` — Row of pillars
- `create_arch(length, height, thickness, position)` — arch

### prop_kit_materials.py
- `create_material(name, color)` — Lambert shader with RGB color
- `assign_material(obj_name, shader_name)` — Apply shader to object/group

## How to Run
1. Open Maya
2. Open Script Editor (Windows > General Editors > Script Editor)
3. Source `main.py` from the arch_prop_kit folder

## Author
Sidney Ferrone | DIGM 131 | Drexel University

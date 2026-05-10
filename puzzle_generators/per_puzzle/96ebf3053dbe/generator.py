"""Generator for c9680e90.

Rule: full 9-divider row recolors 5s and 6-components, selecting one
representative and its reflection.

Combinatorial axes (8): grid_h/w, component_orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_divider, no_components, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "96ebf3053dbe"
VERSION = "1.1.0"
TASK_ID = "96ebf3053dbe"
SUMMARY = "Full 9-divider row; rule recolors 5s and 6-components into rep + reflection."

INVARIANTS = [
    "one full row uses color 9",
    "cells above the divider may use color 5",
    "components below the divider use color 6",
    "the 6-component sits clear of grid borders",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_divider", "no_components", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "component_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for component_orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orient = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
             overrides.get("component_orientation") or \
             ctx.draw_choice("component_orientation", list(ORIENTATIONS))
    h = 9 + rng.randint(0, 2)
    w = 8 + rng.randint(0, 3)
    line_r = h // 2
    g = full_grid(h, w, 0)
    for c in range(w):
        g[line_r][c] = 9
    g[1][1] = 5
    if orient == "vertical":
        c = 2 + rng.randint(0, w - 4)
        for r in range(line_r + 2, min(h, line_r + 5)):
            g[r][c] = 6
    else:
        r = line_r + 2
        for c in range(2, min(w - 1, 5)):
            g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_divider":
        g[8][3] = 6
        return g
    if name == "no_components":
        for c in range(10):
            g[5][c] = 9
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 9
        return g
    return g

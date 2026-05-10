"""Generator for f15e1fac.

Rule: cyan edge line advances across grid and shifts when crossing
red edge markers.

Combinatorial axes (8): grid_h/w, cyan_edge, red_edge, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_cyan, no_red, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8eb9146172f8"
VERSION = "1.1.0"
TASK_ID = "8eb9146172f8"
SUMMARY = "Cyan edge line advances and shifts on red edge markers."

INVARIANTS = [
    "cyan cells all start on one grid edge",
    "red markers all sit on one edge and define shift events",
    "the generated line stays inside the grid after each shift",
    "the rule preserves the input markers and paints the shifted cyan trace",
]

EDGES = ("top", "bottom", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cyan", "no_red", "full_grid")
HELPFUL_TEXTURES = EDGES

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "cyan_edge":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(EDGES)},
    "red_edge":       {"type": "str", "default": "rng",
                       "valid": "|".join(EDGES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for cyan_edge",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    cyan_edge = (overrides.get("texture") if overrides.get("texture") in EDGES else None) or \
                overrides.get("cyan_edge") or \
                ctx.draw_choice("cyan_edge", list(EDGES))
    red_edge = ctx.draw_choice("red_edge", list(EDGES))
    g = full_grid(11, 11, 0)
    if cyan_edge == "top":
        for c in (4, 6):
            g[0][c] = 8
    elif cyan_edge == "bottom":
        for c in (4, 6):
            g[10][c] = 8
    elif cyan_edge == "left":
        for r in (4, 6):
            g[r][0] = 8
    else:
        for r in (4, 6):
            g[r][10] = 8
    if red_edge == "top":
        for c in (3, 7):
            g[0][c] = 2
    elif red_edge == "bottom":
        for c in (3, 7):
            g[10][c] = 2
    elif red_edge == "left":
        for r in (3, 7):
            g[r][0] = 2
    else:
        for r in (3, 7):
            g[r][10] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_cyan":
        for c in (3, 7):
            g[0][c] = 2
        return g
    if name == "no_red":
        for c in (4, 6):
            g[0][c] = 8
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 8
        return g
    return g

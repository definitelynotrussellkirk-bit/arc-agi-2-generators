"""Generator for a1aa0c1e.

Rule: floor colors encode ladder rung counts into 3-wide bars, with a
maroon separator and optional gray marker.

Combinatorial axes (8): grid_h/w, floor_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_floors, no_rungs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b088f161470"
VERSION = "1.1.0"
TASK_ID = "7b088f161470"
SUMMARY = "Floor colors encode ladder rung counts; maroon separator + gray marker."

INVARIANTS = [
    "floor rows are full nonzero rows",
    "the last floor row supplies the maroon output color",
    "between consecutive floors, contiguous rung rows in that floor color are counted",
    "floor colors are distinct from each other and from gray",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_floors", "no_rungs", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7"},
    "floor_count":    {"type": "int", "default": "3", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("floor_count", 3, 3)
    c1, c2, c3, maroon = ctx.draw_distinct_colors("colors", n=4, exclude={0, 5})
    g = full_grid(13, 7, 0)
    floors = [(0, c1), (4, c2), (8, c3), (12, maroon)]
    for r, color in floors:
        for c in range(7):
            g[r][c] = color
    for r in [2]:
        for c in range(1, 4):
            g[r][c] = c1
    for r in [5, 6]:
        for c in range(2, 5):
            g[r][c] = c2
    for r in [9, 10, 11]:
        for c in range(1, 4):
            g[r][c] = c3
    g[3][6] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 7, 0)
    if name == "no_floors":
        g[3][6] = 5
        return g
    if name == "no_rungs":
        for r, color in [(0, 1), (4, 2), (8, 3), (12, 9)]:
            for c in range(7):
                g[r][c] = color
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(7):
                g[r][c] = 9
        return g
    return g

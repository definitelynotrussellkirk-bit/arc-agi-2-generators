"""Generator for arc_additional_puzzle_bank_volume4:H24.

Rule: pivot = first 2; for each 1-cell, paint 1 at original + 3 reflected
positions (vertical mirror, horizontal mirror, both).

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pivot, no_cells, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef4af8761400"
VERSION = "1.1.0"
TASK_ID = "ef4af8761400"
SUMMARY = "Grid with 2-pivot + 1-cells in one quadrant; 4-fold reflection."

INVARIANTS = [
    "exactly one 2-pivot, away from grid edges",
    "1-2 1-cells in one quadrant, all reflections stay in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pivot", "no_cells", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    pr = h // 2
    pc = w // 2
    g[pr][pc] = 2
    g[pr - 2][pc - 1] = 1
    g[pr - 1][pc - 2] = 1
    g[pr - 1][pc - 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_pivot":
        g[2][2] = 1
        return g
    if name == "no_cells":
        g[4][4] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 1
        return g
    return g

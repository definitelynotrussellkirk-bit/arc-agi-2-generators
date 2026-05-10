"""Generator for arc_puzzle_bank_third21:E18.

Rule: every nonzero cell drops one row when the cell below is background
in the input.

Combinatorial axes (8): grid_h/w, n_cells, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: empty_grid, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e873f4e123b6"
VERSION = "1.1.0"
TASK_ID = "e873f4e123b6"
SUMMARY = "Every nonzero cell drops one row when the cell below is background."
INVARIANTS = [
    "nonzero cells are sparse",
    "some cells have empty space below",
    "all moves are simultaneous",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "6..10"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "6..10"},
    "n_cells":        {"type": "int", "default": "rng 4..8", "valid": "4..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = ctx.draw_int("n_cells", 4, 8)
    g = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h - 1) for c in range(w)]
    rng.shuffle(positions)
    for i, (r, c) in enumerate(positions[:n]):
        g[r][c] = (i % 8) + 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "empty_grid":
        return g
    if name == "single_cell":
        g[2][3] = 3
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 3
        return g
    return g

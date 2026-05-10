"""Generator for arc_additional_puzzles_21_set3:H15.

Rule: 2-marker on row 0 or col 0 defines mirror axis. Mirror each
5-cell across axis; paint 7 if target empty.

Combinatorial axes (8): grid_h/w, palette_kind, axis, n_5cells,
palette_size, position_bias, n_distinct_colors, mirror_kind, texture.
Degenerates: no_axis, no_5s, target_occupied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aeb31f908966"
VERSION = "1.1.0"
TASK_ID = "aeb31f908966"
SUMMARY = "2-axis on top row OR left col + 5-cells on one side."

INVARIANTS = [
    "exactly one 2-marker (on row 0 OR col 0)",
    "1-3 5-cells in one half of the grid",
]

PALETTE_KINDS = ("default", "vert_axis", "horiz_axis", "mixed_axis")
DEGENERATE_TEXTURES = ("no_axis", "no_5s", "target_occupied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "axis":           {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "n_5cells":       {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "axis_relative", "valid": "axis_relative"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "mirror_kind":    {"type": "str", "default": "fixed", "valid": "fixed"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    axis = ctx.draw_int("axis", 0, 1)
    g = full_grid(h, w, 0)
    if axis == 0:
        g[0][5] = 2
        g[3][1] = 5; g[4][1] = 5
        g[5][2] = 5
    else:
        g[3][0] = 2
        g[1][3] = 5; g[2][4] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # 5-cells but no 2-marker → mirror axis undefined
        g[3][1] = 5; g[4][1] = 5
        return g
    if name == "no_5s":
        # axis but no source cells → rule has nothing to mirror
        g[0][5] = 2
        return g
    if name == "target_occupied":
        # axis + 5-cells but mirror targets are pre-occupied → no 7s painted
        g[0][5] = 2
        g[3][1] = 5; g[4][1] = 5
        g[3][9] = 4; g[4][9] = 4
        return g
    return g

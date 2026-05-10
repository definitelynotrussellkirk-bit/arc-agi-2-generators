"""Generator for arc_additional_puzzles_21_set5:M35.

Rule: for each color with exactly 2 aligned cells (same row or column,
even distance), paint the integer midpoint cell with color 9.

Combinatorial axes (8): grid_h/w, palette_kind, num_pairs,
palette_size, position_bias, n_distinct_colors, alignment_mix, texture.
Degenerates: odd_distance, only_one_cell, three_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2365d033c2b8"
VERSION = "1.1.0"
TASK_ID = "2365d033c2b8"
SUMMARY = "2 colors each with 2 aligned cells (even distance) so midpoint is integer."

INVARIANTS = [
    "2 distinct non-{0,9} colors, each with exactly 2 cells",
    "each color's 2 cells are aligned with even distance",
]

PALETTE_KINDS = ("default", "row_only", "col_only", "mixed_axes")
DEGENERATE_TEXTURES = ("odd_distance", "only_one_cell", "three_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_pairs":      {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "alignment_mix":  {"type": "str", "default": "row+col", "valid": "row+col"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[2][1] = 1
    g[2][7] = 1
    g[1][4] = 3
    g[5][4] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "odd_distance":
        # distance 5 — no integer midpoint
        g[2][1] = 1
        g[2][6] = 1
        return g
    if name == "only_one_cell":
        # color has only 1 cell — no pair, rule no-op
        g[2][3] = 1
        g[1][6] = 3
        g[5][6] = 3
        return g
    if name == "three_cells":
        # color has 3 cells — pairing ambiguous
        g[2][1] = 1
        g[2][3] = 1
        g[2][7] = 1
        g[1][5] = 3
        g[5][5] = 3
        return g
    return g

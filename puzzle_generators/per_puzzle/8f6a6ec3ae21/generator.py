"""Generator for arc_puzzle_bank_21_set5_e:medium_e06.

Rule: col 0 holds 1-marks at certain rows; row 0 holds 2-marks at
certain cols; output paints 8 at every (row-of-1, col-of-2) intersection.

Combinatorial axes (8): grid_h/w, palette_kind, n_marks_1, n_marks_2,
palette_size, position_bias, n_distinct_colors, mark_density, texture.
Degenerates: no_1_marks, no_2_marks, marks_at_origin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8f6a6ec3ae21"
VERSION = "1.1.0"
TASK_ID = "8f6a6ec3ae21"
SUMMARY = "Row 0 has 2-3 2-marks at >0 cols; col 0 has 2-3 1-marks at >0 rows."

INVARIANTS = [
    "background is 0",
    "(0,0) is 0",
    "row 0 has 2-3 2-cells at cols >= 1",
    "col 0 has 2-3 1-cells at rows >= 1",
]

PALETTE_KINDS = ("default", "sparse", "dense", "balanced")
DEGENERATE_TEXTURES = ("no_1_marks", "no_2_marks", "marks_at_origin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks_1":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_marks_2":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "axis", "valid": "axis"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "mark_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_2 = rng.randint(2, 3)
    n_1 = rng.randint(2, 3)
    for c in rng.sample(range(1, w), n_2):
        g[0][c] = 2
    for r in rng.sample(range(1, h), n_1):
        g[r][0] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_1_marks":
        # only 2-marks in row 0 — no rows to intersect with
        g[0][2] = 2
        g[0][5] = 2
        return g
    if name == "no_2_marks":
        # only 1-marks in col 0 — no cols to intersect with
        g[2][0] = 1
        g[4][0] = 1
        return g
    if name == "marks_at_origin":
        # invariant violation: (0,0) nonzero, marks include the origin
        g[0][0] = 1  # ambiguous: is this a 1-mark or 2-mark?
        g[0][3] = 2
        g[3][0] = 1
        return g
    return g

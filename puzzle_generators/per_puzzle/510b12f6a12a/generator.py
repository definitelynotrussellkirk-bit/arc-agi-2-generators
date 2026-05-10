"""Generator for arc_puzzle_bank_21_set5_s:S5_M2 — beam-crossing cells.

Rule: top row (row 0) has 2-marks (defining vertical beams downward).
Left column (col 0) has 1-marks (defining horizontal beams rightward).
Beams stop at color-5 blockers. Output paints 6 at every (row r, col c)
where a vertical beam from col c crosses a horizontal beam from row r.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_v/n_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_v_marks, no_h_marks, all_marks_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "510b12f6a12a"
VERSION = "1.1.0"
TASK_ID = "510b12f6a12a"
SUMMARY = "Top-row 2-markers + left-col 1-markers (no blockers); intersections form a grid."

INVARIANTS = [
    "background is 0",
    "(0,0) is 0",
    "row 0 has 2-marks at cols >= 1; col 0 has 1-marks at rows >= 1",
    ">=2 marks of each type so the intersection set is interesting",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_v_marks", "no_h_marks", "marks_at_origin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_v":            {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "row0_2marks_col0_1marks",
                       "valid": "row0_2marks_col0_1marks"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_v = rng.randint(2, 3)
    n_h = rng.randint(2, 3)
    for c in rng.sample(range(1, w), n_v):
        g[0][c] = 2
    for r in rng.sample(range(1, h), n_h):
        g[r][0] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_v_marks":
        # no vertical beams → no intersections, rule produces empty output
        for r in [2, 4, 6]: g[r][0] = 1
        return g
    if name == "no_h_marks":
        # no horizontal beams → no intersections
        for c in [2, 4, 6]: g[0][c] = 2
        return g
    if name == "marks_at_origin":
        # mark at (0,0) → invariant says (0,0) is 0; rule's preconditions broken
        g[0][0] = 2   # invalid: marker at origin
        for c in [3, 5]: g[0][c] = 2
        for r in [3, 5]: g[r][0] = 1
        return g
    return g

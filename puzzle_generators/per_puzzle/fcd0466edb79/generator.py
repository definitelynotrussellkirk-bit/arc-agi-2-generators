"""Generator for arc_puzzle_bank_eleventh21:M77 — select cols by row-0 1-marks.

Rule: row 0 has 1-markers at certain cols. Output is the rows below
row 0, restricted to only the marked cols.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marks, all_cols_marked, body_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fcd0466edb79"
VERSION = "1.1.0"
TASK_ID = "fcd0466edb79"
SUMMARY = "Row 0 has 2-3 1-markers at distinct cols + dense colored content below."

INVARIANTS = [
    "background is 0 in non-content cells",
    "row 0 has 2-3 1-cells at distinct cols (>=1 col not marked)",
    "rows below row 0 contain a variety of non-zero values (so output is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marks", "all_cols_marked", "body_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "row0_marker",
                       "valid": "row0_marker"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "density":        {"type": "str", "default": "medium", "valid": "medium"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_cols = rng.randint(2, min(3, w - 1))
    cols = rng.sample(range(w), n_cols)
    for c in cols:
        g[0][c] = 1
    for r in range(1, h):
        for c in range(w):
            if rng.random() < 0.5:
                g[r][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    if name == "no_marks":
        # row 0 has no 1-markers → no columns selected, output has 0 columns (ambiguous)
        for r in range(1, h):
            for c in range(w):
                if (r * 3 + c) % 3 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "all_cols_marked":
        # every column marked → output equals body without row 0, rule effect minimal
        for c in range(w):
            g[0][c] = 1
        for r in range(1, h):
            for c in range(w):
                if (r + c) % 2 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "body_empty":
        # marks present but body all zeros → output is all-zero strip, no information
        for c in [1, 4, 6]:
            g[0][c] = 1
        return g
    return g

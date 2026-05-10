"""Generator for arc_puzzle_bank_21_set15_bundle:easy_o04.

Within each row, colors that appear once are kept and repeated colors are
erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, all_singletons, blank_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4d8f78cee8b3"
VERSION = "1.1.0"
TASK_ID = "4d8f78cee8b3"
SUMMARY = "Rows mixing singleton colors with repeated distractor colors."

INVARIANTS = [
    "background is 0",
    "active rows contain one repeated color and one singleton color",
    "some rows may be empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "all_singletons", "blank_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 6..10", "valid": "2..18"},
    "position_bias":  {"type": "str", "default": "row_keyed_singletons",
                       "valid": "row_keyed_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..10", "valid": "2..18"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        row_count = min(ctx.draw_int("row_count", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    colors = ctx.draw_distinct_colors("colors", n=row_count * 2, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    for i, r in enumerate(rows):
        repeated = colors[2 * i]
        singleton = colors[2 * i + 1]
        cols = rng.sample(range(w), 3)
        g[r][cols[0]] = repeated
        g[r][cols[1]] = repeated
        g[r][cols[2]] = singleton
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # every row's colors all repeat → output is fully blank
        g[1][1] = 4; g[1][3] = 4; g[1][5] = 4
        g[3][2] = 6; g[3][6] = 6; g[3][8] = 6
        g[5][1] = 3; g[5][4] = 3; g[5][7] = 3
        return g
    if name == "all_singletons":
        # every cell is a unique color in its row → rule is identity
        g[1][1] = 4; g[1][3] = 6; g[1][5] = 3
        g[3][2] = 8; g[3][6] = 7
        g[5][4] = 1; g[5][8] = 9
        return g
    if name == "blank_rows":
        # blank → no rows to filter, identity output
        return g
    return g

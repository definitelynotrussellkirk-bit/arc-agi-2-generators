"""Generator for arc_puzzle_bank_21_set21_bundle:easy_p05.

Rule: rows contain a unique nonzero majority color plus one minority
color; the rule recolors based on majority.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rows, all_tied, single_row_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff5eb7af92e7"
VERSION = "1.1.0"
TASK_ID = "ff5eb7af92e7"
SUMMARY = "Rows contain a unique nonzero majority color plus one minority color."

INVARIANTS = [
    "background is 0",
    "each active row has one majority nonzero color",
    "minority cells never tie the majority count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rows", "all_tied", "single_row_one_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng h-3..h", "valid": "1..14"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_pairs",
                       "valid": "row_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    active_rows = rng.sample(range(h), rng.randint(max(1, h - 3), h))
    for r in active_rows:
        maj, minor = rng.sample(colors, 2)
        maj_count = rng.randint(3, min(4, w - 1))
        minor_count = rng.randint(1, min(2, w - maj_count))
        cols = rng.sample(range(w), maj_count + minor_count)
        for c in cols[:maj_count]:
            grid[r][c] = maj
        for c in cols[maj_count:]:
            grid[r][c] = minor
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_rows":
        # empty grid → no rows to recolor by majority
        return g
    if name == "all_tied":
        # majority and minority counts equal → no unique majority, rule undefined
        for c in range(0, 4):
            g[2][c] = 4
        for c in range(4, 8):
            g[2][c] = 6
        return g
    if name == "single_row_one_color":
        # entire active row is one color → no minority to contrast against
        for c in range(w):
            g[3][c] = 5
        return g
    return g

"""Generator for arc_puzzle_bank_21_set8:easy_h04.

Rule: keep only colors whose occurrences are confined to a single row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, kept_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_single_row, all_multi_row, single_color_total.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c6496d261a6"
VERSION = "1.1.0"
TASK_ID = "2c6496d261a6"
SUMMARY = "Keep only colors whose occurrences are confined to one row."

INVARIANTS = [
    "background is 0",
    "some colors occur only within one row",
    "some colors occur in multiple rows",
    "multi-row colors are erased everywhere",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_single_row", "all_multi_row", "single_color_total")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "kept_colors":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "row_confined_with_distractors",
                       "valid": "row_confined_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _place_empty(g, rng, row, color):
    cols = [c for c, v in enumerate(g[row]) if v == 0]
    if not cols:
        return False
    g[row][rng.choice(cols)] = color
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        kept = ctx.draw_int("kept_colors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        kept = ctx.draw_int("kept_colors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        kept = ctx.draw_int("kept_colors", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], kept + 2)
    for color in palette[:kept]:
        r = rng.randrange(h)
        for c in rng.sample(range(w), rng.randint(1, 3)):
            g[r][c] = color
    for color in palette[kept:]:
        for _ in range(40):
            rows = rng.sample(range(h), 2)
            if _place_empty(g, rng, rows[0], color) and _place_empty(g, rng, rows[1], color):
                break
        else:
            raise ValueError("could not place multi-row color")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "all_single_row":
        # every color is confined to one row → rule is identity, output equals input
        for c in [1, 4, 7]: g[0][c] = 4
        for c in [2, 6, 8]: g[2][c] = 6
        for c in [1, 5]: g[4][c] = 3
        return g
    if name == "all_multi_row":
        # every color spans multiple rows → rule erases everything, output is empty
        g[0][2] = 4; g[3][6] = 4
        g[1][1] = 6; g[4][7] = 6
        g[2][3] = 3; g[5][8] = 3
        return g
    if name == "single_color_total":
        # only one color anywhere → no comparison; either kept or all erased
        for c in [1, 5]: g[0][c] = 4
        for c in [3, 8]: g[3][c] = 4   # multi-row
        return g
    return g

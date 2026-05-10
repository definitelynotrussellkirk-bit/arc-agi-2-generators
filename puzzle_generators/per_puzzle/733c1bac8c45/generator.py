"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m03.

Rule: each row's nonzero cells pack to the left in that row's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_left_packed, multi_color_in_row, no_active_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "733c1bac8c45"
VERSION = "1.1.0"
TASK_ID = "733c1bac8c45"
SUMMARY = "Single-color row populations scattered across otherwise zero rows."

INVARIANTS = [
    "background is 0",
    "each nonempty row uses exactly one nonzero color",
    "each nonempty row has 1-5 colored cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_left_packed", "multi_color_in_row", "no_active_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "scattered_rows",
                       "valid": "scattered_rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        row_count = min(ctx.draw_int("row_count", 3, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    colors = ctx.draw_distinct_colors("colors", n=row_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    for i, r in enumerate(rows):
        n = rng.randint(1, min(5, w - 1))
        cols = rng.sample(range(w), n)
        for c in cols:
            g[r][c] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "already_left_packed":
        # rows already left-packed → rule is identity, no movement visible
        for r, vs in [(1, [3, 3, 3]), (3, [4, 4]), (5, [6, 6, 6, 6])]:
            for i, v in enumerate(vs):
                g[r][i] = v
        return g
    if name == "multi_color_in_row":
        # row uses multiple colors → "single color per row" invariant violated, ambiguous packing color
        for c, v in [(1, 3), (3, 5), (5, 7), (7, 4)]:
            g[2][c] = v
        return g
    if name == "no_active_rows":
        # empty grid → no rows to pack
        return g
    return g

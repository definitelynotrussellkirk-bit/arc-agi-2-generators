"""Generator for arc_puzzle_bank_21_set9_s:S9_E7.

Rule: rows containing two same-color markers are filled across the
inclusive interval between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_marker_only, span_already_filled, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "569aa05e004d"
VERSION = "1.1.0"
TASK_ID = "569aa05e004d"
SUMMARY = "Rows containing two same-color markers are filled across the inclusive interval between them."

INVARIANTS = [
    "background is 0",
    "two to four rows contain exactly two cells of one color",
    "the two cells in each active row are separated by at least one zero",
    "output contains only the filled row intervals",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_marker_only", "span_already_filled", "no_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..6"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        row_count = min(ctx.draw_int("row_count", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        row_count = min(ctx.draw_int("row_count", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
        row_count = min(ctx.draw_int("row_count", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    colors = [2, 3, 4, 6, 7, 8]
    for r, color in zip(rows, colors):
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = color
        g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "single_marker_only":
        # active rows have 1 marker each → no pair to define an interval
        g[1][3] = 3
        g[3][6] = 5
        return g
    if name == "span_already_filled":
        # interval between markers already painted with a different color → conflict
        g[2][1] = 4; g[2][7] = 4
        for c in range(2, 7):
            g[2][c] = 6
        return g
    if name == "no_markers":
        # empty grid → no markers, no intervals, rule is no-op
        return g
    return g

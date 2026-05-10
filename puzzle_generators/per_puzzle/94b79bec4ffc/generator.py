"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p02.

Rows are marked on the left or right border to dock their colored segment.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_segment, marker_at_both_edges.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "94b79bec4ffc"
VERSION = "1.1.0"
TASK_ID = "94b79bec4ffc"
SUMMARY = "Marked rows with one non-marker segment docked left or right."

INVARIANTS = [
    "background is 0",
    "row marker 1 appears only at the left edge",
    "row marker 2 appears only at the right edge",
    "segment colors exclude marker colors 1 and 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_segment", "marker_at_both_edges")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "marked_rows_with_segment",
                       "valid": "marked_rows_with_segment"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..7"},
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
        w = ctx.draw_int("grid_w", 9, 11)
        row_count = min(ctx.draw_int("row_count", 3, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    colors = ctx.draw_distinct_colors("colors", n=row_count, exclude={0, 1, 2})
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    for i, r in enumerate(rows):
        length = rng.randint(2, min(5, w - 3))
        if rng.choice([True, False]):
            g[r][0] = 1
            start = rng.randint(2, w - length - 1)
        else:
            g[r][w - 1] = 2
            start = rng.randint(1, w - length - 3)
        for c in range(start, start + length):
            g[r][c] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # segment without row marker → no dock direction specified
        for c in range(3, 7): g[2][c] = 4
        return g
    if name == "no_segment":
        # marker without segment → nothing to dock
        g[2][0] = 1
        g[4][w - 1] = 2
        return g
    if name == "marker_at_both_edges":
        # row has both 1 and 2 markers → ambiguous dock direction
        g[2][0] = 1; g[2][w - 1] = 2
        for c in range(3, 7): g[2][c] = 4
        return g
    return g

"""Generator for arc_additional_puzzle_bank_volume20:E136 — Recolor 1-blobs that touch the border to 2.

Rule: any 1-color blob with at least one cell on the grid border
(row 0, row h-1, col 0, col w-1) → recolor to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_interior, all_border, no_color_1.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "dcf954423fbb"
VERSION = "1.1.0"
TASK_ID = "dcf954423fbb"
SUMMARY = "Mix of 1-blobs touching border vs interior, plus 7-decoration."

INVARIANTS = [
    "≥2 1-blobs touching the grid border",
    "≥1 1-blob fully interior (won't recolor)",
    "1-2 7-decoration blobs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_interior", "all_border", "no_color_1")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "border_and_interior_blobs",
                       "valid": "border_and_interior_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
    L = [(0, 0), (1, 0), (1, 1)]
    placements = [
        (0, rng.randint(0, 2), sq),
        (rng.randint(2, 4), rng.randint(3, w - 5), sq),
        (h - 2, rng.randint(0, 1), L),
        (rng.randint(0, 1), w - 2, [(0, 0), (1, 0)]),
    ]
    for top, left, s in placements:
        paint_at(g, top, left, s, 1)
    g[h - 3][rng.randint(1, 3)] = 7
    g[h - 2][rng.randint(2, 4)] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_interior":
        # all 1-blobs are strictly interior → rule recolors nothing, output equals input
        paint_at(g, 3, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 1)
        paint_at(g, 5, 6, [(0, 0), (1, 0), (1, 1)], 1)
        return g
    if name == "all_border":
        # all 1-blobs touch the border → all recolored to 2; no contrast in output
        paint_at(g, 0, 1, [(0, 0), (0, 1), (1, 0)], 1)
        paint_at(g, h - 2, w - 3, [(0, 0), (0, 1), (1, 1)], 1)
        paint_at(g, 4, 0, [(0, 0), (1, 0)], 1)
        return g
    if name == "no_color_1":
        # no color-1 cells → rule has no blobs to recolor, output equals input
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 5, 5, [(0, 0), (1, 0), (1, 1)], 6)
        return g
    return g

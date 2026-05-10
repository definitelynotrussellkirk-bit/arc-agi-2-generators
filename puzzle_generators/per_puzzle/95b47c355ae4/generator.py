"""Generator for arc_additional_puzzle_bank_volume4:E25.

Rule: erase all 6-cells; for each original 6 position (r, c) place a new
6 at (r+1, c+1) if in-bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_6_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_6_cells, all_6_at_bottom_right, no_5_decoration.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "95b47c355ae4"
VERSION = "1.1.0"
TASK_ID = "95b47c355ae4"
SUMMARY = "Scattered 6-cells + small 5-blobs as decoration."

INVARIANTS = [
    "≥4 isolated 6-cells",
    "≥2 5-blobs (rectangles) as decoration",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_6_cells", "all_6_at_bottom_right", "no_5_decoration")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_6_cells":      {"type": "int", "default": "rng 4..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    sq = [(0, 0), (0, 1)]
    sq2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
    paint_at(g, 1, 1, sq, 5)
    paint_at(g, h - 4, w - 4, sq2, 5)
    paint_at(g, 6 if h > 7 else h - 2, 0, [(0, 0), (0, 1)], 5)
    cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 0]
    rng.shuffle(cells)
    n6 = rng.randint(4, 6)
    for r, c in cells[:n6]:
        g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_6_cells":
        # only 5-decorations, no 6-cells → rule has nothing to shift
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 5)
        paint_at(g, 5, 7, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
        return g
    if name == "all_6_at_bottom_right":
        # all 6s at bottom-right → shift (+1, +1) puts every 6 out of bounds
        for r, c in [(h - 1, w - 1), (h - 1, w - 2), (h - 2, w - 1)]:
            g[r][c] = 6
        return g
    if name == "no_5_decoration":
        # only scattered 6-cells, no 5-decorations → invariant violated, no decor markers
        for r, c in [(2, 3), (4, 6), (5, 1), (6, 8)]:
            g[r][c] = 6
        return g
    return g

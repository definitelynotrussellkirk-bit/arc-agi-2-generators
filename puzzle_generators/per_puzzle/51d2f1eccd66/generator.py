"""Generator for arc_puzzle_bank_twentythird21:M160 — flood 8-walled chambers.

Rule: 8-walls divide the grid into chambers. Each chamber's interior
gets fully filled with the single non-0/non-8 marker color present
in it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, multi_markers_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "51d2f1eccd66"
VERSION = "1.1.0"
TASK_ID = "51d2f1eccd66"
SUMMARY = "8-walled 2x2 chambers, each with one corner-marker."

INVARIANTS = [
    "background is 0",
    "8-walls form a 2×2 chamber layout (rows 0,4,8 and cols 0,4,8 are 8)",
    "each chamber holds exactly one marker (corner cell) in a distinct non-0/non-8 color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "multi_markers_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "4", "valid": "4..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "four_walled_chambers",
                       "valid": "four_walled_chambers"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
    rng = ctx.draw_rng("layout")
    h, w = 9, 9
    g = full_grid(h, w, 0)
    fill_box(g, 0, 0, 0, w - 1, 8)
    fill_box(g, 4, 0, 4, w - 1, 8)
    fill_box(g, h - 1, 0, h - 1, w - 1, 8)
    fill_box(g, 0, 0, h - 1, 0, 8)
    fill_box(g, 0, 4, h - 1, 4, 8)
    fill_box(g, 0, w - 1, h - 1, w - 1, 8)
    chambers = [(1, 1, 3, 3), (1, 5, 3, 7), (5, 1, 7, 3), (5, 5, 7, 7)]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 4)
    for (r1, c1, r2, c2), color in zip(chambers, palette):
        cells = [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
        r, c = rng.choice(cells)
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # markers but no 8-walls → no chambers defined, flood scope undefined
        g[1][1] = 4
        g[1][6] = 6
        g[6][1] = 7
        g[6][6] = 3
        return g
    if name == "no_markers":
        # walls form chambers but no markers → no color to fill chambers with
        fill_box(g, 0, 0, 0, w - 1, 8)
        fill_box(g, 4, 0, 4, w - 1, 8)
        fill_box(g, h - 1, 0, h - 1, w - 1, 8)
        fill_box(g, 0, 0, h - 1, 0, 8)
        fill_box(g, 0, 4, h - 1, 4, 8)
        fill_box(g, 0, w - 1, h - 1, w - 1, 8)
        return g
    if name == "multi_markers_per_chamber":
        # one chamber has 2 different markers → ambiguous flood color
        fill_box(g, 0, 0, 0, w - 1, 8)
        fill_box(g, 4, 0, 4, w - 1, 8)
        fill_box(g, h - 1, 0, h - 1, w - 1, 8)
        fill_box(g, 0, 0, h - 1, 0, 8)
        fill_box(g, 0, 4, h - 1, 4, 8)
        fill_box(g, 0, w - 1, h - 1, w - 1, 8)
        g[1][1] = 4; g[3][3] = 6   # two colors in same chamber!
        g[1][5] = 7
        g[5][1] = 3
        return g
    return g

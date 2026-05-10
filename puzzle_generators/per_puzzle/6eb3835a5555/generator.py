"""Generator for arc_puzzle_bank_eighteenth21:M125.

5-walls divide the grid into rectangular chambers; chambers whose strict
interior contains exactly one non-0/non-5 color get filled with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, empty_chambers, multiple_colors_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "6eb3835a5555"
VERSION = "1.1.0"
TASK_ID = "6eb3835a5555"
SUMMARY = "5-walled 2x2 chamber layout with one marker per chamber (distinct colors)."

INVARIANTS = [
    "background is 0",
    "5-walls form a 2×2 chamber layout (rows 0,3,6 + cols 0,3,8 are 5)",
    "each chamber holds exactly one marker in a distinct non-0/non-5 color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "empty_chambers", "multiple_colors_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7..7"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "4", "valid": "4..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "five_walls_2x2_chambers",
                       "valid": "five_walls_2x2_chambers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
    h, w = 7, 9
    g = full_grid(h, w, 0)
    fill_box(g, 0, 0, 0, w - 1, 5)
    fill_box(g, 3, 0, 3, w - 1, 5)
    fill_box(g, h - 1, 0, h - 1, w - 1, 5)
    fill_box(g, 0, 0, h - 1, 0, 5)
    fill_box(g, 0, 3, h - 1, 3, 5)
    fill_box(g, 0, w - 1, h - 1, w - 1, 5)
    chambers = [(1, 1, 2, 2), (1, 4, 2, 7), (4, 1, 5, 2), (4, 4, 5, 7)]
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
    for (r1, c1, r2, c2), color in zip(chambers, palette):
        cells = [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
        r, c = rng.choice(cells)
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # markers placed without 5-wall structure → no chambers to fill
        g[2][2] = 4
        g[2][6] = 6
        g[5][2] = 7
        return g
    if name == "empty_chambers":
        # walls drawn but chambers empty → no markers, nothing to fill
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, 3, 0, 3, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        fill_box(g, 0, 3, h - 1, 3, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        return g
    if name == "multiple_colors_per_chamber":
        # one chamber has 2 different markers → "exactly one color" precondition fails
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, 3, 0, 3, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        fill_box(g, 0, 3, h - 1, 3, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        g[1][1] = 4
        g[2][2] = 6  # two different colors in same chamber
        g[1][5] = 7
        return g
    return g

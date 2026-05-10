"""Generator for 15b:hard_101 — fill chambers by dot count legend.

Rule: top row legend gives 3 colors at cols 1, 2, 3. 8-walls form 3
vertical chambers, each containing 1, 2, or 3 dots (always color 1).
Output fills each chamber with the legend color whose position equals
the chamber's dot count.

Combinatorial axes (8): ch_h, ch_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dots, no_legend, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "67a09b7f6b66"
VERSION = "1.1.0"
TASK_ID = "67a09b7f6b66"
SUMMARY = "Top legend (3 colors at cols 1-3) + 3 8-walled chambers with 1/2/3 dots."

INVARIANTS = [
    "background is 0",
    "row 0 cols 1, 2, 3 hold a 3-color legend (distinct colors)",
    "8-walls form 3 vertical chambers below row 1",
    "each chamber holds 1, 2, or 3 isolated dots of color 1; counts are a permutation of {1, 2, 3}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dots", "no_legend", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 6..7", "valid": "5..9"},
    "ch_w":           {"type": "int", "default": "3", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "legend_top_3_chambers_below",
                       "valid": "legend_top_3_chambers_below"},
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
    if difficulty == "easy":
        ch = ctx.draw_int("ch_h", 6, 6)
        cw = ctx.draw_int("ch_w", 3, 3)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 7, 9)
        cw = ctx.draw_int("ch_w", 3, 5)
    else:
        ch = ctx.draw_int("ch_h", 6, 7)
        cw = ctx.draw_int("ch_w", 3, 3)
    rng = ctx.draw_rng("layout")
    h = ch + 3
    w = 3 * cw + 4
    g = full_grid(h, w, 0)
    legend = rng.sample([2, 3, 4, 5, 6, 7, 9], 3)
    for j, v in enumerate(legend):
        g[0][j + 1] = v
    walls_c = [0, cw + 1, 2 * cw + 2, w - 1]
    for c in range(w):
        g[1][c] = 8; g[h - 1][c] = 8
    for r in range(1, h):
        for wc in walls_c: g[r][wc] = 8
    counts = rng.sample([1, 2, 3], 3)
    chamber_cols = [(walls_c[i] + 1, walls_c[i + 1] - 1) for i in range(3)]
    for (c_lo, c_hi), n in zip(chamber_cols, counts):
        cells = [(r, c) for r in range(2, h - 1) for c in range(c_lo, c_hi + 1)]
        slots = rng.sample(cells, n)
        for r, c in slots: g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 6, 3
    h = ch + 3
    w = 3 * cw + 4
    g = full_grid(h, w, 0)
    walls_c = [0, cw + 1, 2 * cw + 2, w - 1]
    if name == "no_dots":
        # Legend + walls but no dots in any chamber — rule's
        # count-to-legend-index lookup has no count to read.
        g[0][1] = 3; g[0][2] = 7; g[0][3] = 4
        for c in range(w):
            g[1][c] = 8; g[h - 1][c] = 8
        for r in range(1, h):
            for wc in walls_c: g[r][wc] = 8
        return g
    if name == "no_legend":
        # Walls + dots but no legend — rule has no count→color mapping.
        for c in range(w):
            g[1][c] = 8; g[h - 1][c] = 8
        for r in range(1, h):
            for wc in walls_c: g[r][wc] = 8
        g[3][1] = 1
        g[3][cw + 2] = 1; g[5][cw + 3] = 1
        return g
    if name == "no_walls":
        # Legend + dots but no 8-walls — chambers are undefined.
        g[0][1] = 3; g[0][2] = 7; g[0][3] = 4
        g[3][2] = 1; g[5][6] = 1
        return g
    return g

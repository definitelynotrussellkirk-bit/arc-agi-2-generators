"""Generator for 14b:hard_94 — fill chambers by legend dot count.

Rule: top row holds a legend of 3 colors. Below row 1, 5-walls form
chambers. Each chamber is filled by legend[dot_count - 1] (and last
legend color if no dots).

Combinatorial axes (8): ch_h, ch_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_walls, no_dots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "952d011ee8be"
VERSION = "1.1.0"
TASK_ID = "952d011ee8be"
SUMMARY = "Top legend (3 colors) + 5-walled chambers with 1/2/3 dots inside."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 contiguous legend colors at cols 1, 2, 3",
    "5-walls form 3 vertical chambers below row 2",
    "each chamber has 1, 2, or 3 isolated 1-color dots; counts permute {1, 2, 3}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_walls", "no_dots")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "ch_w":           {"type": "int", "default": "rng 3..3", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "legend_plus_5wall_chambers",
                       "valid": "legend_plus_5wall_chambers"},
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
    if difficulty == "easy":
        ch = ctx.draw_int("ch_h", 5, 5)
        cw = ctx.draw_int("ch_w", 3, 3)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 6, 7)
        cw = ctx.draw_int("ch_w", 3, 3)
    else:
        ch = ctx.draw_int("ch_h", 5, 7)
        cw = ctx.draw_int("ch_w", 3, 3)
    rng = ctx.draw_rng("layout")
    h = ch + 4
    w = 3 * cw + 4
    g = full_grid(h, w, 0)
    legend = rng.sample([2, 3, 4, 6, 7, 8, 9], 3)
    for j, v in enumerate(legend): g[0][j + 1] = v
    walls_c = [0, cw + 1, 2 * cw + 2, w - 1]
    for c in range(w):
        g[2][c] = 5; g[h - 1][c] = 5
    for r in range(2, h):
        for wc in walls_c: g[r][wc] = 5
    counts = rng.sample([1, 2, 3], 3)
    chamber_cols = [(walls_c[i] + 1, walls_c[i + 1] - 1) for i in range(3)]
    for (c_lo, c_hi), n in zip(chamber_cols, counts):
        cells = [(r, c) for r in range(3, h - 1) for c in range(c_lo, c_hi + 1)]
        slots = rng.sample(cells, n)
        for r, c in slots: g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 5, 3
    h, w = ch + 4, 3 * cw + 4
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # walls + chambers + dots but no top-row legend → no count→color mapping
        walls_c = [0, cw + 1, 2 * cw + 2, w - 1]
        for c in range(w): g[2][c] = 5; g[h - 1][c] = 5
        for r in range(2, h):
            for wc in walls_c: g[r][wc] = 5
        for r, c in [(3, 1), (5, 5), (7, 9)]:
            if 0 <= r < h and 0 <= c < w: g[r][c] = 1
        return g
    if name == "no_walls":
        # legend + dots but no 5-walls → no chambers, dots aren't grouped
        legend = [2, 3, 4]
        for j, v in enumerate(legend): g[0][j + 1] = v
        g[3][1] = 1; g[5][5] = 1; g[7][9] = 1
        return g
    if name == "no_dots":
        # legend + chambers but no dots → all chambers have count=0, ambiguous fill
        legend = [2, 3, 4]
        for j, v in enumerate(legend): g[0][j + 1] = v
        walls_c = [0, cw + 1, 2 * cw + 2, w - 1]
        for c in range(w): g[2][c] = 5; g[h - 1][c] = 5
        for r in range(2, h):
            for wc in walls_c: g[r][wc] = 5
        return g
    return g

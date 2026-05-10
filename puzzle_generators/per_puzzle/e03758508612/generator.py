"""Generator for 21b:hard_145 — fill chambers by seed priority legend.

Rule: top row legend (cols 0-2) ranks 3 colors. 8-walls form 2x2
chambers. Each chamber has 1-2 seeds with colors from legend. Output
fills each chamber with the highest-priority seed color.

Combinatorial axes (8): ch_h, ch_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_seeds, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e03758508612"
VERSION = "1.1.0"
TASK_ID = "e03758508612"
SUMMARY = "Top legend (3 colors) + 2x2 8-walled chambers with 1-2 seeds each."

INVARIANTS = [
    "background is 0",
    "row 0 cols 0..2 hold the 3-color priority legend",
    "8-walls form a 2x2 chamber layout below the legend row",
    "each chamber has 1-2 seed cells using legend colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_seeds", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "ch_w":           {"type": "int", "default": "rng 4..4", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "legend_top_chambers_below",
                       "valid": "legend_top_chambers_below"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        ch = ctx.draw_int("ch_h", 2, 2)
        cw = ctx.draw_int("ch_w", 4, 4)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 3, 4)
        cw = ctx.draw_int("ch_w", 4, 5)
    else:
        ch = ctx.draw_int("ch_h", 2, 3)
        cw = ctx.draw_int("ch_w", 4, 4)
    rng = ctx.draw_rng("layout")
    h = 2 * ch + 4
    w = 2 * cw + 3
    g = full_grid(h, w, 0)
    legend = rng.sample([1, 2, 3, 4, 6, 7, 9], 3)
    for j, v in enumerate(legend): g[0][j] = v
    for c in range(w):
        g[1][c] = 8; g[ch + 2][c] = 8; g[h - 1][c] = 8
    for r in range(1, h):
        g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
    chambers = [(2, 1), (2, cw + 2), (ch + 3, 1), (ch + 3, cw + 2)]
    for rr, cc in chambers:
        n_seeds = rng.randint(1, 2)
        cells = [(r, c) for r in range(rr, rr + ch) for c in range(cc, cc + cw)]
        slots = rng.sample(cells, n_seeds)
        seed_colors = rng.sample(legend, n_seeds)
        for (r, c), color in zip(slots, seed_colors): g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 2, 4
    h = 2 * ch + 4
    w = 2 * cw + 3
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Walls + seeds present but row 0 is empty — rule has no
        # priority ordering to drive the fill choice.
        for c in range(w):
            g[1][c] = 8; g[ch + 2][c] = 8; g[h - 1][c] = 8
        for r in range(1, h):
            g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
        g[3][2] = 4; g[6][7] = 6
        return g
    if name == "no_seeds":
        # Legend + walls but every chamber empty — rule has no seed
        # to pick a chamber color from.
        for j, v in enumerate([1, 2, 3]): g[0][j] = v
        for c in range(w):
            g[1][c] = 8; g[ch + 2][c] = 8; g[h - 1][c] = 8
        for r in range(1, h):
            g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
        return g
    if name == "no_walls":
        # Legend + seeds but no 8-walls — chamber boundaries undefined.
        for j, v in enumerate([1, 2, 3]): g[0][j] = v
        g[3][2] = 1; g[6][7] = 2
        return g
    return g

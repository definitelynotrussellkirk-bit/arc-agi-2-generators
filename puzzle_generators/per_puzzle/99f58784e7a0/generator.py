"""Generator for 21b:m147 — fill each walled chamber from its seed.

Rule: 8-walls form rectangular chambers (a 2x2 layout). Each chamber
has exactly one non-bg seed cell. Output fills each chamber with its
seed color (replacing all bg cells).

Combinatorial axes (8): grid_h, grid_w, palette_kind, ch_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "99f58784e7a0"
VERSION = "1.1.0"
TASK_ID = "99f58784e7a0"
SUMMARY = "8-grid (2x2 chambers) with 1 distinct-color seed per chamber."

INVARIANTS = [
    "background is 0",
    "8-walls form a 2x2 chamber layout (outer frame + 1 horizontal + 1 vertical divider)",
    "each chamber has exactly one non-bg, non-8 seed cell, all 4 colors distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "derived", "valid": "9..15"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ch_h":           {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "8walls_2x2_chambers_with_seeds",
                       "valid": "8walls_2x2_chambers_with_seeds"},
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
        ch = ctx.draw_int("ch_h", 3, 3)
        cw = ctx.draw_int("ch_w", 4, 4)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 4, 4)
        cw = ctx.draw_int("ch_w", 5, 5)
    else:
        ch = ctx.draw_int("ch_h", 3, 4)
        cw = ctx.draw_int("ch_w", 4, 5)
    rng = ctx.draw_rng("layout")
    h = 2 * ch + 3
    w = 2 * cw + 3
    g = full_grid(h, w, 0)
    # outer frame + dividers
    for c in range(w):
        g[0][c] = 8; g[ch + 1][c] = 8; g[h - 1][c] = 8
    for r in range(h):
        g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 4)
    chambers = [(1, 1), (1, cw + 2), (ch + 2, 1), (ch + 2, cw + 2)]
    for color, (rr, cc) in zip(palette, chambers):
        sr = rng.randint(rr, rr + ch - 1)
        sc = rng.randint(cc, cc + cw - 1)
        g[sr][sc] = color
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 3, 4
    h = 2 * ch + 3
    w = 2 * cw + 3
    if name == "no_walls":
        # seeds without 8-walls → no chambers, undefined fill
        g = full_grid(h, w, 0)
        g[2][2] = 4; g[2][7] = 6
        g[6][2] = 7; g[6][7] = 9
        return g
    if name == "no_seeds":
        # walls form chambers but no seeds → nothing to fill with
        g = full_grid(h, w, 0)
        for c in range(w):
            g[0][c] = 8; g[ch + 1][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
        return g
    if name == "multiple_seeds_per_chamber":
        # one chamber has 2 seeds → "exactly one" fails, ambiguous fill
        g = full_grid(h, w, 0)
        for c in range(w):
            g[0][c] = 8; g[ch + 1][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][cw + 1] = 8; g[r][w - 1] = 8
        g[1][1] = 4; g[2][2] = 6  # both in TL chamber
        g[1][cw + 2] = 7
        g[ch + 2][1] = 9
        return g
    return full_grid(h, w, 0)

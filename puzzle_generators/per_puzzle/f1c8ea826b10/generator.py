"""Generator for arc_additional_puzzles_21_set15_bundle:H99 — chamber checker weave.

Rule: 5-walls form chambers. In each chamber the min/max marker colors
generate a checkerboard fill anchored at the chamber's bbox top-left.
Single-color chambers fill solid; empty chambers fill 0; walls unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ch_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, single_color_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f1c8ea826b10"
VERSION = "1.1.0"
TASK_ID = "f1c8ea826b10"

SUMMARY = "5-walls form 2x2 chambers; each chamber holds 2 distinct marker colors."

INVARIANTS = [
    "background is 0",
    "5-walls form a 2x2 chamber layout (outer frame + 1 horizontal + 1 vertical divider)",
    "each chamber has exactly 2 marker cells in distinct non-{0, 5} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "single_color_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "derived", "valid": "9..13"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ch_h":           {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..8"},
    "position_bias":  {"type": "str", "default": "2x2_chambers_2_markers_each",
                       "valid": "2x2_chambers_2_markers_each"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8..8"},
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
    for c in range(w):
        g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
    chambers = [(1, 1), (1, cw + 2), (ch + 2, 1), (ch + 2, cw + 2)]
    for rr, cc in chambers:
        cells = [(r, c) for r in range(rr, rr + ch) for c in range(cc, cc + cw)]
        slots = rng.sample(cells, 2)
        colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
        for (r, c), color in zip(slots, colors):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 3, 4
    h = 2 * ch + 3
    w = 2 * cw + 3
    if name == "no_walls":
        # markers without 5-walls → no chambers, undefined fill
        g = full_grid(h, w, 0)
        g[2][2] = 4; g[3][3] = 6
        g[2][7] = 7; g[3][8] = 8
        g[6][2] = 1; g[7][3] = 2
        g[6][7] = 3; g[7][8] = 9
        return g
    if name == "no_markers":
        # walls form chambers but no markers → all chambers empty, fill 0
        g = full_grid(h, w, 0)
        for c in range(w):
            g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
        return g
    if name == "single_color_per_chamber":
        # each chamber has 1 marker → solid fill, no checkerboard contrast
        g = full_grid(h, w, 0)
        for c in range(w):
            g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
        chambers = [(1, 1), (1, cw + 2), (ch + 2, 1), (ch + 2, cw + 2)]
        cols = [4, 6, 7, 8]
        for (rr, cc), color in zip(chambers, cols):
            g[rr + 1][cc + 1] = color
        return g
    return full_grid(h, w, 0)

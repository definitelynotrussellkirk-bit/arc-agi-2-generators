"""Generator for arc_puzzle_bank_twentieth21:M137 — 1-mask × color-bank.

Rule: an 8-divider column splits the grid. Left = 1-mask (cells are
0 or 1). Right = same-shape grid of colors. Output (same shape as
left/right): mask cell == 1 → take the right's color, else 0.

Combinatorial axes (8): block_h, block_w, palette_kind, n_ones,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, all_zero_mask, all_one_mask.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "834177c803c3"
VERSION = "1.1.0"
TASK_ID = "834177c803c3"
SUMMARY = "Left h×w 1-mask + 8-divider col + right h×w color block."

INVARIANTS = [
    "background is 0",
    "exactly one full-height 8-color divider column",
    "left side is a 0/1 mask of fixed h×w",
    "right side is the same h×w with non-bg colors (no 0s)",
    "left mask has 4-8 ones (so there are non-trivial output cells)",
    "right color block uses 2-4 distinct colors (none are 1 or 8)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "all_zero_mask", "all_one_mask")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "2..5"},
    "block_w":        {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "block_h":        {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "mask_8col_colors",
                       "valid": "mask_8col_colors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..7"},
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
        bh = ctx.draw_int("block_h", 3, 3)
        bw = ctx.draw_int("block_w", 3, 3)
    elif difficulty == "hard":
        bh = ctx.draw_int("block_h", 3, 3)
        bw = ctx.draw_int("block_w", 4, 4)
    else:
        bh = ctx.draw_int("block_h", 3, 3)
        bw = ctx.draw_int("block_w", 3, 4)
    rng = ctx.draw_rng("layout")
    h = bh
    w = bw + 1 + bw  # left | 8-col | right
    g = full_grid(h, w, 0)
    fill_box(g, 0, bw, h - 1, bw, 8)
    n_ones = rng.randint(max(2, bh * bw // 3), bh * bw - 1)
    mask_cells = [(r, c) for r in range(bh) for c in range(bw)]
    rng.shuffle(mask_cells)
    for (r, c) in mask_cells[:n_ones]:
        g[r][c] = 1
    palette = list(random_palette(rng, rng.randint(2, 4), exclude={1, 8}))
    for r in range(bh):
        for c in range(bw):
            g[r][bw + 1 + c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    bh, bw = 3, 3
    h, w = bh, bw + 1 + bw
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # mask + colors but no 8-col separator → can't tell which side is which
        for r in range(bh):
            g[r][0] = 1; g[r][1] = 1
            g[r][bw + 1 + 0] = 4; g[r][bw + 1 + 1] = 6
        return g
    if name == "all_zero_mask":
        # mask is all 0 → output is all 0, rule has no effect
        fill_box(g, 0, bw, h - 1, bw, 8)
        for r in range(bh):
            for c in range(bw):
                g[r][bw + 1 + c] = 4
        return g
    if name == "all_one_mask":
        # mask is all 1 → output is full color block, rule degenerates to copy
        fill_box(g, 0, bw, h - 1, bw, 8)
        for r in range(bh):
            for c in range(bw):
                g[r][c] = 1
                g[r][bw + 1 + c] = 4
        return g
    return g

"""Generator for arc_puzzle_bank_fifth21:H35.

Rows 0 and 1 define a color map, row 2 defines a column mask, and the body is
recolored then cropped to the marked columns.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_mask, blank_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a53fa114c4a9"
VERSION = "1.1.0"
TASK_ID = "a53fa114c4a9"
SUMMARY = "Legend recolor followed by column-mask crop."

INVARIANTS = [
    "rows 0 and 1 contain aligned source/target color pairs",
    "row 2 contains the color-1 keep-column mask",
    "body rows begin at row 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_mask", "blank_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "n_keep":         {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "4..10"},
    "position_bias":  {"type": "str", "default": "legend_mask_body",
                       "valid": "legend_mask_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..8", "valid": "4..10"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
    h, w = 10, 13
    if difficulty == "easy":
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
        n_keep = ctx.draw_int("n_keep", 2, 3)
    elif difficulty == "hard":
        n_pairs = ctx.draw_int("n_pairs", 3, 4)
        n_keep = ctx.draw_int("n_keep", 4, 5)
    else:
        n_pairs = ctx.draw_int("n_pairs", 2, 4)
        n_keep = ctx.draw_int("n_keep", 2, 5)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_pairs * 2)
    srcs = colors[:n_pairs]
    dsts = colors[n_pairs:]
    pair_cols = sorted(rng.sample(range(w), n_pairs))
    keep_cols = sorted(rng.sample(range(w), n_keep))
    g = full_grid(h, w, 0)
    for c, src, dst in zip(pair_cols, srcs, dsts):
        g[0][c] = src
        g[1][c] = dst
    for c in keep_cols:
        g[2][c] = 1
    for r in range(3, h):
        for c in range(w):
            if rng.random() < 0.42:
                g[r][c] = rng.choice(srcs)
    for i, c in enumerate(keep_cols):
        g[3 + (i % (h - 3))][c] = srcs[i % len(srcs)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # mask + body but no row-0/1 legend → no recolor mapping defined
        for c in [2, 5, 8]: g[2][c] = 1
        for r in range(3, h):
            for c in range(w):
                if (r + c) % 3 == 0: g[r][c] = 4
        return g
    if name == "no_mask":
        # legend + body but no row-2 mask → no columns to keep
        g[0][2] = 4; g[1][2] = 6
        for r in range(3, h):
            for c in range(w):
                if (r + c) % 3 == 0: g[r][c] = 4
        return g
    if name == "blank_body":
        # legend + mask but body all-zero → recolor + crop yields blank
        g[0][2] = 4; g[1][2] = 6
        for c in [2, 5, 8]: g[2][c] = 1
        return g
    return g

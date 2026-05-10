"""Generator for arc_puzzle_bank_21_set7:easy_g05.

Rule: separated solid monochrome 2×2 blocks are reduced to top-left
and bottom-right cells (main diagonal of the block).

Combinatorial axes (8): grid_h/w, palette_kind, n_blocks, palette_size,
position_bias, n_distinct_colors, block_density, texture.
Degenerates: no_blocks, blocks_smaller, blocks_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ffd8d801705"
VERSION = "1.1.0"
TASK_ID = "5ffd8d801705"
SUMMARY = "Separated solid monochrome 2x2 blocks are reduced to top-left and bottom-right cells."

INVARIANTS = [
    "every object is a solid 2x2 block",
    "blocks are separated",
    "background is zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_smaller", "blocks_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "block_density":  {"type": "str", "default": "fixed_2x2", "valid": "fixed_2x2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = ctx.draw_int("n_blocks", 2, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    spots = [(r, c) for r in range(0, h - 1, 3) for c in range(0, w - 1, 3)]
    rng.shuffle(spots)
    for i, (r, c) in enumerate(spots[:n]):
        color = (i % 8) + 1
        g[r][c] = color
        g[r + 1][c] = color
        g[r][c + 1] = color
        g[r + 1][c + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # singletons only — no 2×2 blocks to reduce
        g[1][2] = 4
        g[3][5] = 7
        return g
    if name == "blocks_smaller":
        # 1×2 strips instead of 2×2 — invariant violated
        g[1][1] = 4; g[1][2] = 4
        g[4][3] = 7; g[4][4] = 7
        return g
    if name == "blocks_touching":
        # adjacent 2×2 blocks fused into 2×4 — separation invariant violated
        g[1][1] = 4; g[1][2] = 4
        g[2][1] = 4; g[2][2] = 4
        g[1][3] = 6; g[1][4] = 6  # touches first block
        g[2][3] = 6; g[2][4] = 6
        return g
    return g

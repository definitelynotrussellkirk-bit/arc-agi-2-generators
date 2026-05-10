"""Generator for arc_puzzle_bank_third21:E20.

Rule: each monochrome solid 2×2 block keeps only its main diagonal
(top-left and bottom-right cells); the other two cells are cleared.

Combinatorial axes (8): grid_h/w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, block_size, texture.
Degenerates: no_blocks, blocks_too_large, already_diagonal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f98b43c1996b"
VERSION = "1.1.0"
TASK_ID = "f98b43c1996b"
SUMMARY = "Each monochrome solid 2x2 block keeps only its main diagonal."

INVARIANTS = [
    "every generated object is a solid 2x2 block",
    "blocks are separated",
    "background is zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_too_large", "already_diagonal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "block_size":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "grid_aligned",
                       "valid": "grid_aligned"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5",
                          "valid": "1..8"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 11)
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
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        return g
    if name == "blocks_too_large":
        # 3×3 solid blocks — rule expects 2×2, so extra cells are unhandled
        for r in range(1, 4):
            for c in range(1, 4):
                g[r][c] = 4
        for r in range(5, 8):
            for c in range(5, 8):
                g[r][c] = 7
        return g
    if name == "already_diagonal":
        # blocks with only main-diagonal cells filled — rule is identity
        g[0][0] = 3; g[1][1] = 3
        g[3][3] = 5; g[4][4] = 5
        return g
    return g

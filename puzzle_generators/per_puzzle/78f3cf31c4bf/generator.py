"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p04.

Combinatorial axes (8): grid_h, grid_w, palette_kind, block_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, full_block, dense_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "78f3cf31c4bf"
VERSION = "1.1.0"
TASK_ID = "78f3cf31c4bf"
SUMMARY = "Separated 2x2 blocks have three same-color cells and one blank corner."

INVARIANTS = [
    "background is 0",
    "each active 2x2 window has exactly three cells of one color",
    "active 2x2 windows are separated by at least one background cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "full_block", "dense_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "block_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "scattered_separated",
                       "valid": "scattered_separated"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_neighborhood(grid, r0, c0):
    h = len(grid)
    w = len(grid[0])
    for r in range(max(0, r0 - 1), min(h, r0 + 3)):
        for c in range(max(0, c0 - 1), min(w, c0 + 3)):
            if grid[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        block_count = ctx.draw_int("block_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        block_count = ctx.draw_int("block_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        block_count = ctx.draw_int("block_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h - 1) for c in range(w - 1)]
    rng.shuffle(positions)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], block_count)
    placed = 0

    for r0, c0 in positions:
        if placed >= block_count:
            break
        if not _clear_neighborhood(grid, r0, c0):
            continue
        missing = rng.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
        color = colors[placed]
        for dr in range(2):
            for dc in range(2):
                if (dr, dc) != missing:
                    grid[r0 + dr][c0 + dc] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # Empty grid — rule has no incomplete corners to fill.
        return g
    if name == "full_block":
        # 2x2 already complete — nothing to fill, rule is no-op.
        for dr in range(2):
            for dc in range(2): g[1 + dr][1 + dc] = 4
        return g
    if name == "dense_blocks":
        # Two 3-of-4 blocks adjacent without separator — corners overlap.
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[1][3] = 5; g[1][4] = 5; g[2][4] = 5
        return g
    return g

"""Generator for arc_puzzle_bank_21_set23_bundle:easy_p03.

Rule: isolated solid 3x3 blocks → only their cross cores (cells with 4
same-color cardinal neighbors) survive.

Combinatorial axes (8): grid_h, grid_w, palette_kind, block_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, blocks_at_edge, partial_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d191ce876ab"
VERSION = "1.1.0"
TASK_ID = "0d191ce876ab"
SUMMARY = "Isolated monochrome 3x3 blocks leave only their cross cores."

INVARIANTS = [
    "background is 0",
    "each object is an isolated solid 3x3 monochrome block",
    "only cells with four same-color cardinal neighbors survive",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_at_edge", "partial_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..15"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "block_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_blocks",
                       "valid": "spaced_3x3_blocks"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _blocked_area(r0: int, c0: int) -> set[tuple[int, int]]:
    return {(r, c) for r in range(r0 - 1, r0 + 4) for c in range(c0 - 1, c0 + 4)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        block_count = ctx.draw_int("block_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        block_count = ctx.draw_int("block_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        block_count = ctx.draw_int("block_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(1, h - 3) for c in range(1, w - 3)]
    rng.shuffle(anchors)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(block_count, 9))
    occupied: set[tuple[int, int]] = set()

    placed = 0
    for r0, c0 in anchors:
        blocked = _blocked_area(r0, c0)
        if blocked & occupied:
            continue
        color = colors[placed % len(colors)]
        for r in range(r0, r0 + 3):
            for c in range(c0, c0 + 3):
                grid[r][c] = color
        occupied |= blocked
        placed += 1
        if placed >= block_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank grid → no cross-cores to keep, output is empty
        return g
    if name == "blocks_at_edge":
        # 3x3 blocks placed at the grid border → center cells lack 4 cardinal same-color neighbors
        # because one side reaches outside; cross core may not survive
        for r in range(0, 3):
            for c in range(0, 3): g[r][c] = 4
        for r in range(h - 3, h):
            for c in range(w - 3, w): g[r][c] = 6
        return g
    if name == "partial_blocks":
        # blocks are 2x2 (not 3x3) → no cell has 4 cardinal same-color neighbors
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(5, 7):
            for c in range(6, 8): g[r][c] = 6
        return g
    return g

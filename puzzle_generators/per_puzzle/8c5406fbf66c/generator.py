"""Generator for arc_puzzle_bank_next21:E13.

Rule: place separated solid 2x2 blocks; their top-left cells become 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, blocks_already_have_8, fragmented_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8c5406fbf66c"
VERSION = "1.1.0"
TASK_ID = "8c5406fbf66c"
SUMMARY = "Place separated solid 2x2 blocks whose top-left cells become 8."

INVARIANTS = [
    "background is 0",
    "each active window is a solid same-color 2x2 block",
    "block colors are nonzero and not 8",
    "active windows are separated to avoid overlapping anchors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_already_have_8", "fragmented_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blocks":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spaced_blocks",
                       "valid": "spaced_blocks"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        target = ctx.draw_int("blocks", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("blocks", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
        target = ctx.draw_int("blocks", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r0 = rng.randint(0, h - 2)
        c0 = rng.randint(0, w - 2)
        guard = {
            (r, c)
            for r in range(max(0, r0 - 1), min(h, r0 + 3))
            for c in range(max(0, c0 - 1), min(w, c0 + 3))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for dr in [0, 1]:
            for dc in [0, 1]:
                g[r0 + dr][c0 + dc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank grid → no 2x2 anchors, rule is identity
        return g
    if name == "blocks_already_have_8":
        # 2x2 blocks of color 8 → top-left already 8, rule is identity
        for dr in [0, 1]:
            for dc in [0, 1]: g[1 + dr][1 + dc] = 8
        for dr in [0, 1]:
            for dc in [0, 1]: g[4 + dr][5 + dc] = 8
        return g
    if name == "fragmented_blocks":
        # color blocks that aren't solid 2x2 (L-shapes, partial squares) → no anchor pattern matches
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4   # L (3 cells, no 2x2)
        g[4][5] = 6; g[5][5] = 6; g[5][6] = 6   # mirrored L
        return g
    return g

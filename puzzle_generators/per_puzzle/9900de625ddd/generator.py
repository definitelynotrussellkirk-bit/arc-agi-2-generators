"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:easy_144_reduce_solid_3x3_blocks_to_centers.

Rule: solid monochrome 3x3 blocks are reduced to their center cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, blocks_2x2, blocks_4x4.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9900de625ddd"
VERSION = "1.1.0"
TASK_ID = "9900de625ddd"
SUMMARY = "Solid monochrome 3x3 blocks are reduced to their center cells."

INVARIANTS = [
    "background is 0",
    "each object is a complete 3x3 block",
    "blocks are separated so no extra 3x3 windows appear",
    "output is blank except for block centers",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_2x2", "blocks_4x4")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blocks":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_blocks",
                       "valid": "spaced_3x3_blocks"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0):
    h, w = len(g), len(g[0])
    if r0 < 0 or c0 < 0 or r0 + 2 >= h or c0 + 2 >= w:
        return False
    for r in range(max(0, r0 - 1), min(h, r0 + 4)):
        for c in range(max(0, c0 - 1), min(w, c0 + 4)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        target = ctx.draw_int("blocks", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
        target = ctx.draw_int("blocks", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("blocks", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(120):
        if placed >= target:
            break
        r0 = rng.randint(0, h - 3)
        c0 = rng.randint(0, w - 3)
        if not _free(g, r0, c0):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(r0, r0 + 3):
            for c in range(c0, c0 + 3):
                g[r][c] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank grid → no 3x3 blocks, rule fires zero times
        return g
    if name == "blocks_2x2":
        # 2x2 blocks instead of 3x3 → no solid 3x3 window, rule fires zero times
        for r in range(1, 3):
            for c in range(1, 3): g[r][c] = 4
        for r in range(5, 7):
            for c in range(6, 8): g[r][c] = 6
        return g
    if name == "blocks_4x4":
        # 4x4 blocks → multiple overlapping 3x3 windows match; ambiguous which gets reduced
        for r in range(1, 5):
            for c in range(1, 5): g[r][c] = 4
        for r in range(6, 10):
            for c in range(7, 11): g[r][c] = 6
        return g
    return g

"""Generator for arc_puzzle_bank_21_set2:S2_E5.

Almost-full 2x2 cyan blocks are completed by filling the missing corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, block_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, full_2x2, single_cell_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "552c2402dce3"
VERSION = "1.1.0"
TASK_ID = "552c2402dce3"

SUMMARY = "Almost-full 2x2 cyan blocks are completed by filling the missing corner."

INVARIANTS = [
    "background is 0",
    "each target pattern is a 2x2 window with exactly three cyan cells",
    "target 2x2 windows are separated from each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "full_2x2", "single_cell_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "block_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_l_blocks",
                       "valid": "separated_l_blocks"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CORNERS = [(0, 0), (0, 1), (1, 0), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("block_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        count = ctx.draw_int("block_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        count = ctx.draw_int("block_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    anchors = []
    for _ in range(count):
        for _attempt in range(300):
            r0 = rng.randint(0, h - 2)
            c0 = rng.randint(0, w - 2)
            if any(abs(r0 - rr) <= 2 and abs(c0 - cc) <= 2 for rr, cc in anchors):
                continue
            if any(g[r0 + dr][c0 + dc] != 0 for dr, dc in _CORNERS):
                continue
            missing = rng.choice(_CORNERS)
            for dr, dc in _CORNERS:
                if (dr, dc) != missing:
                    g[r0 + dr][c0 + dc] = 8
            anchors.append((r0, c0))
            break
        else:
            raise ValueError("could not place almost-square")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank → no L-blocks to complete
        return g
    if name == "full_2x2":
        # 2x2 already full → no missing corner to fill
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 8
        return g
    if name == "single_cell_blocks":
        # only one cell of cyan per "block" → "exactly 3 cells" precondition fails
        g[1][1] = 8
        g[4][5] = 8
        return g
    return g

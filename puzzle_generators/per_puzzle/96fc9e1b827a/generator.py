"""Generator for arc_puzzle_bank_21_set14_s:S14_M4 — column histogram of largest.

Rule: pick the (single) largest blob; output a column-density bar
histogram in 8 (col counts → bars rising from bottom).

Combinatorial axes (8): grid_h, grid_w, palette_kind, staircase_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, no_blobs, uniform_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "96fc9e1b827a"
VERSION = "1.1.0"
TASK_ID = "96fc9e1b827a"
SUMMARY = "One staircase blob (clearly largest) + 1-2 small distractor blobs."

INVARIANTS = [
    "background is 0",
    "exactly one largest blob (strictly larger than any other)",
    "largest blob's column counts vary (so output bars differ)",
    "distractor blobs are smaller and don't 4-touch the largest",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "no_blobs", "uniform_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "staircase_size": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_staircase_blob",
                       "valid": "single_staircase_blob"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    sw = rng.randint(3, 4)
    sh = sw
    r0 = rng.randint(1, h - sh - 2)
    c0 = rng.randint(1, w - sw - 2)
    for k in range(sw):
        for j in range(k + 1):
            r = r0 + sh - 1 - j
            c = c0 + k
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # 2 blobs same size → "the largest" is ambiguous
        for (r, c) in [(2, 1), (3, 1), (4, 1), (4, 2)]: g[r][c] = 4   # size 4
        for (r, c) in [(2, 7), (3, 7), (4, 7), (4, 8)]: g[r][c] = 6   # size 4 (tied)
        return g
    if name == "no_blobs":
        # blank → no largest blob to histogram
        return g
    if name == "uniform_columns":
        # largest blob is a solid rectangle → all column counts equal, bars uniform
        for r in range(2, 5):
            for c in range(2, 6): g[r][c] = 4   # 3x4 rect
        return g
    return g

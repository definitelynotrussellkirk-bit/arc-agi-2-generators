"""Generator for arc_puzzle_bank_21_set3:S3_M1 — point reflect around 5-pivot.

Rule: 5 = pivot. Each non-{0,5} cell stays AND its reflection through
the pivot is also painted.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_blob, blob_already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "38200022d1b7"
VERSION = "1.1.0"
TASK_ID = "38200022d1b7"
SUMMARY = "5-pivot at center + a small blob in upper-left whose reflection lands in lower-right."

INVARIANTS = [
    "background is 0",
    "exactly one 5-cell at grid center",
    "non-5 blob fully on one side; reflection in-bounds and disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_blob", "blob_already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "pivot_with_one_side_blob",
                       "valid": "pivot_with_one_side_blob"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    pr = h // 2; pc = w // 2
    g[pr][pc] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    for color in palette:
        for _ in range(40):
            r = rng.randint(0, pr - 1)
            c = rng.randint(0, pc - 1)
            mr = 2 * pr - r; mc = 2 * pc - c
            if not (0 <= mr < h and 0 <= mc < w):
                continue
            if g[r][c] != 0 or g[mr][mc] != 0:
                continue
            g[r][c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    pr, pc = h // 2, w // 2
    if name == "no_pivot":
        # cells exist but no 5-pivot → no point of reflection defined
        g[1][2] = 4
        g[2][3] = 6
        return g
    if name == "no_blob":
        # pivot only, no other cells → no reflection content
        g[pr][pc] = 5
        return g
    if name == "blob_already_symmetric":
        # cells already point-symmetric around pivot → rule is identity
        g[pr][pc] = 5
        g[1][2] = 4; g[h - 2][w - 3] = 4
        g[2][6] = 6; g[h - 3][w - 7] = 6
        return g
    return g

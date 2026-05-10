"""Generator for arc_puzzle_bank_21_set5_e:medium_e04 — extract odd-one-out shape.

Rule: N+1 blobs total, N of them share normalized shape, exactly one
has a unique shape. Output: that unique blob, cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_unique, all_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    L_TROMINO_NE, L_TROMINO_SE, T_TETROMINO, SQUARE_2X2,
)

GENERATOR_ID = "2b638b6cbbc8"
VERSION = "1.1.0"
TASK_ID = "2b638b6cbbc8"
SUMMARY = "2 same-shape blobs + 1 unique-shape blob, distinct colors."

INVARIANTS = [
    "background is 0",
    "exactly 3 blobs: 2 with identical normalized shape + 1 unique",
    "all 3 distinct colors, blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_unique", "all_same")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_same_one_unique",
                       "valid": "two_same_one_unique"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _bbox(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _free(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        rr, cc = r0 + r, c0 + c
        if not (0 <= rr < h and 0 <= cc < w):
            return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    common = rng.choice([L_TROMINO_NE, L_TROMINO_SE])
    unique = T_TETROMINO if common is not T_TETROMINO else SQUARE_2X2
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    placements = [(common, palette[0]), (common, palette[1]), (unique, palette[2])]
    rng.shuffle(placements)
    for shape, color in placements:
        sh, sw = _bbox(shape)
        for _ in range(40):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            if _free(g, r0, c0, shape):
                paint_at(g, r0, c0, shape, color)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no candidates to compare.
        return g
    if name == "all_unique":
        # All three blobs have distinct shapes — rule's "majority
        # share a shape" precondition fails; odd-one-out undefined.
        paint_at(g, 1, 1, L_TROMINO_NE, 4)
        paint_at(g, 1, 5, T_TETROMINO, 6)
        paint_at(g, 4, 1, SQUARE_2X2, 7)
        return g
    if name == "all_same":
        # All three blobs share the same shape — rule's "exactly
        # one unique" finds none.
        paint_at(g, 1, 1, L_TROMINO_NE, 4)
        paint_at(g, 1, 5, L_TROMINO_NE, 6)
        paint_at(g, 4, 1, L_TROMINO_NE, 7)
        return g
    return g

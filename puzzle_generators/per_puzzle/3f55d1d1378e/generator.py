"""Generator for arc_puzzle_bank_21_set15_bundle:medium_o06 — keep translated duplicates.

Rule: blobs whose normalized shape (color-blind, ignoring rotation)
appears at least twice are kept; others are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_unique, all_same_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    SQUARE_2X2, L_TROMINO_NE, L_TROMINO_SE, T_TETROMINO,
)

GENERATOR_ID = "3f55d1d1378e"
VERSION = "1.1.0"
TASK_ID = "3f55d1d1378e"
SUMMARY = "Two same-shape blobs (different colors) + one unique-shape distractor."

INVARIANTS = [
    "background is 0",
    "exactly two blobs share the same normalized shape (kept)",
    "≥1 blob has a unique shape (erased)",
    "blobs are 4-disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_unique", "all_same_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "duplicate_with_unique",
                       "valid": "duplicate_with_unique"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shared_shape = rng.choice([SQUARE_2X2, L_TROMINO_SE])
    other_shape = T_TETROMINO if shared_shape != T_TETROMINO else L_TROMINO_NE
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    placements = [(shared_shape, palette[0]), (shared_shape, palette[1]), (other_shape, palette[2])]
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
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no candidates to count.
        return g
    if name == "all_unique":
        # All shapes distinct — rule's "appears at least twice"
        # filter excludes everything; output empty.
        paint_at(g, 1, 1, T_TETROMINO, 4)
        paint_at(g, 1, 7, L_TROMINO_NE, 6)
        paint_at(g, 5, 1, SQUARE_2X2, 7)
        return g
    if name == "all_same_shape":
        # All blobs share one shape — rule's "keep duplicates"
        # branch keeps everything; output equals input.
        paint_at(g, 1, 1, SQUARE_2X2, 4)
        paint_at(g, 1, 7, SQUARE_2X2, 6)
        paint_at(g, 5, 4, SQUARE_2X2, 7)
        return g
    return g

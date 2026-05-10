"""Generator for 3b:m18 — rotate each L-triomino CW.

Rule: every L-triomino blob (3-cell L shape) gets rotated 90° CW
within its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, non_l_blobs, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    L_TROMINO_NE, L_TROMINO_NW, L_TROMINO_SE, L_TROMINO_SW,
)

GENERATOR_ID = "371eb0221101"
VERSION = "1.1.0"
TASK_ID = "371eb0221101"
SUMMARY = "2-3 L-tromino blobs in distinct colors."

INVARIANTS = [
    "background is 0",
    "every blob is a 3-cell L-tromino",
    "blobs don't 4-touch (with 1-cell padding)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "non_l_blobs", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered_isolated",
                       "valid": "scattered_isolated"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        rr, cc = r0 + r, c0 + c
        if not (0 <= rr < h and 0 <= cc < w): return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    Ls = [L_TROMINO_NE, L_TROMINO_NW, L_TROMINO_SE, L_TROMINO_SW]
    for color in palette:
        L = rng.choice(Ls)
        for _ in range(40):
            r0 = rng.randint(0, h - 2)
            c0 = rng.randint(0, w - 2)
            if _free(g, r0, c0, L):
                paint_at(g, r0, c0, L, color)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has nothing to rotate.
        return g
    if name == "non_l_blobs":
        # Solid 2x2 squares and straight lines, no L-trominoes — rule's L
        # match never fires, so the rule is a no-op (output == input).
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[5 + dr][5 + dc] = 6
        return g
    if name == "single_blob":
        # Just one L-tromino — there's no diversity of L orientations.
        for dr, dc in L_TROMINO_NE:
            g[2 + dr][4 + dc] = 5
        return g
    return g

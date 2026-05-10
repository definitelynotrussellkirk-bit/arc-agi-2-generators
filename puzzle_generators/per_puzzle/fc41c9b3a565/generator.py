"""Generator for arc_puzzle_bank_21_set7:medium_g10 — keep only 180-symmetric blobs.

Rule: keep blobs whose normalized cells are point-symmetric (180°);
drop the rest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_symmetric, all_asymmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    SQUARE_2X2, PLUS_5, L_TROMINO_NE, L_TROMINO_SE,
)

GENERATOR_ID = "fc41c9b3a565"
VERSION = "1.1.0"
TASK_ID = "fc41c9b3a565"
SUMMARY = "≥1 180-symmetric blob (kept) + ≥1 asymmetric blob (dropped)."

INVARIANTS = [
    "background is 0",
    "≥1 blob is 180-symmetric (e.g. 2x2 square or plus)",
    "≥1 blob is non-180-symmetric (L-tromino)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_symmetric", "all_asymmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "mixed_180_symmetry_blobs",
                       "valid": "mixed_180_symmetry_blobs"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sym_shape = rng.choice([SQUARE_2X2, PLUS_5])
    asym_shape = rng.choice([L_TROMINO_NE, L_TROMINO_SE])
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    placements = [(sym_shape, palette[0]), (asym_shape, palette[1]), (asym_shape, palette[2])]
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
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no candidates to filter.
        return g
    if name == "all_symmetric":
        # All blobs 180-symmetric — rule's drop branch never fires;
        # output equals input.
        paint_at(g, 1, 1, PLUS_5, 4)
        paint_at(g, 4, 6, SQUARE_2X2, 6)
        return g
    if name == "all_asymmetric":
        # All blobs 180-asymmetric — rule's keep branch finds
        # nothing; output empty.
        paint_at(g, 1, 1, L_TROMINO_NE, 4)
        paint_at(g, 5, 6, L_TROMINO_SE, 6)
        return g
    return g

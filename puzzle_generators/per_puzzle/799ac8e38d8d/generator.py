"""Generator for arc_puzzle_bank_21_set20_bundle:medium_p01 — orientation recolor.

Rule: each blob's bbox: w > h → 2 (horizontal), h > w → 3 (vertical),
else (square) → 4. Output keeps blob shapes, only colors change.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_squares, all_same_orientation, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import SQUARE_2X2, H_LINE_3, V_LINE_3

GENERATOR_ID = "799ac8e38d8d"
VERSION = "1.1.0"
TASK_ID = "799ac8e38d8d"
SUMMARY = "Three blobs, one each: wider, taller, square (so all three branches fire)."

INVARIANTS = [
    "background is 0",
    ">=1 horizontal blob (w > h), >=1 vertical blob (h > w), >=1 square (h = w)",
    "input colors aren't already the orientation colors (rule isn't identity)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_squares", "all_same_orientation", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _bbox_dims(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _free_at(g, r0, c0, cells):
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([5, 6, 7, 8, 9], 3)
    shapes = [H_LINE_3, V_LINE_3, SQUARE_2X2]
    rng.shuffle(palette)
    for shape, color in zip(shapes, palette):
        sh, sw = _bbox_dims(shape)
        for _ in range(40):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            if _free_at(g, r0, c0, shape):
                paint_at(g, r0, c0, shape, color)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "all_squares":
        # all blobs are squares → every output cell becomes 4, no orientation contrast
        paint_at(g, 1, 1, SQUARE_2X2, 5)
        paint_at(g, 4, 5, SQUARE_2X2, 6)
        paint_at(g, 6, 9, SQUARE_2X2, 7)
        return g
    if name == "all_same_orientation":
        # only horizontal blobs → only color 2 fires, no 3 or 4 contrast
        paint_at(g, 1, 1, H_LINE_3, 5)
        paint_at(g, 4, 5, H_LINE_3, 6)
        paint_at(g, 7, 8, H_LINE_3, 7)
        return g
    if name == "no_blobs":
        # empty grid → no objects to recolor, rule no-op
        return g
    return g

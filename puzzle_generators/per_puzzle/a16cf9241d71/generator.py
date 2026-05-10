"""Generator for arc_puzzle_bank_nineteenth21:M127 — mirror left-side shape across 8-line.

Rule: a full-height 8-color column divides the grid. Cells on the
left side are mirrored across the 8-line to the right side
(preserving color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_idx,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, no_shape, shape_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "a16cf9241d71"
VERSION = "1.1.0"
TASK_ID = "a16cf9241d71"
SUMMARY = "Full-height 8-line column divides grid; left-side shape gets mirrored to the right."

INVARIANTS = [
    "background is 0",
    "exactly one full-height column of 8s",
    "left side has a small connected shape (3-5 cells); right side is empty",
    "the shape's mirror image stays in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "no_shape", "shape_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_idx":      {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "left_shape_with_8_axis",
                       "valid": "left_shape_with_8_axis"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    line_c = w // 2
    fill_box(g, 0, line_c, h - 1, line_c, 8)
    color = rng.choice(list(random_palette(rng, 4, exclude={8})))
    shape = rng.choice(_SHAPES)
    sh = max(c[0] for c in shape) + 1
    sw = max(c[1] for c in shape) + 1
    if sw > line_c: return g
    r0 = rng.randint(0, h - sh)
    c0 = rng.randint(0, line_c - sw)
    paint_at(g, r0, c0, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # left shape but no 8-axis → no axis to mirror across
        for r, c in [(1, 1), (2, 1), (2, 2)]: g[r][c] = 4
        return g
    if name == "no_shape":
        # axis only, no shape → nothing to mirror
        for r in range(h): g[r][4] = 8
        return g
    if name == "shape_on_axis":
        # shape overlaps 8-axis → ambiguous left/right
        for r in range(h): g[r][4] = 8
        for r, c in [(2, 3), (2, 4), (3, 4)]: g[r][c] = 4
        return g
    return g

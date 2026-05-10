"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_45_draw_border_from_corners.

Rule: four same-color corner cells define a rectangle border to draw.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_h, rect_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_3_corners, mismatched_corners, degenerate_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d83ca4e3fa19"
VERSION = "1.1.0"
TASK_ID = "d83ca4e3fa19"
SUMMARY = "Four same-color corner cells define a rectangle border to draw."

INVARIANTS = [
    "background is 0",
    "exactly four nonzero cells are present",
    "the four cells are the corners of one axis-aligned rectangle",
    "all corner cells share one color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_3_corners", "mismatched_corners", "degenerate_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_h":         {"type": "int", "default": "rng 3..6", "valid": "2..16"},
    "rect_w":         {"type": "int", "default": "rng 3..7", "valid": "2..18"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_4corner_rectangle",
                       "valid": "single_4corner_rectangle"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        rh = min(ctx.draw_int("rect_h", 3, 4), h)
        rw = min(ctx.draw_int("rect_w", 3, 5), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        rh = min(ctx.draw_int("rect_h", 5, 6), h)
        rw = min(ctx.draw_int("rect_w", 6, 7), w)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 12)
        rh = min(ctx.draw_int("rect_h", 3, 6), h)
        rw = min(ctx.draw_int("rect_w", 3, 7), w)
    rng = ctx.draw_rng("layout")
    r0 = rng.randint(0, h - rh)
    c0 = rng.randint(0, w - rw)
    r1 = r0 + rh - 1
    c1 = c0 + rw - 1
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, 0)
    for r, c in ((r0, c0), (r0, c1), (r1, c0), (r1, c1)):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "only_3_corners":
        # only 3 corners present → 4th corner missing, rect underdetermined
        g[1][1] = 4
        g[1][7] = 4
        g[5][1] = 4
        return g
    if name == "mismatched_corners":
        # 4 corners but different colors → not all-same-color
        g[1][1] = 4; g[1][7] = 6
        g[5][1] = 3; g[5][7] = 7
        return g
    if name == "degenerate_rect":
        # corners are colinear (rh=1) → no real border, just a single line
        g[3][1] = 4; g[3][7] = 4
        g[3][1] = 4; g[3][7] = 4   # same row twice (only 2 distinct cells)
        return g
    return g

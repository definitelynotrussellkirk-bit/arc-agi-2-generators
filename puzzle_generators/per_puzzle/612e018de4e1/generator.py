"""Generator for arc_additional_puzzle_bank_volume14:E92.

Rule: three blue corners of an axis-aligned rectangle imply a red
fourth corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, missing_corner,
rect_size, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_two_corners, four_corners, non_aligned_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "612e018de4e1"
VERSION = "1.1.0"
TASK_ID = "612e018de4e1"
SUMMARY = "Three blue corners of an axis-aligned rectangle imply a red fourth corner."

INVARIANTS = [
    "background is 0",
    "exactly three blue cells mark rectangle corners",
    "the missing fourth rectangle corner is initially empty",
    "rectangle height and width vary independently",
]

PALETTE_KINDS = ("default", "missing_tl", "missing_tr", "missing_bl_or_br")
DEGENERATE_TEXTURES = ("only_two_corners", "four_corners", "non_aligned_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 7..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "missing_corner": {"type": "str", "default": "rng",
                       "valid": "tl|tr|bl|br"},
    "rect_size":      {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rect_corners", "valid": "rect_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 13)
        w = ctx.draw_int("grid_w", 7, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    r0 = rng.randint(0, h - 4)
    r1 = rng.randint(r0 + 2, h - 1)
    c0 = rng.randint(0, w - 4)
    c1 = rng.randint(c0 + 2, w - 1)
    corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
    missing = rng.choice(corners)
    for r, c in corners:
        if (r, c) != missing:
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "only_two_corners":
        # only 2 corners marked → rectangle is underdetermined
        g[1][1] = 1
        g[1][6] = 1
        return g
    if name == "four_corners":
        # all 4 corners present → rule has no missing corner to infer
        for r, c in [(1, 1), (1, 6), (6, 1), (6, 6)]:
            g[r][c] = 1
        return g
    if name == "non_aligned_corners":
        # 3 cells but they don't share rows or columns → no axis-aligned rectangle
        for r, c in [(1, 1), (3, 4), (6, 7)]:
            g[r][c] = 1
        return g
    return g

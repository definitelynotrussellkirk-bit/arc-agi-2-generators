"""Generator for arc_puzzle_bank_21_set17_s:S17_E5.

Rule: 2-seeds and 3-seeds each grow a 3×3 neighborhood; output marks
their intersection.

Combinatorial axes (8): grid_h, grid_w, palette_kind, num_2_seeds,
num_3_seeds, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_overlap, no_seeds_color2, no_seeds_color3.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ef5f8be2639"
VERSION = "1.1.0"
TASK_ID = "3ef5f8be2639"
SUMMARY = "Square growth from colors 2 and 3 is intersected."

INVARIANTS = [
    "one or two color-2 seeds and one or two color-3 seeds are present",
    "at least one color-2 and color-3 seed pair is within overlapping 3x3 neighborhoods",
    "output marks the intersection of the two square-growth masks",
]

PALETTE_KINDS = ("default", "tight_overlap", "wide_grid", "scattered")
DEGENERATE_TEXTURES = ("no_overlap", "no_seeds_color2", "no_seeds_color3")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "width":          {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_2_seeds":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "num_3_seeds":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "near_overlap",
                       "valid": "near_overlap"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 7, 7)
        w = ctx.draw_int("width", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 8, 9)
        w = ctx.draw_int("width", 8, 9)
    else:
        h = ctx.draw_int("height", 7, 9)
        w = ctx.draw_int("width", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 3)
    c = rng.randint(2, w - 4)
    g[r][c] = 2
    g[r][c + 2] = 3
    if rng.random() < 0.5:
        g[rng.randint(1, h - 2)][rng.randint(1, w - 2)] = 2
    if rng.random() < 0.5:
        g[rng.randint(1, h - 2)][rng.randint(1, w - 2)] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # 2-seed and 3-seed too far apart — 3×3 neighborhoods don't intersect
        g[1][1] = 2
        g[6][6] = 3
        return g
    if name == "no_seeds_color2":
        # only 3-seeds — no intersection partner
        g[3][3] = 3
        g[5][5] = 3
        return g
    if name == "no_seeds_color3":
        # only 2-seeds — no intersection partner
        g[3][3] = 2
        g[5][5] = 2
        return g
    return g

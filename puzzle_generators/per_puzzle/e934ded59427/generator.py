"""Generator for arc_puzzle_bank_21_set12_bundle:medium_l13 — Draw rect borders for color pairs.

Rule: for each color with 2 cells, draw rectangle border using those
cells as opposite corners.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: collinear_pair, single_color, no_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e934ded59427"
VERSION = "1.1.0"
TASK_ID = "e934ded59427"
SUMMARY = "2 colors each with 2 cells at diagonal corners."

INVARIANTS = [
    "exactly 2 colors with exactly 2 cells each at distinct rows/cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("collinear_pair", "single_color", "no_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "diagonal_corners",
                       "valid": "diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    r1 = rng.randint(0, 1); c1 = rng.randint(0, 2)
    r2 = rng.randint(r1 + 2, h - 2); c2 = rng.randint(c1 + 2, w // 2 - 1)
    g[r1][c1] = palette[0]; g[r2][c2] = palette[0]
    r3 = rng.randint(0, 1); c3 = rng.randint(w // 2 + 1, w - 3)
    r4 = rng.randint(r3 + 2, h - 1); c4 = rng.randint(c3 + 1, w - 1)
    g[r3][c3] = palette[1]; g[r4][c4] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "collinear_pair":
        # both cells share a row → "rectangle" degenerates to a line segment
        g[2][1] = 4; g[2][6] = 4
        g[5][2] = 7; g[5][8] = 7
        return g
    if name == "single_color":
        # only one color has a pair → only one rectangle, no second pair
        g[1][1] = 4; g[5][6] = 4
        return g
    if name == "no_pairs":
        # singletons only, no pair has 2 cells → nothing to enclose
        g[1][1] = 4
        g[5][6] = 7
        return g
    return g

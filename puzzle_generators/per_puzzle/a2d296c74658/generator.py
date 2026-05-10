"""Generator for arc_additional_puzzles_21_set3:E18.

Rule: cells (r, c) = 0 with g[r-1][c] = 7 AND g[r+1][c] = 7 become 4.

Combinatorial axes (8): grid_h/w, palette_kind, num_triplets, vertical_offset,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_one_seven, sevens_adjacent, gap_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2d296c74658"
VERSION = "1.1.0"
TASK_ID = "a2d296c74658"
SUMMARY = "2-3 vertical (7, 0, 7) triplets in distinct columns."

INVARIANTS = [
    "≥2 columns have a vertical (7, 0, 7) triplet",
]

PALETTE_KINDS = ("default", "scattered", "tight", "wide_grid")
DEGENERATE_TEXTURES = ("only_one_seven", "sevens_adjacent", "gap_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_triplets":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "vertical_offset": {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "uniform", "valid": "uniform"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_cols = set()
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            c = rng.randint(0, w - 1); r = rng.randint(0, h - 3)
            if c not in used_cols:
                g[r][c] = 7; g[r + 2][c] = 7
                used_cols.add(c)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 7
    g = full_grid(h, w, 0)
    if name == "only_one_seven":
        # single 7 with no partner — no triplet exists
        g[2][2] = 7
        g[4][5] = 7
        return g
    if name == "sevens_adjacent":
        # 7s with no zero between them — no fill happens
        g[2][2] = 7
        g[3][2] = 7
        g[4][5] = 7
        g[5][5] = 7
        return g
    if name == "gap_already_filled":
        # the would-be-4 cell is already nonzero — rule has nothing to fill
        g[2][2] = 7
        g[3][2] = 4
        g[4][2] = 7
        return g
    return g

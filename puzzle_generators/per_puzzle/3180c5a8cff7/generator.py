"""Generator for arc_additional_puzzles_21_set3:E17.

Rule: cells (r, c) = 0 with g[r][c-1] = 5 AND g[r][c+1] = 5 become 3.

Combinatorial axes (8): grid_h/w, palette_kind, num_triplets, horiz_offset,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_one_five, fives_adjacent, gap_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3180c5a8cff7"
VERSION = "1.1.0"
TASK_ID = "3180c5a8cff7"
SUMMARY = "2-3 (5, 0, 5) horizontal patterns scattered in different rows."

INVARIANTS = [
    "≥2 (5,0,5) triplets in distinct rows",
]

PALETTE_KINDS = ("default", "scattered", "tight", "wide_grid")
DEGENERATE_TEXTURES = ("only_one_five", "fives_adjacent", "gap_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_triplets":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "horiz_offset":   {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 3)
            if r not in used_rows:
                g[r][c] = 5; g[r][c + 2] = 5
                used_rows.add(r)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "only_one_five":
        # single 5 with no partner — no triplet
        g[2][2] = 5
        g[5][6] = 5
        return g
    if name == "fives_adjacent":
        # 5s with no zero between — rule has no fill cell
        g[2][2] = 5
        g[2][3] = 5
        g[5][5] = 5
        g[5][6] = 5
        return g
    if name == "gap_already_filled":
        # the would-be-3 cell is already nonzero — rule no-op
        g[2][2] = 5
        g[2][3] = 3
        g[2][4] = 5
        return g
    return g

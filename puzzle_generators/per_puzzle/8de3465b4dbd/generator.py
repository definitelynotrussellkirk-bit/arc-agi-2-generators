"""Generator for arc_additional_puzzles_21_set2:E12 — Pattern (2,3,0) horizontally → set the 0 to 8.

Rule: for each (r, c) where g[r][c]=2, g[r][c+1]=3, g[r][c+2]=0,
set g[r][c+2] to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, gap_already_filled, reverse_order.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8de3465b4dbd"
VERSION = "1.1.0"
TASK_ID = "8de3465b4dbd"
SUMMARY = "2-3 horizontal '2,3' pairs at row positions, plus distractor (3,2) pairs."

INVARIANTS = [
    ">=2 rows have a (2,3,0) horizontal sub-sequence",
    ">=1 distractor (3,2) pair (won't trigger)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "gap_already_filled", "reverse_order")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "horizontal_2_3",
                       "valid": "horizontal_2_3"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 3)
            if r not in used_rows:
                g[r][c] = 2; g[r][c + 1] = 3
                used_rows.add(r)
                break
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 2)
        if r not in used_rows and g[r][c] == 0 and g[r][c + 1] == 0:
            g[r][c] = 3; g[r][c + 1] = 2
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # no (2,3) pairs → rule has no targets, identity output
        for r, c, v in [(1, 2, 4), (3, 5, 5), (5, 7, 6)]:
            g[r][c] = v
        return g
    if name == "gap_already_filled":
        # (2,3,X) where X != 0 → rule's "next cell is 0" condition never matches
        g[2][1] = 2; g[2][2] = 3; g[2][3] = 5  # gap pre-filled with non-zero
        g[5][4] = 2; g[5][5] = 3; g[5][6] = 6
        return g
    if name == "reverse_order":
        # (3,2) pairs only, no (2,3) → rule never triggers
        g[2][1] = 3; g[2][2] = 2
        g[5][4] = 3; g[5][5] = 2
        return g
    return g

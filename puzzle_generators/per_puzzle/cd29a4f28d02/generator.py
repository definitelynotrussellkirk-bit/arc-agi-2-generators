"""Generator for arc_additional_puzzles_21_set13_bundle:E87 — Each 2-cell color → rect outline.

Rule: for each color with 2 cells, draw rect outline between them
on a fresh empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_cell_colors, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cd29a4f28d02"
VERSION = "1.1.0"
TASK_ID = "cd29a4f28d02"
SUMMARY = "1-2 colors with 2 cells each at distinct rows AND cols."

INVARIANTS = [
    "≥1 color with 2 cells at distinct rows AND cols",
    "bboxes don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_cell_colors", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_pairs",
                       "valid": "diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n = rng.randint(1, 2)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n)
    used = set()
    for color in pal:
        for _ in range(20):
            r1 = rng.randint(0, h - 3); r2 = rng.randint(r1 + 2, h - 1)
            c1 = rng.randint(0, w - 3); c2 = rng.randint(c1 + 2, w - 1)
            if (r1, c1) not in used and (r2, c2) not in used and g[r1][c1] == 0 and g[r2][c2] == 0:
                g[r1][c1] = color; g[r2][c2] = color
                used.add((r1, c1)); used.add((r2, c2))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no color appears twice
        return g
    if name == "single_cell_colors":
        # every color appears once → no pair to define a rect
        g[1][1] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "collinear_pair":
        # 2-cell pair on the same row OR same column → rect collapses to a line
        g[2][1] = 4; g[2][8] = 4   # same row
        g[1][5] = 6; g[5][5] = 6   # same column
        return g
    return g

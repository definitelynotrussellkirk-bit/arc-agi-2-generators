"""Generator for arc_puzzle_bank_21_set18_s:S18_E5.

Rule: color 2 closes across rows while color 3 closes down columns.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_color_2, no_color_3, no_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "26a885b7ba49"
VERSION = "1.1.0"
TASK_ID = "26a885b7ba49"
SUMMARY = "Color 2 closes across rows while color 3 closes down columns."

INVARIANTS = [
    "color 2 cells define horizontal spans",
    "color 3 cells define vertical spans",
    "vertical color-3 closure overwrites row closure where they overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_color_2", "no_color_3", "no_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "row_2_col_3",
                       "valid": "row_2_col_3"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    used: set[tuple[int, int]] = set()
    for r in rng.sample(range(h), 2):
        c1 = rng.randint(0, w - 5)
        c2 = rng.randint(c1 + 3, w - 1)
        g[r][c1] = 2
        g[r][c2] = 2
        used.update({(r, c1), (r, c2)})
    cols = rng.sample(range(w), 2)
    for c in cols:
        r1 = rng.randint(0, h - 5)
        r2 = rng.randint(r1 + 3, h - 1)
        for r in (r1, r2):
            if (r, c) in used:
                r = (r + 1) % h
            g[r][c] = 3
            used.add((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_color_2":
        # only column closures → no row spans
        g[1][3] = 3; g[5][3] = 3
        g[1][6] = 3; g[5][6] = 3
        return g
    if name == "no_color_3":
        # only row closures → no column spans, no overlap-overwrite case
        g[2][1] = 2; g[2][5] = 2
        g[5][2] = 2; g[5][7] = 2
        return g
    if name == "no_overlap":
        # spans in disjoint regions → overlap rule never triggers
        g[1][1] = 2; g[1][3] = 2
        g[5][5] = 3; g[7][5] = 3
        return g
    return g

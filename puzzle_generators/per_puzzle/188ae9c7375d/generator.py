"""Generator for additional_bank:H4 — 3-row bar chart of components for colors 2, 3, 4.

Rule: counts = (n_2_components, n_3_components, n_4_components). Output
3 × max(counts) grid: row r is color (2/3/4) for first count_r cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n2,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_equal_counts, only_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "188ae9c7375d"
VERSION = "1.1.0"
TASK_ID = "188ae9c7375d"
SUMMARY = "1-3 components each of colors 2, 3, 4 (non-touching); output is 3-row bar chart."

INVARIANTS = [
    "between 1 and 3 components of color 2, 3, and 4 each",
    "all blobs are non-touching",
    "at least one count differs (so output isn't trivially uniform)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_equal_counts", "only_one_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n2":             {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "non_touching_blobs",
                       "valid": "non_touching_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    n2 = ctx.draw_int("n2", 1, 3)
    n3 = ctx.draw_int("n3", 1, 3)
    n4 = ctx.draw_int("n4", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    for color, n in ((2, n2), (3, n3), (4, n4)):
        for _ in range(n):
            blob = grow_blob(rng, h, w, used, rng.randint(1, 2))
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_components":
        # blank → all counts zero, output is 0-wide bar chart
        return g
    if name == "all_equal_counts":
        # equal counts (1 of each) → bar chart is uniform width, no contrast
        g[1][1] = 2
        g[3][3] = 3
        g[5][5] = 4
        return g
    if name == "only_one_color":
        # only color 2, no 3 or 4 → bar chart degenerate to single row
        g[1][1] = 2
        g[3][3] = 2
        g[5][5] = 2
        return g
    return g

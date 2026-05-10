"""Generator for arc_additional_puzzles_21_set22_bundle:M153 — Bar chart of components per color.

Rule: for each non-bg color in the grid, count its connected components
of that color → bar chart row of color. Width = max count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_color, all_equal_counts, blobs_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "fee4c44dbec8"
VERSION = "1.1.0"
TASK_ID = "fee4c44dbec8"
SUMMARY = "Several non-touching blobs of 1-3 colors with varied counts; output is per-color count bar chart."

INVARIANTS = [
    "between 2 and 4 distinct non-bg colors used",
    "each color has between 1 and 3 components",
    "blobs are non-touching",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_color", "all_equal_counts", "blobs_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..4",  "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_blobs_per_color",
                       "valid": "scattered_blobs_per_color"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_colors = ctx.draw_int("n_colors", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_colors = ctx.draw_int("n_colors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_colors = ctx.draw_int("n_colors", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(1, 10)); rng.shuffle(palette)
    palette = palette[:n_colors]
    used = set()
    for color in palette:
        n = rng.randint(1, 3)
        for _ in range(n):
            size = rng.randint(1, 2)
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "single_color":
        # only one color → bar chart has only one bar; weakly tests rule
        for (r, c) in [(1, 1), (3, 4), (5, 7), (7, 2)]: g[r][c] = 4
        return g
    if name == "all_equal_counts":
        # every color has same count → output bar chart is trivially uniform
        g[1][1] = 4; g[3][2] = 4
        g[1][4] = 6; g[3][5] = 6
        g[1][7] = 3; g[3][8] = 3
        return g
    if name == "blobs_touching":
        # adjacent blobs of same color fuse into one component → count is wrong
        g[1][1] = 4; g[1][2] = 4
        g[3][1] = 4; g[3][2] = 4  # 4-cells but might fuse into bigger blob
        return g
    return g

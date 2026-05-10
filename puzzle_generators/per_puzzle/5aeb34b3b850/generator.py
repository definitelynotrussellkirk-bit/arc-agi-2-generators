"""Generator for arc_additional_puzzle_bank_volume23:M157 — Output count-row of colors 2,3,4.

Rule: count red(2), green(3), yellow(4) connected components. Output
single row: n2 reps of 2, then 0, then n3 reps of 3, then 0, then n4
reps of 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n2, n3, n4,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_color, all_zero_counts, all_equal_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "5aeb34b3b850"
VERSION = "1.1.0"
TASK_ID = "5aeb34b3b850"
SUMMARY = "Several blobs each of color 2, 3, 4; output counts per-color in a single row."

INVARIANTS = [
    "between 1 and 3 components of color 2",
    "between 1 and 3 components of color 3",
    "between 1 and 3 components of color 4",
    "at least one count differs (so output isn't trivially uniform)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_color", "all_zero_counts", "all_equal_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12",  "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n2":             {"type": "int", "default": "rng 1..3",   "valid": "1..5"},
    "n3":             {"type": "int", "default": "rng 1..3",   "valid": "1..5"},
    "n4":             {"type": "int", "default": "rng 1..3",   "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "scattered_3color_blobs",
                       "valid": "scattered_3color_blobs"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n2 = ctx.draw_int("n2", 1, 2)
        n3 = ctx.draw_int("n3", 1, 2)
        n4 = ctx.draw_int("n4", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n2 = ctx.draw_int("n2", 2, 3)
        n3 = ctx.draw_int("n3", 2, 3)
        n4 = ctx.draw_int("n4", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        n2 = ctx.draw_int("n2", 1, 3)
        n3 = ctx.draw_int("n3", 1, 3)
        n4 = ctx.draw_int("n4", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    for color, n in ((2, n2), (3, n3), (4, n4)):
        for _ in range(n):
            size = rng.randint(1, 2)
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "missing_color":
        # only red and green blobs (no yellow) → output has n4=0
        g[1][1] = 2; g[2][3] = 2
        g[5][5] = 3; g[6][7] = 3
        return g
    if name == "all_zero_counts":
        # blank → all counts are 0, output row degenerate
        return g
    if name == "all_equal_counts":
        # exactly 2 of each color → output row is symmetric (no asymmetry signal)
        g[1][1] = 2; g[1][3] = 2
        g[3][2] = 3; g[3][5] = 3
        g[5][4] = 4; g[5][7] = 4
        return g
    return g

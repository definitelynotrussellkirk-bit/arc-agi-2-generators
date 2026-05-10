"""Generator for arc_additional_puzzle_bank_volume21:E141.

Rule: each 2-blob that is a vertical line (single column, size ≥2)
gets its top and bottom cells set to 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, length_spread, texture.
Degenerates: horizontal_lines, single_cell_blobs, no_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6c894e4b9bf5"
VERSION = "1.1.0"
TASK_ID = "6c894e4b9bf5"
SUMMARY = "3-4 vertical 2-lines of varying lengths, plus decoration of color 7."

INVARIANTS = [
    "3-4 disjoint vertical 2-lines (single col, length ≥2)",
    "1-2 7-decorations that won't qualify",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("horizontal_lines", "single_cell_blobs", "no_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "3", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "vertical_columns",
                       "valid": "vertical_columns"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "length_spread":  {"type": "str", "default": "varied", "valid": "varied"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = rng.sample(range(1, w - 1), 3)
    for c in cols:
        length = rng.randint(2, 5)
        r0 = rng.randint(0, h - length)
        for dr in range(length):
            g[r0 + dr][c] = 2
    g[h - 3][1] = 7; g[h - 3][2] = 7; g[h - 3][3] = 7
    g[h - 2][1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "horizontal_lines":
        # 2-blobs are horizontal lines → none qualify under the vertical-line filter
        for c in range(2, 6):
            g[2][c] = 2
        for c in range(1, 5):
            g[5][c] = 2
        return g
    if name == "single_cell_blobs":
        # 2-blobs of size 1 → "top" and "bottom" coincide, endpoint marking degenerates
        for r, c in [(1, 2), (3, 5), (5, 8)]:
            g[r][c] = 2
        return g
    if name == "no_lines":
        # only decoration color present → no 2-blobs to mark
        for r, c in [(2, 2), (3, 3), (5, 5)]:
            g[r][c] = 7
        return g
    return g

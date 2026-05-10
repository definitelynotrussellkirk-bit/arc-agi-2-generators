"""Generator for arc_additional_puzzle_bank_volume9:E58 — complete blue 2x2 L-shapes with green.

Rule: blue 2×2 L-shapes are completed by filling the missing cell green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shapes, all_solid_squares, mixed_color_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3a379d1ed52c"
VERSION = "1.1.0"
TASK_ID = "3a379d1ed52c"
SUMMARY = "Blue 2x2 L-shapes are completed by filling the missing cell green."

INVARIANTS = [
    "background is 0",
    "each target 2x2 window contains exactly three blue cells",
    "target windows are separated from one another",
    "missing cells are blank before the rule runs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shapes", "all_solid_squares", "mixed_color_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_blue_L_trominoes",
                       "valid": "spaced_blue_L_trominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_shapes = ctx.draw_int("n_shapes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_shapes = ctx.draw_int("n_shapes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_shapes = ctx.draw_int("n_shapes", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(0, h - 1, 3) for c in range(0, w - 1, 3)]
    rng.shuffle(anchors)
    corners = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for r, c in anchors[:n_shapes]:
        missing = rng.choice(corners)
        for dr, dc in corners:
            if (dr, dc) != missing:
                g[r + dr][c + dc] = 1
    if not any(1 in row for row in g):
        g[0][0] = 1
        g[0][1] = 1
        g[1][0] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        # blank → no L-shapes to complete
        return g
    if name == "all_solid_squares":
        # 2x2 fully filled with blue → no missing cell to fill
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(2): g[4 + r][4 + c] = 1
        return g
    if name == "mixed_color_corners":
        # 2x2 with 3 cells but mixed colors → "all blue" precondition fails
        g[1][1] = 1; g[1][2] = 4; g[2][1] = 1   # mixed
        g[4][4] = 6; g[4][5] = 1; g[5][4] = 1   # mixed
        return g
    return g

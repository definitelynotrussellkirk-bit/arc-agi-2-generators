"""Generator for arc_puzzle_bank_twentythird21:E155.

Rule: each row's column-0 cell may hold a color; the output paints
the entire row with that color (or leaves bg if column 0 is 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_column0, body_already_painted, all_rows_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "252c3df06496"
VERSION = "1.1.0"
TASK_ID = "252c3df06496"
SUMMARY = "Column 0 has 2-4 colored cells (one per chosen row); rest of grid is empty."

INVARIANTS = [
    "background is 0",
    "column 0 has 2-4 cells in distinct colors at distinct rows",
    "all other cells are 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_column0", "body_already_painted", "all_rows_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "column0", "valid": "column0"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 5, 6)
        n = ctx.draw_int("n_rows", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_rows", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_rows", 2, min(4, h))
    n = min(n, h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for r, color in zip(rows, colors):
        g[r][0] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "empty_column0":
        # column 0 is all zero → no rows to paint, rule is no-op
        for r, c in [(1, 3), (3, 4), (4, 2)]:
            g[r][c] = 5
        return g
    if name == "body_already_painted":
        # some body cells already nonzero → conflict with row-paint operation
        g[1][0] = 3; g[3][0] = 7
        g[1][2] = 4; g[3][5] = 9
        return g
    if name == "all_rows_same_color":
        # every column-0 cell shares one color → output is uniformly that color
        for r in range(h):
            g[r][0] = 4
        return g
    return g

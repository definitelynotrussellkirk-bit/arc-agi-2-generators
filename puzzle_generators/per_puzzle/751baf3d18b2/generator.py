"""Generator for arc_puzzle_bank_tenth21:E70.

Rule: row 0 is a column-header palette; every nonzero body cell is
recolored to its column's header.

Combinatorial axes (8): grid_h/w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, body_density, texture.
Degenerates: no_header_row, empty_body, header_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "751baf3d18b2"
VERSION = "1.1.0"
TASK_ID = "751baf3d18b2"
SUMMARY = "Body cells recolor to the nonzero header color in their column."

INVARIANTS = [
    "background is 0",
    "row 0 is a column header palette",
    "body nonzero cells may use arbitrary colors",
    "each body nonzero recolors to its column header",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_header_row", "empty_body", "header_zero")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "int", "default": "rng 30..55", "valid": "1..100"},
    "palette_size":   {"type": "int", "default": "rng 5..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..9", "valid": "1..9"},
    "body_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 7, 11)
    density = ctx.draw_int("density", 30, 55)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for r in range(1, h):
        for c in range(w):
            if rng.randrange(100) < density:
                g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "no_header_row":
        # body has cells but row 0 is all zero — no header to copy from
        g[2][3] = 4
        g[3][1] = 6
        return g
    if name == "empty_body":
        # full header row but no body cells — rule has nothing to recolor
        for c in range(w):
            g[0][c] = ((c % 7) + 2)
        return g
    if name == "header_zero":
        # body cells under zero header positions — would recolor to bg
        g[0][2] = 4
        g[0][5] = 7
        # body cell at column 0 where header is 0
        g[2][0] = 9
        g[3][3] = 5
        return g
    return g

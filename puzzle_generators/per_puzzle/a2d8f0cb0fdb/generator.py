"""Generator for arc_puzzle_bank_twentieth21:E134 — recolor 1s by row-0 color.

Rule: row 0 has a single colored cell (the 'palette'). Other rows have a
sparse 1-pattern; output recolors the 1s with the palette color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_ones,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, multiple_palette_cells, no_ones.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2d8f0cb0fdb"
VERSION = "1.1.0"
TASK_ID = "a2d8f0cb0fdb"
SUMMARY = "Row 0 has 1 colored marker (non-{0, 1}). Body has scattered color-1 cells."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly one cell in a non-{0, 1} color",
    "rows >=1 have 3-8 sparse color-1 cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "multiple_palette_cells", "no_ones")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 4..8", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "row0_palette",
                       "valid": "row0_palette"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 5, 6)
        n_ones = ctx.draw_int("n_ones", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n_ones = ctx.draw_int("n_ones", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 5, 8)
        n_ones = ctx.draw_int("n_ones", 4, 8)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    g[0][rng.randint(0, w - 1)] = color
    for _ in range(n_ones):
        for _t in range(40):
            r = rng.randint(1, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # row 0 has no palette cell → no recolor target, rule no-op
        for r, c in [(1, 2), (2, 4), (3, 1), (4, 5)]:
            g[r][c] = 1
        return g
    if name == "multiple_palette_cells":
        # multiple palette cells in row 0 → ambiguous which color to use
        g[0][1] = 3
        g[0][3] = 5
        g[0][5] = 7
        for r, c in [(1, 2), (2, 4), (3, 0), (4, 6)]:
            g[r][c] = 1
        return g
    if name == "no_ones":
        # palette present but no 1-cells in body → nothing to recolor
        g[0][3] = 5
        return g
    return g

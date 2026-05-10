"""Generator for arc_puzzle_bank_twentieth21:E138 — paint plus shape per non-zero cell.

Rule: each non-zero cell paints a plus shape (itself + 4 cardinal neighbors)
in its color (clipped to grid).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, cells_at_corner, overlapping_pluses.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56c98fd9e674"
VERSION = "1.1.0"
TASK_ID = "56c98fd9e674"
SUMMARY = "1-3 isolated colored cells (each surrounded by bg)."

INVARIANTS = [
    "background is 0",
    "1-3 single-cell markers in distinct non-zero colors at non-adjacent positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "cells_at_corner", "overlapping_pluses")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "interior_separated_singletons",
                       "valid": "interior_separated_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
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
        n = ctx.draw_int("n_cells", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_cells", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_cells", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = []
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in colors:
        for _t in range(120):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if any(abs(r - pr) + abs(c - pc) < 4 for pr, pc in placed): continue
            g[r][c] = color
            placed.append((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # blank → no markers, plus rule has nothing to paint
        return g
    if name == "cells_at_corner":
        # markers at corner → 2 plus arms clip out of bounds (only L visible)
        g[0][0] = 4
        g[h - 1][w - 1] = 6
        return g
    if name == "overlapping_pluses":
        # markers adjacent → plus stamps overlap, last-wins is ambiguous
        g[2][2] = 4
        g[2][3] = 6   # plus arms collide on (2,2)/(2,3)
        return g
    return g

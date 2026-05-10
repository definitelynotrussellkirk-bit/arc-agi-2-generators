"""Generator for arc_additional_puzzle_bank_volume3:E18 — shift red singletons right.

Rule: isolated red singletons shift one cell to the right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_singletons,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, cells_at_right_edge, multi_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e58953aee67a"
VERSION = "1.1.0"
TASK_ID = "e58953aee67a"
SUMMARY = "Isolated red singletons shift one cell to the right."

INVARIANTS = [
    "background is 0",
    "target red cells are cardinally isolated singletons",
    "each target has an empty in-bounds right destination",
    "targets are separated so shifted cells do not collide",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "cells_at_right_edge", "multi_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_singletons":   {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_red_singletons",
                       "valid": "spaced_red_singletons"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_singletons = ctx.draw_int("n_singletons", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_singletons = ctx.draw_int("n_singletons", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_singletons = ctx.draw_int("n_singletons", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: list[tuple[int, int]] = []
    for _ in range(240):
        if len(cells) >= n_singletons:
            break
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) <= 1 and abs(c - cc) <= 2 for rr, cc in cells):
            continue
        g[r][c] = 2
        cells.append((r, c))
    if not cells:
        g[1][1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # blank → no red cells to shift
        return g
    if name == "cells_at_right_edge":
        # cells at right edge → shift goes out of bounds
        g[2][w - 1] = 2
        g[5][w - 1] = 2
        return g
    if name == "multi_cell_blobs":
        # multi-cell blobs (not singletons) → "isolated singleton" precondition fails
        g[2][2] = 2; g[2][3] = 2   # adjacent (pair)
        g[5][5] = 2; g[6][5] = 2   # adjacent (pair)
        return g
    return g

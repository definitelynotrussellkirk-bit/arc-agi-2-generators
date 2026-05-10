"""Generator for arc_puzzle_bank_fourth21:E25.

Rule: each isolated nonzero cell shifts right by one (its right neighbor must be empty).

Combinatorial axes (8): grid_h, grid_w, palette_kind, cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, cell_at_right_edge, cells_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85305305afdf"
VERSION = "1.1.0"
TASK_ID = "85305305afdf"

SUMMARY = "Scatter isolated movable cells with empty space to their right."

INVARIANTS = [
    "background is 0",
    "each nonzero cell has an empty right neighbor",
    "cells are separated so simultaneous right shifts do not collide",
    "all nonzero cells are inside the grid except the rightmost column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "cell_at_right_edge", "cells_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_with_right_room",
                       "valid": "spaced_with_right_room"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("cells", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("cells", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("cells", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randrange(h)
        c = rng.randint(0, w - 2)
        footprint = {(r, c), (r, c + 1)}
        guard = {
            (rr, cc)
            for rr in range(max(0, r - 1), min(h, r + 2))
            for cc in range(max(0, c - 1), min(w, c + 3))
        }
        if guard & reserved:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        reserved.update(footprint | guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # blank → no cells to shift, rule has no effect
        return g
    if name == "cell_at_right_edge":
        # cells in last column → no right neighbor exists, rule undefined
        g[1][w - 1] = 4
        g[3][w - 1] = 6
        return g
    if name == "cells_blocked":
        # adjacent cells where each blocks the other's right shift
        g[1][2] = 4; g[1][3] = 6  # 4's right is occupied by 6
        g[3][5] = 3; g[3][6] = 8  # 3's right is occupied by 8
        return g
    return g

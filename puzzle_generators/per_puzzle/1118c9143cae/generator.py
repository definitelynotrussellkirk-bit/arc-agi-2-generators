"""Generator for arc_puzzle_bank_21_set24_bundle:easy_p06.

Rule: sparse cells echoed by 180-degree rotation.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: cell_at_center, cells_already_symmetric, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1118c9143cae"
VERSION = "1.1.0"
TASK_ID = "1118c9143cae"
SUMMARY = "Sparse cells are echoed by a 180-degree rotation."

INVARIANTS = [
    "background is 0",
    "no input cell occupies another input cell's half-turn reflection",
    "the output keeps originals and adds reflected cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("cell_at_center", "cells_already_symmetric", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "off_center",
                       "valid": "off_center"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _reflect(h: int, w: int, r: int, c: int) -> tuple[int, int]:
    return h - 1 - r, w - 1 - c


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        cell_count = ctx.draw_int("cell_count", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        cell_count = ctx.draw_int("cell_count", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        cell_count = ctx.draw_int("cell_count", 3, 6)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h) for c in range(w)
                 if (r, c) != _reflect(h, w, r, c)]
    rng.shuffle(positions)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(cell_count, 9))
    used: set[tuple[int, int]] = set()
    placed = 0

    for r, c in positions:
        mirror = _reflect(h, w, r, c)
        if (r, c) in used or mirror in used:
            continue
        grid[r][c] = colors[placed % len(colors)]
        used.add((r, c))
        used.add(mirror)
        placed += 1
        if placed >= cell_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 9  # odd dims so center cell is fixed under 180
    g = full_grid(h, w, 0)
    if name == "cell_at_center":
        # cell at the half-turn fixed point → its mirror is itself, echo is no-op for it
        g[h // 2][w // 2] = 7
        for r, c, v in [(2, 3, 4), (5, 6, 5)]:
            g[r][c] = v
        return g
    if name == "cells_already_symmetric":
        # input is already 180-symmetric → output equals input, rule is identity
        pairs = [((1, 2), (7, 6)), ((2, 5), (6, 3)), ((3, 1), (5, 7))]
        for (r1, c1), (r2, c2) in pairs:
            g[r1][c1] = 4
            g[r2][c2] = 4
        return g
    if name == "empty_grid":
        # no cells → echo no-op
        return g
    return g

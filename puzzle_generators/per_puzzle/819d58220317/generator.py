"""Generator for arc_additional_puzzle_bank_volume7:H46.

Rule: the count of red markers selects which empty band between
nested yellow frames is filled cyan.

Combinatorial axes (8): grid_size, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, rank_too_high, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "819d58220317"
VERSION = "1.1.0"
TASK_ID = "819d58220317"
SUMMARY = "The count of red markers selects which empty band between nested yellow frames is filled cyan."

INVARIANTS = [
    "nested yellow hollow frames are present",
    "red marker count is a valid band index",
    "the selected band contains blank cells",
    "frame borders remain yellow",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "rank_too_high", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 14..16", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "nested_frames",
                       "valid": "nested_frames"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "framed", "valid": "framed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame(g: list[list[int]], r0: int, c0: int, r1: int, c1: int) -> None:
    for r in range(r0, r1 + 1):
        g[r][c0] = 4
        g[r][c1] = 4
    for c in range(c0, c1 + 1):
        g[r0][c] = 4
        g[r1][c] = 4


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 14, 14)
        rank = ctx.draw_int("rank", 1, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 15, 16)
        rank = ctx.draw_int("rank", 2, 3)
    else:
        n = ctx.draw_int("grid_size", 14, 16)
        rank = ctx.draw_int("rank", 1, 3)
    g = full_grid(n, n, 0)
    _frame(g, 1, 1, n - 2, n - 2)
    _frame(g, 4, 4, n - 5, n - 5)
    if n >= 14:
        _frame(g, 6, 6, n - 7, n - 7)
    for i in range(rank):
        g[n - 1][i] = 2
    return g


def _draw_from_degenerate(name, rng):
    n = 14
    g = full_grid(n, n, 0)
    if name == "no_red":
        # no red markers → rank = 0, no band selected
        _frame(g, 1, 1, n - 2, n - 2)
        _frame(g, 4, 4, n - 5, n - 5)
        _frame(g, 6, 6, n - 7, n - 7)
        return g
    if name == "rank_too_high":
        # red marker count exceeds the number of bands → no valid band to fill
        _frame(g, 1, 1, n - 2, n - 2)
        _frame(g, 4, 4, n - 5, n - 5)
        for i in range(8):
            g[n - 1][i] = 2
        return g
    if name == "no_frames":
        # red markers but no frames → no bands to count
        for i in range(2):
            g[n - 1][i] = 2
        return g
    return g

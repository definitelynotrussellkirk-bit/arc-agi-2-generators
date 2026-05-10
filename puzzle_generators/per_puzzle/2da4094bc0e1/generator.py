"""Generator for arc_additional_puzzle_bank_volume10:E66.

Rule: exact horizontal yellow length-3 lines receive magenta caps at
their immediate left and right neighbors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_bars,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: wrong_length_bars, bars_at_edge, no_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2da4094bc0e1"
VERSION = "1.1.0"
TASK_ID = "2da4094bc0e1"
SUMMARY = "Exact horizontal yellow length-3 lines receive magenta caps."

INVARIANTS = [
    "background is 0",
    "target yellow bars are maximal horizontal runs of exactly length 3",
    "cap cells are empty when inside the grid",
    "bars occupy distinct rows so they do not merge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("wrong_length_bars", "bars_at_edge", "no_bars")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bars":         {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "row_local", "valid": "row_local"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        n_bars = ctx.draw_int("n_bars", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 14)
        n_bars = ctx.draw_int("n_bars", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
        n_bars = ctx.draw_int("n_bars", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), min(n_bars, h))
    for i, r in enumerate(rows):
        c = rng.randint(0, w - 3)
        if i == 0 and w >= 5:
            c = 1
        for dc in range(3):
            g[r][c + dc] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "wrong_length_bars":
        # bars of length 2 and 4 → no length-3 bar matches the rule's filter
        for dc in range(2):
            g[1][2 + dc] = 4
        for dc in range(4):
            g[4][2 + dc] = 4
        return g
    if name == "bars_at_edge":
        # bars touch grid edges → at least one cap position is out-of-bounds
        for dc in range(3):
            g[1][0 + dc] = 4
        for dc in range(3):
            g[4][w - 3 + dc] = 4
        return g
    if name == "no_bars":
        # empty grid → rule has no targets
        return g
    return g

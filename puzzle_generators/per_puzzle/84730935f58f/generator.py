"""Generator for arc_puzzle_bank_21_set17_s:S17_E6.

Rule: cell (0, 0) is the stencil selector — 1 = plus growth, anything
else = X (diagonal) growth. All other nonzero cells are seeds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, mode, num_seeds,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_selector, no_seeds, ambiguous_selector.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "84730935f58f"
VERSION = "1.1.0"
TASK_ID = "84730935f58f"
SUMMARY = "A legend cell chooses plus or diagonal-X seed growth."

INVARIANTS = [
    "cell (0,0) is the stencil selector",
    "selector 1 means plus growth; any other selector means X growth",
    "remaining nonzero cells are seeds",
]

PALETTE_KINDS = ("default", "many_seeds", "spread_seeds", "tight_seeds")
DEGENERATE_TEXTURES = ("no_selector", "no_seeds", "ambiguous_selector")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "width":          {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "mode":           {"type": "choice", "default": "rng plus|x",
                       "valid": "plus|x"},
    "num_seeds":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5",
                          "valid": "1..7"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 6, 7)
        w = ctx.draw_int("width", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 7, 8)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 6, 8)
    mode = ctx.draw_choice("mode", ["plus", "x"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = 1 if mode == "plus" else 2
    cells = [(r, c) for r in range(h) for c in range(w) if (r, c) != (0, 0)]
    for idx, (r, c) in enumerate(rng.sample(cells, rng.randint(2, 4))):
        g[r][c] = 4 + idx
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_selector":
        # seeds but no selector at (0,0) — growth pattern undefined
        g[2][3] = 5
        g[4][2] = 6
        return g
    if name == "no_seeds":
        # selector but nothing to grow
        g[0][0] = 1
        return g
    if name == "ambiguous_selector":
        # selector 1 AND a non-1 nonzero at (1,0) — no clear single legend
        g[0][0] = 1
        g[0][1] = 2
        g[3][3] = 5
        return g
    return g

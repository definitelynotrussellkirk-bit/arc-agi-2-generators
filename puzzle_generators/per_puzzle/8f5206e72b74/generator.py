"""Generator for arc_puzzle_bank_thirteenth21:E85.

Rule: same-color horizontal endpoints with zeros between are bridged.

Combinatorial axes (8): grid_h/w, palette_kind, n_pairs, palette_size,
position_bias, n_distinct_colors, gap_density, texture.
Degenerates: no_gap, single_endpoint, no_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8f5206e72b74"
VERSION = "1.1.0"
TASK_ID = "8f5206e72b74"
SUMMARY = "Same-color horizontal endpoints with zeros between are bridged."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "matching endpoints share one row",
    "the cells between matching endpoints are blank",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_gap", "single_endpoint", "no_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "gap_density":    {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 13)
    target = min(ctx.draw_int("pairs", 2, 4), h, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    for r, color in zip(rows, colors):
        c0 = rng.randint(0, w - 3)
        c1 = rng.randint(c0 + 2, w - 1)
        g[r][c0] = color
        g[r][c1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_gap":
        # touching endpoints — interval has zero interior
        g[2][3] = 4
        g[2][4] = 4
        return g
    if name == "single_endpoint":
        # single cell, no second endpoint
        g[3][5] = 6
        return g
    if name == "no_seeds":
        # empty grid — nothing to bridge
        return g
    return g

"""Generator for arc_puzzle_bank_21_set12_s:S12_M1 — crop max-degree component.

Rule: a contact graph contains one unique highest-degree component,
which is cropped and recolored.

Combinatorial axes (8): grid_h, grid_w, palette_kind, leaf_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_chain, tied_max_degree, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b81390858ebd"
VERSION = "1.1.0"
TASK_ID = "b81390858ebd"
SUMMARY = "A contact graph contains one unique highest-degree component, which is cropped and recolored."

INVARIANTS = [
    "background is 0",
    "nonzero components are same-color 4-connected objects",
    "one central component has strictly higher contact degree than every other component",
    "distractor components have lower contact degree and do not touch the target cluster",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_chain", "tied_max_degree", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "leaf_count":     {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "position_bias":  {"type": "str", "default": "central_hub_with_leaves",
                       "valid": "central_hub_with_leaves"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "4..7"},
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
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 11, 13)
        leaf_count = ctx.draw_int("leaf_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 14, 15)
        leaf_count = ctx.draw_int("leaf_count", 4, 4)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 11, 15)
        leaf_count = ctx.draw_int("leaf_count", 3, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r = rng.randint(3, h - 4)
    c = rng.randint(3, w - 4)
    g[r][c] = 3
    leaves = [
        (r - 1, c, 1),
        (r, c + 1, 2),
        (r + 1, c, 4),
        (r, c - 1, 6),
    ]
    for lr, lc, color in leaves[:leaf_count]:
        g[lr][lc] = color

    g[1][w - 3] = 7
    g[1][w - 2] = 7
    g[h - 2][1] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_chain":
        # all components isolated → all degree 0, no max to find
        g[2][2] = 3
        g[6][6] = 7
        g[8][9] = 8
        return g
    if name == "tied_max_degree":
        # 2 components share max degree → "unique highest-degree" precondition fails
        g[3][3] = 3; g[3][4] = 1; g[3][2] = 2   # hub A: degree 2
        g[7][8] = 4; g[7][9] = 6; g[7][7] = 5   # hub B: degree 2 (tied)
        return g
    if name == "all_isolated":
        # only one isolated component → trivial degree-0 case
        g[5][5] = 3
        return g
    return g

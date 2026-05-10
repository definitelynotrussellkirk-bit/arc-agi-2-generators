"""Generator for arc_puzzle_bank_21_set12_s:S12_M6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, winner_orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_winner, tied_variety, single_cluster.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8f0cbb9e10ac"
VERSION = "1.1.0"
TASK_ID = "8f0cbb9e10ac"

SUMMARY = "The cluster with the greatest color variety is cropped and recolored."

INVARIANTS = [
    "background is 0",
    "one contact cluster contains four distinct component colors",
    "a larger distractor cluster has fewer distinct colors",
    "the winning cluster is unique by distinct-color count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_winner", "tied_variety", "single_cluster")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "winner_orientation": {"type": "str", "default": "rng horizontal|vertical",
                           "valid": "horizontal|vertical"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "winner_plus_distractor",
                       "valid": "winner_plus_distractor"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
    orientation = ctx.draw_choice("winner_orientation", ["horizontal", "vertical"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4]
    if orientation == "horizontal":
        r = rng.randint(2, h - 5)
        c = rng.randint(2, w - 7)
        for i, color in enumerate(colors):
            g[r][c + i] = color
    else:
        r = rng.randint(2, h - 6)
        c = rng.randint(2, w - 5)
        for i, color in enumerate(colors):
            g[r + i][c] = color
    base_r = h - 2
    for i, color in enumerate([6, 7, 6, 7, 6]):
        g[base_r][1 + i] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_winner":
        # only the 2-color distractor → no max-variety cluster to select
        for i, color in enumerate([6, 7, 6, 7, 6]):
            g[h - 2][1 + i] = color
        return g
    if name == "tied_variety":
        # two clusters tie at 4 distinct colors → ambiguous winner
        for i, color in enumerate([1, 2, 3, 4]):
            g[2][2 + i] = color
        for i, color in enumerate([5, 6, 7, 9]):
            g[h - 2][2 + i] = color
        return g
    if name == "single_cluster":
        # only one cluster, no contrast → "uniqueness by distinct count" trivial
        for i, color in enumerate([1, 2, 3, 4]):
            g[3][3 + i] = color
        return g
    return g

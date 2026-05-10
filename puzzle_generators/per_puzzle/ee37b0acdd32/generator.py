"""Generator for arc_puzzle_bank_21_set12_s:S12_M4 — connect blue and red via contact chain.

Rule: blue and red endpoint components are connected by a unique
shortest contact path.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blue, no_red, no_chain.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ee37b0acdd32"
VERSION = "1.1.0"
TASK_ID = "ee37b0acdd32"

SUMMARY = "Blue and red endpoint components are connected by a unique shortest contact path."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue endpoint component and one red endpoint component",
    "the endpoint components lie in one simple contact chain",
    "distractor components are disconnected from the endpoint path",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blue", "no_red", "no_chain")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "9..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng horizontal|vertical",
                       "valid": "horizontal|vertical"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "blue_red_chain_with_distractor",
                       "valid": "blue_red_chain_with_distractor"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    orientation = ctx.draw_choice("orientation", ["horizontal", "vertical"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    colors = [1, 3, 4, 6, 2]
    if orientation == "horizontal":
        r = rng.randint(2, h - 4)
        c = rng.randint(2, w - 7)
        for i, color in enumerate(colors):
            g[r][c + i] = color
    else:
        r = rng.randint(2, h - 7)
        c = rng.randint(2, w - 4)
        for i, color in enumerate(colors):
            g[r + i][c] = color

    g[h - 2][w - 3] = 7
    g[h - 2][w - 2] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_blue":
        # red endpoint + chain but no blue endpoint → no path source
        for i, color in enumerate([3, 4, 6, 2]):
            g[3][3 + i] = color
        g[h - 2][w - 3] = 7
        return g
    if name == "no_red":
        # blue endpoint + chain but no red endpoint → no path target
        for i, color in enumerate([1, 3, 4, 6]):
            g[3][3 + i] = color
        g[h - 2][w - 3] = 7
        return g
    if name == "no_chain":
        # blue and red exist but components are not in any contact chain
        g[2][2] = 1
        g[7][9] = 2   # far apart, no chain
        g[h - 2][w - 3] = 7
        return g
    return g

"""Generator for arc_puzzle_bank_21_set12_s:S12_E6 — recolor by contact degree.

Rule: components are recolored by contact degree: 0→3, 1→4, 2→6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, chain_orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_chain, all_isolated, ring_chain.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e245314f96d8"
VERSION = "1.1.0"
TASK_ID = "e245314f96d8"
SUMMARY = "Components are recolored by contact degree: 0 to 3, 1 to 4, and 2 to 6."

INVARIANTS = [
    "background is 0",
    "a three-component chain provides degree-1 and degree-2 examples",
    "an isolated component provides a degree-0 example",
    "outputs are blank except for degree-coded components",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_chain", "all_isolated", "ring_chain")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "width":          {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "chain_orientation": {"type": "choice", "default": "rng horizontal|vertical",
                          "valid": "horizontal|vertical"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "linear_chain_with_distractor",
                       "valid": "linear_chain_with_distractor"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..4"},
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
        h = ctx.draw_int("height", 8, 9)
        w = ctx.draw_int("width", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
    else:
        h = ctx.draw_int("height", 8, 11)
        w = ctx.draw_int("width", 10, 13)
    orientation = ctx.draw_choice("chain_orientation", ["horizontal", "vertical"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 4)
    c = rng.randint(2, w - 7)
    if orientation == "horizontal":
        g[r][c] = 2
        g[r][c + 1] = 5
        g[r][c + 2] = 7
    else:
        g[r][c] = 2
        g[r + 1][c] = 5
        g[r + 2][c] = 7
    g[h - 2][w - 3] = 9
    g[h - 2][w - 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_chain":
        # all components isolated → no degree-1 or degree-2 examples (only degree-0)
        g[1][1] = 2
        g[1][6] = 5
        g[5][3] = 7
        g[6][9] = 9
        return g
    if name == "all_isolated":
        # only one isolated component → only degree-0 case present
        g[4][5] = 6; g[4][6] = 6
        return g
    if name == "ring_chain":
        # closed cycle → all nodes have degree 2 (no degree-0 or degree-1)
        g[2][2] = 2; g[2][3] = 5
        g[3][3] = 7; g[3][2] = 9
        return g
    return g

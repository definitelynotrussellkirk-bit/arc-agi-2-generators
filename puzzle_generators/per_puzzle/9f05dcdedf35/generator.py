"""Generator for arc_puzzle_bank_21_set12_s:S12_E3 — recolor leaf-degree components to 8.

Rule: leaf components in a contact graph are recolored to 8 in place
(degree-1 chain endpoints are recolored; degree-0 distractors and
interior chain nodes keep their colors).

Combinatorial axes (8): grid_h, grid_w, palette_kind, chain_orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_chain, all_isolated, ring_chain.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9f05dcdedf35"
VERSION = "1.1.0"
TASK_ID = "9f05dcdedf35"
SUMMARY = "Leaf components in a contact graph are recolored to 8 in place."

INVARIANTS = [
    "background is 0",
    "three differently colored components form a simple contact chain",
    "the chain endpoints have degree one",
    "an isolated distractor has degree zero and is not recolored",
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
        g[r][c + 1] = 3
        g[r][c + 2] = 4
    else:
        g[r][c] = 2
        g[r + 1][c] = 3
        g[r + 2][c] = 4
    g[h - 2][w - 3] = 6
    g[h - 2][w - 2] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_chain":
        # all components isolated (degree 0) → no leaves to recolor
        g[1][1] = 2
        g[1][6] = 3
        g[5][3] = 4
        g[6][9] = 6
        return g
    if name == "all_isolated":
        # only one isolated distractor → no chain at all
        g[4][5] = 6; g[4][6] = 6
        return g
    if name == "ring_chain":
        # closed cycle → no degree-1 leaves (all nodes have degree 2)
        g[2][2] = 2; g[2][3] = 3
        g[3][3] = 4; g[3][2] = 5
        # touching forms a 2x2 ring in contact graph
        return g
    return g

"""Generator for arc_additional_puzzle_bank_volume8:M56.

Rule: k = count of 1-cells. Template = largest 3-blob shape. Rotate by
(k-1) cw turns (k=4: flip-h instead). Stamp at 7-anchor in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchor, no_k_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d7788d30a256"
VERSION = "1.1.0"
TASK_ID = "d7788d30a256"
SUMMARY = "k 1-cells in row 0 + 3-template + 7-anchor."

INVARIANTS = [
    "row 0 has between 1 and 4 cells of color 1 (rotation count)",
    "exactly one 3-blob template",
    "exactly one 7-anchor where rotated stamp fits",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchor", "no_k_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k":              {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_template_anchor",
                       "valid": "fixed_template_anchor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        k = ctx.draw_int("k", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        k = ctx.draw_int("k", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        k = ctx.draw_int("k", 1, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:k]:
        g[0][c] = 1
    g[2][1] = 3
    g[3][1] = 3; g[3][2] = 3
    g[4][2] = 3
    g[6][7] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        # no 3-blob → nothing to rotate and stamp
        g[0][0] = 1; g[0][1] = 1
        g[6][7] = 7
        return g
    if name == "no_anchor":
        # no 7-anchor → rotated stamp has nowhere to land
        g[0][0] = 1; g[0][1] = 1
        g[2][1] = 3; g[3][1] = 3; g[3][2] = 3; g[4][2] = 3
        return g
    if name == "no_k_marker":
        # no 1-cells → rotation count k = 0, rule has no rotation input
        g[2][1] = 3; g[3][1] = 3; g[3][2] = 3; g[4][2] = 3
        g[6][7] = 7
        return g
    return g

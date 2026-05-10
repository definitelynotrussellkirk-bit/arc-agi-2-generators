"""Generator for arc_additional_puzzle_bank_volume13:M90 — recolor odd-vsym blue.

Rule: the blue component with the unique vertical-symmetry status is
recolored red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_symmetric, all_asymmetric, two_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "93ca517eac25"
VERSION = "1.1.0"
TASK_ID = "93ca517eac25"
SUMMARY = "The blue component with the unique vertical-symmetry status is recolored red."

INVARIANTS = [
    "background is 0",
    "there are three separated blue components",
    "two components are vertically symmetric after normalization",
    "one component is not vertically symmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_symmetric", "all_asymmetric", "two_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "two_sym_one_asym_blue",
                       "valid": "two_sym_one_asym_blue"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top = rng.randint(0, h - 8)
    left = rng.randint(0, w - 10)
    symmetric_a = [(top, left + 1), (top + 1, left), (top + 1, left + 1), (top + 1, left + 2)]
    symmetric_b = [(top + 4, left + 1), (top + 5, left), (top + 5, left + 1), (top + 5, left + 2)]
    odd = [(top + 2, left + 6), (top + 2, left + 7), (top + 3, left + 6), (top + 4, left + 6)]
    for cells in [symmetric_a, symmetric_b, odd]:
        for r, c in cells:
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    sym = [(0, 1), (1, 0), (1, 1), (1, 2)]   # T shape (vsym)
    asym = [(0, 0), (0, 1), (1, 0), (2, 0)]   # L shape (asym)
    if name == "all_symmetric":
        # all 3 components symmetric → no "odd one out" to recolor
        for dr, dc in sym: g[1 + dr][1 + dc] = 1
        for dr, dc in sym: g[1 + dr][7 + dc] = 1
        for dr, dc in sym: g[7 + dr][4 + dc] = 1
        return g
    if name == "all_asymmetric":
        # all 3 components asymmetric → no "odd one out" (all share same status)
        for dr, dc in asym: g[1 + dr][1 + dc] = 1
        for dr, dc in asym: g[1 + dr][7 + dc] = 1
        for dr, dc in asym: g[6 + dr][4 + dc] = 1
        return g
    if name == "two_components":
        # only 2 components → "odd one" is whichever is unique, but invariant says 3
        for dr, dc in sym: g[1 + dr][1 + dc] = 1
        for dr, dc in asym: g[1 + dr][7 + dc] = 1
        return g
    return g

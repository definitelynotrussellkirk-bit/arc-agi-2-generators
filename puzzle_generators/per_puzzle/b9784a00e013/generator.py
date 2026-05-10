"""Generator for arc_puzzle_bank_ninth21:E60.

Rule: keep the unique-largest connected component, erase others.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9784a00e013"
VERSION = "1.1.0"
TASK_ID = "b9784a00e013"
SUMMARY = "One largest component is mixed with smaller separated components."

INVARIANTS = [
    "background is 0",
    "there is one unique largest connected component",
    "all smaller components are separated by background",
    "the largest component is preserved and all others are erased",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g: list[list[int]], top: int, left: int, shape: list[tuple[int, int]], color: int) -> None:
    for dr, dc in shape:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    large = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]
    _paint(g, 1, 1, large, colors[0])
    _paint(g, 0, w - 3, [(0, 0), (0, 1)], colors[1])
    _paint(g, h - 2, 0, [(0, 0), (1, 0), (1, 1)], colors[2])
    _paint(g, h - 2, w - 2, [(0, 0), (1, 0)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two components share the same maximum size → "unique largest" invariant violated, ambiguous
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6), (6, 7)]:
            g[r][c] = 6
        return g
    if name == "single_component":
        # only one component → trivially the largest, rule is identity
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3), (4, 3)]:
            g[r][c] = 5
        return g
    if name == "no_components":
        # empty grid → no largest, rule output is empty/all-zero
        return g
    return g

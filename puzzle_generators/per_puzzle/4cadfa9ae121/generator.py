"""Generator for arc_puzzle_bank_21_set12_s:S12_E2 — keep only isolated components.

Rule: only components with contact degree zero are kept in a blank
output grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, isolated_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, no_isolated, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4cadfa9ae121"
VERSION = "1.1.0"
TASK_ID = "4cadfa9ae121"
SUMMARY = "Only components with contact degree zero are kept in a blank output grid."

INVARIANTS = [
    "background is 0",
    "there is at least one edge-touching component pair",
    "there is at least one isolated component",
    "isolated components preserve their original colors and positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "no_isolated", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "isolated_count": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "cluster_with_isolated",
                       "valid": "cluster_with_isolated"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        isolated_count = ctx.draw_int("isolated_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        isolated_count = ctx.draw_int("isolated_count", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        isolated_count = ctx.draw_int("isolated_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 4)
    c = rng.randint(2, w - 7)
    _paint(g, [(r, c), (r + 1, c)], 2)
    _paint(g, [(r, c + 1), (r, c + 2)], 3)
    _paint(g, [(r + 2, c), (r + 3, c)], 4)
    isolated = [
        (6, [(1, w - 3), (1, w - 2)]),
        (7, [(h - 2, w - 3)]),
    ]
    for color, cells in isolated[:isolated_count]:
        _paint(g, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        # blank → nothing to filter (output is also blank)
        return g
    if name == "no_isolated":
        # only edge-touching cluster → all components dropped, output empty
        _paint(g, [(3, 3), (4, 3)], 2)
        _paint(g, [(3, 4), (3, 5)], 3)
        _paint(g, [(5, 3), (6, 3)], 4)
        return g
    if name == "all_isolated":
        # every component is isolated → rule is identity (no filtering signal)
        _paint(g, [(2, 2), (2, 3)], 6)
        _paint(g, [(7, 8), (7, 9)], 7)
        return g
    return g

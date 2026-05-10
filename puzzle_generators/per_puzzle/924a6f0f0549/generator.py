"""Generator for arc_puzzle_bank_fifth21:H33.

The number of color-1 markers in the first row selects the body component of
that area. The rule outlines that component and crops to the outline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_size_match, multiple_size_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "924a6f0f0549"
VERSION = "1.1.0"
TASK_ID = "924a6f0f0549"
SUMMARY = "Top-row count selects a body object by size for outline-and-crop."

INVARIANTS = [
    "row 0 has three to six color-1 markers",
    "body components have distinct cell counts",
    "exactly one component area matches the marker count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_size_match", "multiple_size_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_size":    {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_count_plus_blobs",
                       "valid": "marker_count_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = {
    3: [(0, 0), (1, 0), (1, 1)],
    4: [(0, 0), (1, 0), (1, 1), (2, 1)],
    5: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    6: [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
    7: [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (3, 0), (3, 1)],
}


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        k = ctx.draw_int("target_size", 4, 4)
    elif difficulty == "hard":
        k = ctx.draw_int("target_size", 5, 6)
    else:
        k = ctx.draw_int("target_size", 4, 6)
    g = full_grid(11, 15, 0)
    for c in rng.sample(range(1, 12), k):
        g[0][c] = 1
    _paint(g, 2, 1, _SHAPES[k], rng.choice([2, 3, 4, 5, 6, 7, 8, 9]))
    _paint(g, 2, 9, _SHAPES[3 if k != 3 else 7], rng.choice([2, 3, 4, 5, 6, 7, 8, 9]))
    _paint(g, 7, 6, _SHAPES[7 if k != 7 else 5], rng.choice([2, 3, 4, 5, 6, 7, 8, 9]))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 15, 0)
    if name == "no_markers":
        # blobs without row-0 marker count → no selection signal
        _paint(g, 2, 1, _SHAPES[4], 4)
        _paint(g, 2, 9, _SHAPES[3], 6)
        _paint(g, 7, 6, _SHAPES[7], 7)
        return g
    if name == "no_size_match":
        # k=5 markers but no body component has size 5
        for c in [1, 3, 5, 7, 9]: g[0][c] = 1
        _paint(g, 2, 1, _SHAPES[3], 4)
        _paint(g, 2, 9, _SHAPES[4], 6)
        _paint(g, 7, 6, _SHAPES[7], 7)
        return g
    if name == "multiple_size_match":
        # 2 components share size k → ambiguous winner
        for c in [1, 2, 3, 4]: g[0][c] = 1  # k=4
        _paint(g, 2, 1, _SHAPES[4], 4)
        _paint(g, 2, 9, _SHAPES[4], 6)
        _paint(g, 7, 6, _SHAPES[7], 7)
        return g
    return g

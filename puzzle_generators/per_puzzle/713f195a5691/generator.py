"""Generator for arc_puzzle_bank_21_set3:S3_H6.

The number of color-1 cells in the left panel selects the green object of that
size in the right panel; the rule draws a cyan bounding box around it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_size_match, multiple_size_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "713f195a5691"
VERSION = "1.1.0"
TASK_ID = "713f195a5691"
SUMMARY = "Left-panel marker count selects the matching-size green object on the right."

INVARIANTS = [
    "one empty separator column divides the grid",
    "left-panel color-1 marker count is between 4 and 6",
    "right panel has exactly one color-3 object with that size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_size_match", "multiple_size_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_count":   {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "left_count_plus_right_blobs",
                       "valid": "left_count_plus_right_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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


def _paint(g, top, left, cells):
    for r, c in cells:
        g[top + r][left + c] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        k = ctx.draw_int("marker_count", 4, 4)
    elif difficulty == "hard":
        k = ctx.draw_int("marker_count", 5, 6)
    else:
        k = ctx.draw_int("marker_count", 4, 6)
    g = full_grid(13, 13, 0)
    sep = 5
    marker_rows = list(range(1, 10))
    rng.shuffle(marker_rows)
    for r in marker_rows[:k]:
        g[r][1 + (r % 3)] = 1
    _paint(g, 2, 6, _SHAPES[k])
    distractor_size = 3 if k != 3 else 7
    _paint(g, 8, 9, _SHAPES[distractor_size])
    assert all(g[r][sep] == 0 for r in range(len(g)))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_markers":
        # right-panel blobs without left-panel markers → no count to select with
        _paint(g, 2, 6, _SHAPES[4])
        _paint(g, 8, 9, _SHAPES[3])
        return g
    if name == "no_size_match":
        # k=5 markers but no right-panel object has size 5
        for r in [1, 3, 5, 7, 9]: g[r][1] = 1  # k=5
        _paint(g, 2, 6, _SHAPES[3])
        _paint(g, 8, 9, _SHAPES[7])
        return g
    if name == "multiple_size_match":
        # 2 right-panel objects share size k → ambiguous winner
        for r in [1, 3, 5, 7]: g[r][1] = 1  # k=4
        _paint(g, 2, 6, _SHAPES[4])
        _paint(g, 8, 9, _SHAPES[4])  # also size 4
        return g
    return g

"""Generator for arc_puzzle_bank_21_set9_s:S9_H4.

Use area and width legends to select one object and recolor it to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legends, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1620d15035b5"
VERSION = "1.1.0"
TASK_ID = "1620d15035b5"
SUMMARY = "Use area and width legends to select one object and recolor it to 8."

INVARIANTS = [
    "top-row color-1 count gives the target object area",
    "left-column color-3 count gives the target object's bbox width",
    "exactly one object away from row 0/col 0 matches both features",
    "the output is a same-size grid containing only the selected object in color 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legends", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "legends_plus_target_distractor",
                       "valid": "legends_plus_target_distractor"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGETS = [
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
]
_DISTRACTORS = [
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        idx = ctx.draw_int("variant", 1, 2)
    else:
        idx = ctx.draw_int("variant", 0, 2)
    target = _TARGETS[idx]
    area = len(target)
    width = max(c for _, c in target) - min(c for _, c in target) + 1
    colors = rng.sample([2, 4, 5, 6, 7, 9], 2)
    g = full_grid(10, 12, 0)
    for c in range(area):
        g[0][c + 1] = 1
    for r in range(width):
        g[r + 1][0] = 3
    _paint(g, 3, 3, target, colors[0])
    _paint(g, 7, 6, _DISTRACTORS[idx], colors[1])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_legends":
        # objects without row-0/col-0 legends → no selection signal
        _paint(g, 3, 3, _TARGETS[0], 4)
        _paint(g, 7, 6, _DISTRACTORS[0], 6)
        return g
    if name == "no_match":
        # legends specify (area, width) but no object matches both
        for c in range(5): g[0][c + 1] = 1  # area = 5
        for r in range(3): g[r + 1][0] = 3  # width = 3
        _paint(g, 3, 3, _DISTRACTORS[0], 4)  # area 3 width 2
        _paint(g, 7, 6, _DISTRACTORS[1], 6)  # area 4 width 4
        return g
    if name == "multiple_matches":
        # 2 objects match both features → ambiguous winner
        for c in range(4): g[0][c + 1] = 1  # area = 4
        for r in range(2): g[r + 1][0] = 3  # width = 2
        _paint(g, 3, 3, [(0, 0), (1, 0), (1, 1), (2, 1)], 4)  # area 4 width 2
        _paint(g, 7, 8, [(0, 0), (1, 0), (1, 1), (2, 1)], 6)  # also matches
        return g
    return g

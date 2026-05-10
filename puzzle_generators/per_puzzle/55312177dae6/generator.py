"""Generator for arc_puzzle_bank_21_set5_s:S5_H4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, family,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_match, all_unique, no_distractor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "55312177dae6"
VERSION = "1.1.0"
TASK_ID = "55312177dae6"
SUMMARY = "Find the color-1 shape family repeated under rotation and emit its canonical mask."

INVARIANTS = [
    "all components are color 1",
    "two components share the same rotational canonical form",
    "one distractor component has a different canonical form",
    "the output is the repeated canonical shape painted with color 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_match", "all_same", "no_distractor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "family":         {"type": "int", "default": "rng 0..7", "valid": "0..7"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "rotation_pair_plus_distractor",
                       "valid": "rotation_pair_plus_distractor"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_FAMILIES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
]
_DISTRACTORS = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0)],
]


def _rot90(cells):
    raw = [(c, -r) for r, c in cells]
    mr = min(r for r, _ in raw)
    mc = min(c for _, c in raw)
    return [(r - mr, c - mc) for r, c in raw]


def _paint(g, top, left, cells):
    for r, c in cells:
        g[top + r][left + c] = 1


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        family = ctx.draw_int("family", 0, 3)
    elif difficulty == "hard":
        family = ctx.draw_int("family", 4, 7)
    else:
        family = ctx.draw_int("family", 0, 7)
    cells = _FAMILIES[family]
    g = full_grid(8, 10, 0)
    _paint(g, 1, 1, cells)
    _paint(g, 1, 6, _rot90(cells))
    _paint(g, 5, 5, _DISTRACTORS[family])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_match":
        # 3 different shapes (no rotation pair) → no shape to extract
        _paint(g, 1, 1, _FAMILIES[0])
        _paint(g, 1, 6, _FAMILIES[1])
        _paint(g, 5, 5, _DISTRACTORS[0])
        return g
    if name == "all_same":
        # all 3 shapes are the same family → no distractor, ambiguous selection
        _paint(g, 1, 1, _FAMILIES[0])
        _paint(g, 1, 6, _FAMILIES[0])
        _paint(g, 5, 5, _FAMILIES[0])
        return g
    if name == "no_distractor":
        # only the rotation pair, no distractor → still works but degenerate
        _paint(g, 1, 1, _FAMILIES[0])
        _paint(g, 1, 6, _rot90(_FAMILIES[0]))
        return g
    return g

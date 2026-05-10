"""Generator for arc_puzzle_bank_21_set10_e:hard_j21.

Pack one representative object from each horizontal/vertical symmetry
class.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_classes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_class, duplicate_class, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0aead82893c5"
VERSION = "1.1.0"
TASK_ID = "0aead82893c5"
SUMMARY = "Pack one representative object from each horizontal/vertical symmetry class."

INVARIANTS = [
    "there are exactly four separated same-color components",
    "the components cover the both-axis, vertical-only, horizontal-only, and neither symmetry classes",
    "all component crops are 3x3 so the packed gallery shape is stable",
    "the output preserves component colors in a 2x2 gallery with one blank row and column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_class", "duplicate_class", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_classes":      {"type": "int", "default": "4", "valid": "4..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "four_symmetry_class_gallery",
                       "valid": "four_symmetry_class_gallery"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BOTH = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
_VERTICAL = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
_HORIZONTAL = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)]
_NEITHER = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g = full_grid(12, 16, 0)
    for (top, left), cells, color in [
        ((1, 1), _BOTH, colors[0]),
        ((1, 9), _VERTICAL, colors[1]),
        ((7, 1), _HORIZONTAL, colors[2]),
        ((7, 9), _NEITHER, colors[3]),
    ]:
        _paint(g, top, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "missing_class":
        # only 3 of 4 symmetry classes → rule's "one rep per class" precondition fails
        _paint(g, 1, 1, _BOTH, 3)
        _paint(g, 1, 9, _VERTICAL, 4)
        _paint(g, 7, 1, _HORIZONTAL, 5)
        return g
    if name == "duplicate_class":
        # two reps of the same class → ambiguous which to keep
        _paint(g, 1, 1, _BOTH, 3)
        _paint(g, 1, 9, _BOTH, 4)
        _paint(g, 7, 1, _HORIZONTAL, 5)
        _paint(g, 7, 9, _NEITHER, 6)
        return g
    if name == "all_same_color":
        # all 4 reps share one color → can't distinguish gallery cells
        _paint(g, 1, 1, _BOTH, 3)
        _paint(g, 1, 9, _VERTICAL, 3)
        _paint(g, 7, 1, _HORIZONTAL, 3)
        _paint(g, 7, 9, _NEITHER, 3)
        return g
    return g

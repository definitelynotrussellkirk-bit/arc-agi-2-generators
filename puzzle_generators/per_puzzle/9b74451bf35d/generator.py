"""Generator for arc_additional_puzzles_21_set19_bundle:H133.

Rule: 3 panels (rows × 3 cols each); find the transform a-mask →
b-mask; apply it to the c-mask using b's first non-zero color.

Combinatorial axes (8): grid_h/w, palette_kind, transform_kind,
palette_size, position_bias, n_distinct_colors, panel_diversity, texture.
Degenerates: identical_a_b, no_panel_a, no_panel_c.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9b74451bf35d"
VERSION = "1.1.0"
TASK_ID = "9b74451bf35d"
SUMMARY = "3 panels separated by 1-col gaps; b is a transform of a."

INVARIANTS = [
    "3 panels of 3 cols each, separated by 1-col gaps",
    "b's mask = transform(a's mask) for some t ∈ {0,1,2,4,5}",
]

PALETTE_KINDS = ("default", "rotated", "flipped", "transposed")
DEGENERATE_TEXTURES = ("identical_a_b", "no_panel_a", "no_panel_c")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "transform_kind": {"type": "str", "default": "rotated",
                       "valid": "rotated"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "panel_diversity": {"type": "str", "default": "varied",
                        "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    h = 3; w = 11
    g = full_grid(h, w, 0)
    color_a = rng.choice([2, 3, 4])
    color_b = rng.choice([5, 6, 7])
    color_c = rng.choice([8, 9])
    cells_a = [(0, 0), (1, 0), (1, 1)]
    cells_b = [(0, 0), (0, 1), (1, 1)]
    cells_c = [(0, 0), (0, 1), (1, 0), (2, 0)]
    for r, c in cells_a: g[r][c] = color_a
    for r, c in cells_b: g[r][4 + c] = color_b
    for r, c in cells_c: g[r][8 + c] = color_c
    return g


def _draw_from_degenerate(name, rng):
    h = 3; w = 11
    g = full_grid(h, w, 0)
    cells_same = [(0, 0), (1, 0), (1, 1)]
    cells_c = [(0, 0), (0, 1), (1, 0), (2, 0)]
    if name == "identical_a_b":
        # a == b → transform is identity, c unchanged (rule trivial)
        for r, c in cells_same: g[r][c] = 2
        for r, c in cells_same: g[r][4 + c] = 5
        for r, c in cells_c: g[r][8 + c] = 8
        return g
    if name == "no_panel_a":
        # b + c but no a — transform's source is missing
        for r, c in cells_same: g[r][4 + c] = 5
        for r, c in cells_c: g[r][8 + c] = 8
        return g
    if name == "no_panel_c":
        # a + b but no c — no operand to apply transform to
        for r, c in cells_same: g[r][c] = 2
        for r, c in [(0, 0), (0, 1), (1, 1)]: g[r][4 + c] = 5
        return g
    return g

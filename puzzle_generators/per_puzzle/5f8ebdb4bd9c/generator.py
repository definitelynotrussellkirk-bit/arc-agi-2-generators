"""Generator for arc_additional_puzzles_21_set19_bundle:M133 — Find transform a→b, apply to c.

Rule: 3 panels (3 cols + separator + 3 cols + separator + 3 cols). Find
which transform takes a→b; apply to c. Codes: 0=identity, 1=cw, 2=180,
4=flip-lr, 5=flip-ud.

Combinatorial axes (8): grid_h, grid_w, palette_kind, transform,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, identical_AB, no_C.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5f8ebdb4bd9c"
VERSION = "1.1.0"
TASK_ID = "5f8ebdb4bd9c"
SUMMARY = "3 panels of 3x3 each separated by 1-col gaps; b is a transform of a; c is unrelated."

INVARIANTS = [
    "grid is exactly 3 rows × 11 cols",
    "panels at cols 0..2, 4..6, 8..10",
    "panel b = transform(a) for some t ∈ {0,1,2,4,5}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identical_AB", "no_C")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3..3"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "transform":      {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "abc_3panels_with_gaps",
                       "valid": "abc_3panels_with_gaps"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _apply(cells, t):
    if t == 0:
        return list(cells)
    if t == 1:
        return [(c, 2 - r) for r, c in cells]
    if t == 2:
        return [(2 - r, 2 - c) for r, c in cells]
    if t == 3:
        return [(r, 2 - c) for r, c in cells]  # flip-lr
    return [(2 - r, c) for r, c in cells]  # flip-ud


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        t_idx = ctx.draw_int("transform", 0, 1)
    elif difficulty == "hard":
        t_idx = ctx.draw_int("transform", 0, 4)
    else:
        t_idx = ctx.draw_int("transform", 0, 4)
    h, w = 3, 11
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color_a = rng.choice([2, 3, 4, 5, 6])
    color_c = rng.choice([7, 8, 9])
    # Panel a: 3 asymmetric cells
    cells_a = [(0, 0), (1, 0), (1, 1), (2, 0)]
    paint_at(g, 0, 0, cells_a, color_a)
    cells_b = _apply(cells_a, t_idx)
    paint_at(g, 0, 4, cells_b, color_a)
    # Panel c: different shape
    cells_c = [(0, 1), (1, 0), (1, 2), (2, 1)]
    paint_at(g, 0, 8, cells_c, color_c)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 3, 11
    g = full_grid(h, w, 0)
    cells_a = [(0, 0), (1, 0), (1, 1), (2, 0)]
    cells_c = [(0, 1), (1, 0), (1, 2), (2, 1)]
    if name == "no_dividers":
        # panels touch (no 1-col gaps) → can't tell where panel boundaries are
        paint_at(g, 0, 0, cells_a, 4)
        paint_at(g, 0, 3, _apply(cells_a, 1), 4)
        paint_at(g, 0, 6, cells_c, 7)
        return g
    if name == "identical_AB":
        # A == B → identity transform, no signal
        paint_at(g, 0, 0, cells_a, 4)
        paint_at(g, 0, 4, cells_a, 4)  # identity
        paint_at(g, 0, 8, cells_c, 7)
        return g
    if name == "no_C":
        # A→B demo but no C → no target to apply transform to
        paint_at(g, 0, 0, cells_a, 4)
        paint_at(g, 0, 4, _apply(cells_a, 1), 4)
        return g
    return g

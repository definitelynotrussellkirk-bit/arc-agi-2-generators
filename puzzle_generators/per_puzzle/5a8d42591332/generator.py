"""Generator for arc_puzzle_bank_21_set4:S4_H4.

Top and left 2x2 headers encode counts. The rule fills the 3x3 matrix of 2x2
cells by comparing each top count with each left count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, min_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top, no_left, all_zero_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a8d42591332"
VERSION = "1.1.0"
TASK_ID = "5a8d42591332"
SUMMARY = "Fixed 3x3 comparison matrix with top and left 2x2 count headers."

INVARIANTS = [
    "top headers live at rows 0..1 and columns 3,6,9",
    "left headers live at columns 0..1 and rows 3,6,9",
    "the 3x3 body blocks start at rows and columns 3,6,9",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top", "no_left", "all_zero_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "min_count":      {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "comparison_matrix_headers",
                       "valid": "comparison_matrix_headers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CELLS_2X2 = [(0, 0), (0, 1), (1, 0), (1, 1)]


def _fill_count(g, r0, c0, count, color, rng):
    cells = list(_CELLS_2X2)
    rng.shuffle(cells)
    for dr, dc in cells[:count]:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        min_count = ctx.draw_int("min_count", 2, 2)
    elif difficulty == "hard":
        min_count = ctx.draw_int("min_count", 1, 1)
    else:
        min_count = ctx.draw_int("min_count", 1, 2)
    starts = [3, 6, 9]
    top_counts = [rng.randint(min_count, 4) for _ in range(3)]
    left_counts = [rng.randint(min_count, 4) for _ in range(3)]
    if top_counts == left_counts:
        left_counts = left_counts[1:] + left_counts[:1]
    g = full_grid(12, 12, 0)
    for c0, count in zip(starts, top_counts):
        _fill_count(g, 0, c0, count, 1, rng)
    for r0, count in zip(starts, left_counts):
        _fill_count(g, r0, 0, count, 2, rng)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_top":
        # only left headers → no top counts to compare → matrix has no signal
        for r0, count in zip([3, 6, 9], [2, 3, 4]):
            cells = _CELLS_2X2[:count]
            for dr, dc in cells:
                g[r0 + dr][0 + dc] = 2
        return g
    if name == "no_left":
        # only top headers → no left counts to compare
        for c0, count in zip([3, 6, 9], [2, 3, 4]):
            cells = _CELLS_2X2[:count]
            for dr, dc in cells:
                g[0 + dr][c0 + dc] = 1
        return g
    if name == "all_zero_counts":
        # both header strips empty → comparison rule has no inputs
        return g
    return g

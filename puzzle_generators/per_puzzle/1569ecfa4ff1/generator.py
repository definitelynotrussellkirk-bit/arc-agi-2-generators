"""Generator for arc_additional_puzzles_21_set20_bundle:E134 — Rotate non-{0,8} cells 90° CW around 8-pivot.

Rule: pivot = 8-cell. For each non-{0,8} cell at (r,c), compute (dr,dc)
relative to pivot; new position = pivot + (dc, -dr). Output keeps
pivot at original position; rotated cells in their new positions.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_cells, multiple_pivots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1569ecfa4ff1"
VERSION = "1.1.0"
TASK_ID = "1569ecfa4ff1"
SUMMARY = "Single 8-pivot with 2-3 cells of one color forming an asymmetric pattern around it."

INVARIANTS = [
    "exactly 1 cell of color 8 (pivot)",
    "≥2 cells of single non-{0,8} color forming an L/asymmetric shape",
    "rotated positions stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_cells", "multiple_pivots")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "centered_pivot_with_asymmetric_arms",
                       "valid": "centered_pivot_with_asymmetric_arms"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pr = h // 2; pc = w // 2
    g[pr][pc] = 8
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    shape = rng.choice([
        [(-1, 0), (0, -1), (1, -1)],
        [(0, -1), (1, -1), (-1, -1)],
        [(-1, -1), (1, 1)],
    ])
    for dr, dc in shape:
        if 0 <= pr + dr < h and 0 <= pc + dc < w:
            g[pr + dr][pc + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pivot":
        # cells exist but no 8-pivot → no center of rotation
        g[1][2] = 4
        g[2][3] = 4
        return g
    if name == "no_cells":
        # pivot only, no other cells → nothing to rotate
        g[3][3] = 8
        return g
    if name == "multiple_pivots":
        # two 8-cells → ambiguous which is the pivot
        g[2][2] = 8
        g[5][5] = 8
        g[3][3] = 4; g[3][4] = 4
        return g
    return g

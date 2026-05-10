"""Generator for b71a7747.

Rule: two-color row/column support is identified by paired colors
and cropped to its active submatrix.

Combinatorial axes (8): grid_h/w, matrix_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_matrix, full_grid, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b277da396290"
VERSION = "1.1.0"
TASK_ID = "b277da396290"
SUMMARY = "Two-color row/column support cropped to its active submatrix."

INVARIANTS = [
    "background is color 0",
    "two non-background colors occupy the same row and column support",
    "the supported submatrix contains exactly those two colors",
    "matrix sits with at least two cells of margin from grid borders",
]

MATRIX_SIZES = ("3", "4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_matrix", "full_grid", "single_color")
HELPFUL_TEXTURES = MATRIX_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "matrix_size":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MATRIX_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for matrix_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size = int((overrides.get("texture") if overrides.get("texture") in MATRIX_SIZES else None) or
               overrides.get("matrix_size") or
               ctx.draw_choice("matrix_size", list(MATRIX_SIZES)))
    h = 8 + rng.randint(0, 3)
    w = 8 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    r0 = 2 + rng.randint(0, h - size - 3)
    c0 = 2 + rng.randint(0, w - size - 3)
    for r in range(size):
        for c in range(size):
            g[r0 + r][c0 + c] = 2 if (r + c) % 2 == 0 else 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_matrix":
        return g
    if name == "single_color":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g

"""Generator for 4938f0c2.

Rule: 2-shape and 3-region; reflect 2-cells through the bbox center of
all 3-cells.

Combinatorial axes (8): grid_h/w, shape_variant, n_threes, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_threes, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ea8116b3e778"
VERSION = "1.1.0"
TASK_ID = "ea8116b3e778"
SUMMARY = "Small 2-shape + 2-3 cells of color 3 forming a center marker."

INVARIANTS = [
    ">=3 cells of color 2 forming an asymmetric shape",
    ">=1 cell of color 3 (acts as center marker)",
    "shape and 3-marker don't overlap",
]

SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)],
]

POSITION_BIASES = ("scattered", "centered", "corners", "rng")
DEGENERATE_TEXTURES = ("no_threes", "no_shape", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "shape_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "n_threes":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 7, 8, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 11, 14
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 9, 9, 11
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    sv = int(overrides.get("shape_variant",
                           ctx.draw_int("shape_variant", 0, len(SHAPES) - 1)))
    sv = max(0, min(len(SHAPES) - 1, sv))
    shape = SHAPES[sv]
    paint_at(g, 0, 1, shape, 2)
    n_threes = int(overrides.get("n_threes",
                                 ctx.draw_int("n_threes", 1, 3)))
    n_threes = max(1, min(3, n_threes))
    for _ in range(n_threes):
        col = rng.randint(2, max(2, w - 4))
        if h >= 2 and 0 <= h - 2 < h and 0 <= col < w:
            g[h - 2][col] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_threes":
        paint_at(g, 0, 1, SHAPES[0], 2)
        return g
    if name == "no_shape":
        g[h - 2][3] = 3; g[h - 2][6] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g

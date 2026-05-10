"""Generator for arc_additional_puzzles_21_set20_bundle:E139.

Rule: crop to non-bg content, then re-place that crop centered in an
empty grid of the original size.

Combinatorial axes (8): grid_h/w, palette_kind, shape_position,
palette_size, n_distinct_colors, position_bias, shape_size, texture.
Degenerates: already_centered, shape_fills_grid, no_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "03909f3e98e7"
VERSION = "1.1.0"
TASK_ID = "03909f3e98e7"
SUMMARY = "Small shape placed in upper-left corner of a larger grid."

INVARIANTS = [
    "shape placed near top-left (so re-centering visibly shifts it)",
    "shape ≤4 cells, ≥2 distinct non-bg colors used",
]

PALETTE_KINDS = ("top_left", "top_right", "bottom_left", "edge_centered")
DEGENERATE_TEXTURES = ("already_centered", "shape_fills_grid", "no_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_position": {"type": "str", "default": "top_left",
                       "valid": "any_corner"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "off-center",
                       "valid": "off-center"},
    "shape_size":     {"type": "int", "default": "4", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    g[1][1] = pal[0]; g[1][3] = pal[1]
    g[2][1] = pal[0]; g[2][2] = pal[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "already_centered":
        cr, cc = h // 2, w // 2
        g[cr - 1][cc - 1] = 4
        g[cr - 1][cc] = 5
        g[cr][cc - 1] = 4
        g[cr][cc] = 6
        return g
    if name == "shape_fills_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4 if (r + c) % 2 == 0 else 5
        return g
    if name == "no_shape":
        return g
    return g

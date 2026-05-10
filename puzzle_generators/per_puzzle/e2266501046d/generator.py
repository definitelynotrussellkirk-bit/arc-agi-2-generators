"""Generator for arc_additional_puzzles_21_set22_bundle:E152.

Rule: collect non-bg cells (single color); fill bbox rect of those
cells with that color on a fresh empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_size,
palette_size, position_bias, n_distinct_colors, rect_aspect, texture.
Degenerates: no_cells, single_cell, two_outlines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "e2266501046d"
VERSION = "1.1.0"
TASK_ID = "e2266501046d"
SUMMARY = "A hollow rect outline of one color (input has hollow interior; output fills it)."

INVARIANTS = [
    "1 hollow rect outline of a single non-bg color, ≥3×3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "single_cell", "two_outlines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_size":      {"type": "str", "default": "fit_grid", "valid": "fit_grid"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "rect_aspect":    {"type": "str", "default": "rng", "valid": "rng"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    rh = rng.randint(4, h - 2); rw = rng.randint(4, w - 2)
    r0 = rng.randint(1, h - rh - 1); c0 = rng.randint(1, w - rw - 1)
    draw_rect_outline(g, r0, c0, rh, rw, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid — bbox of empty set is undefined
        return g
    if name == "single_cell":
        # one cell → bbox is 1×1, fill is identity (no visible rule)
        g[3][4] = 5
        return g
    if name == "two_outlines":
        # two separate outlines of the same color → bbox spans both
        draw_rect_outline(g, 1, 1, 3, 3, 4)
        draw_rect_outline(g, 5, 5, 3, 4, 4)
        return g
    return g

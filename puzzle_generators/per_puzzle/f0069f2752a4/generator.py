"""Generator for arc_puzzle_bank_21_set9_s:S9_E4.

Border-touching components are kept while fully interior components are removed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, border_side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_obj, no_interior_obj, all_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f0069f2752a4"
VERSION = "1.1.0"
TASK_ID = "f0069f2752a4"
SUMMARY = "Border-touching components are kept while fully interior components are removed."

INVARIANTS = [
    "background is 0",
    "at least one component touches the grid border",
    "at least one component is strictly interior",
    "kept components preserve their colors and positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_obj", "no_interior_obj", "all_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "border_side":    {"type": "str", "default": "rng top|left|bottom|right",
                       "valid": "top|left|bottom|right"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "border_obj_plus_interior_obj",
                       "valid": "border_obj_plus_interior_obj"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    side = ctx.draw_choice("border_side", ["top", "left", "bottom", "right"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if side == "top":
        _paint(g, [(0, 1), (0, 2), (1, 2)], 2)
    elif side == "left":
        _paint(g, [(1, 0), (2, 0), (2, 1)], 2)
    elif side == "bottom":
        _paint(g, [(h - 1, 1), (h - 1, 2), (h - 2, 2)], 2)
    else:
        _paint(g, [(1, w - 1), (2, w - 1), (2, w - 2)], 2)
    r = rng.randint(3, h - 3)
    c = rng.randint(3, w - 3)
    _paint(g, [(r, c), (r, c + 1), (r + 1, c)], 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_border_obj":
        # only interior component → rule erases everything
        _paint(g, [(4, 4), (4, 5), (5, 4)], 4)
        return g
    if name == "no_interior_obj":
        # only border-touching component → rule keeps everything (no contrast)
        _paint(g, [(0, 1), (0, 2), (1, 2)], 2)
        return g
    if name == "all_interior":
        # multiple components, all strictly interior → rule erases all of them
        _paint(g, [(3, 3), (3, 4), (4, 3)], 4)
        _paint(g, [(5, 5), (5, 6), (6, 5)], 6)
        return g
    return g

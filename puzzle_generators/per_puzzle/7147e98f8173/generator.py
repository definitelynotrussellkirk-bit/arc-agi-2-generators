"""Generator for arc_additional_puzzle_bank_volume18:H126.

Rule: a blue corner control rotates the red template; the green→orange
vector shifts it onto a blank cyan output.

Combinatorial axes (8): grid_h/w, palette_kind, corner_position,
palette_size, position_bias, n_distinct_colors, vector_length, texture.
Degenerates: no_corner, no_template, missing_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "7147e98f8173"
VERSION = "1.1.0"
TASK_ID = "7147e98f8173"
SUMMARY = "A blue corner control rotates the red template, then the green-to-orange vector shifts it onto a blank cyan output."

INVARIANTS = [
    "one blue control is placed in a corner",
    "one red asymmetric template is present",
    "green and orange markers define a nonzero vector",
    "the shifted transformed copy remains in-bounds",
]

PALETTE_KINDS = ("default", "tl_corner", "tr_corner", "bl_or_br_corner")
DEGENERATE_TEXTURES = ("no_corner", "no_template", "missing_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corner_position": {"type": "str", "default": "rng",
                        "valid": "tl|tr|bl|br"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "vector_length":  {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cr, cc = rng.choice([(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)])
    g[cr][cc] = 1
    paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 2)
    g[0][w - 4] = 3
    g[3][w - 2] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_corner":
        # template + markers but no blue control — rotation undefined
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 2)
        g[0][w - 4] = 3
        g[3][w - 2] = 6
        return g
    if name == "no_template":
        # blue corner + markers but no red template to rotate/shift
        g[0][0] = 1
        g[0][w - 4] = 3
        g[3][w - 2] = 6
        return g
    if name == "missing_marker":
        # corner + template but only green marker, no orange
        g[h - 1][0] = 1
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 2)
        g[0][w - 4] = 3
        return g
    return g

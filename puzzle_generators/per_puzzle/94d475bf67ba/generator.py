"""Generator for arc_additional_puzzles_21_set8:H52.

Rule: nested rectangle frames; for each cell inside a frame, paint it
with the smallest enclosing frame's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_outer, no_inner, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "94d475bf67ba"
VERSION = "1.1.0"
TASK_ID = "94d475bf67ba"
SUMMARY = "Two nested rectangle frames of distinct colors, outer ≥7x7."

INVARIANTS = [
    "outer rectangle frame ≥7x7",
    "inner rectangle frame strictly inside outer ≥3x3",
    "different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_outer", "no_inner", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "outer_inner",
                       "valid": "outer_inner"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "frames", "valid": "frames"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    outer_color, inner_color = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    fh = h - 2; fw = w - 2
    draw_rect_outline(g, 1, 1, fh, fw, outer_color)
    inner_h = rng.randint(3, fh - 4)
    inner_w = rng.randint(3, fw - 4)
    r0 = rng.randint(2, h - inner_h - 2)
    c0 = rng.randint(2, w - inner_w - 2)
    draw_rect_outline(g, r0, c0, inner_h, inner_w, inner_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_outer":
        # only an inner frame → no outer enclosure
        draw_rect_outline(g, 3, 3, 4, 4, 6)
        return g
    if name == "no_inner":
        # only outer frame → no inner-color region, fill is single-color
        draw_rect_outline(g, 1, 1, h - 2, w - 2, 4)
        return g
    if name == "single_frame":
        # only one frame total → no nesting hierarchy
        draw_rect_outline(g, 2, 2, 5, 5, 4)
        return g
    return g

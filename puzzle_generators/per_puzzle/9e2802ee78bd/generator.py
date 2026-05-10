"""Generator for arc_puzzle_bank_twelfth21:M80 — marker chooses panel transform.

Rule: a row-0 marker chooses how to transform the left source panel
into the blank right panel across a vertical separator. Marker 2 flips
the source panel; marker 3 rotates it clockwise.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_separator, right_panel_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e2802ee78bd"
VERSION = "1.1.0"
TASK_ID = "9e2802ee78bd"
SUMMARY = "Marker 2 flips the source panel; marker 3 rotates it clockwise."

INVARIANTS = [
    "marker at row 0 column 0 is either 2 or 3",
    "a full color-9 separator column spans rows below the marker row",
    "the left 5x5 source panel is copied into the right 5x5 target panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_separator", "right_panel_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6..6"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker":         {"type": "int", "default": "rng choice 2|3", "valid": "2 or 3"},
    "shape":          {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_with_panels_and_9_div",
                       "valid": "marker_with_panels_and_9_div"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 2), (1, 1), (1, 2), (1, 3)],
    [(1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        marker = ctx.draw_choice("marker", [2])
    elif difficulty == "hard":
        marker = ctx.draw_choice("marker", [3])
    else:
        marker = ctx.draw_choice("marker", [2, 3])
    shape = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    color = rng.choice([4, 5, 6, 7, 8])
    g = full_grid(6, 12, 0)
    g[0][0] = marker
    for r in range(1, 6):
        g[r][6] = 9
    for r, c in shape:
        g[1 + r][1 + c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 12, 0)
    shape = _SHAPES[0]
    if name == "no_marker":
        # (0,0) empty → no transform code
        for r in range(1, 6): g[r][6] = 9
        for r, c in shape: g[1 + r][1 + c] = 4
        return g
    if name == "no_separator":
        # marker but no 9-col → panels undefined
        g[0][0] = 2
        for r, c in shape: g[1 + r][1 + c] = 4
        return g
    if name == "right_panel_filled":
        # right panel already has content → transform would clobber
        g[0][0] = 2
        for r in range(1, 6): g[r][6] = 9
        for r, c in shape: g[1 + r][1 + c] = 4
        for r, c in shape: g[1 + r][7 + c] = 6   # right pre-filled
        return g
    return g

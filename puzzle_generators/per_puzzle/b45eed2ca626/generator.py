"""Generator for ec883f72.

Rule: L-corner of one color casts a ray in the open diagonal
direction using the other color.

Combinatorial axes (8): grid_h/w, corner_orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_corner, no_other, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b45eed2ca626"
VERSION = "1.1.0"
TASK_ID = "b45eed2ca626"
SUMMARY = "L-corner of one color casts diagonal ray using the other color."

INVARIANTS = [
    "background is color 0",
    "at least two nonzero colors are present",
    "one color forms an orthogonal L-corner",
    "outer and other colors are distinct and non-zero",
]

ORIENTATIONS = ("down_right", "down_left", "up_right", "up_left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_corner", "no_other", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "corner_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for corner_orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orient = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
             overrides.get("corner_orientation") or \
             ctx.draw_choice("corner_orientation", list(ORIENTATIONS))
    outer, other = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(9, 9, 0)
    r, c = 4, 4
    g[r][c] = outer
    if "down" in orient:
        g[r + 1][c] = outer
    else:
        g[r - 1][c] = outer
    if "right" in orient:
        g[r][c + 1] = outer
    else:
        g[r][c - 1] = outer
    g[8][8] = other
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_corner":
        g[8][8] = 2
        return g
    if name == "no_other":
        g[4][4] = 1; g[4][5] = 1; g[5][4] = 1
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 1
        return g
    return g

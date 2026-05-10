"""Generator for f8cc533f.

Rule: a partial square icon is completed by fourfold symmetry.

Combinatorial axes (8): grid_h/w, side, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, foreground.
Degenerates: no_icon, single_pixel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56bcb1d01e53"
VERSION = "1.1.0"
TASK_ID = "56bcb1d01e53"
SUMMARY = "Partial square icon completed by fourfold symmetry."

INVARIANTS = [
    "one connected foreground icon sits in a square bounding box",
    "the observed cells form a vertical spine and one horizontal arm",
    "rotating the observed cells around the square center completes the icon",
]

SIDE_KINDS = ("S5", "S7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_icon", "single_pixel", "full_grid")
HELPFUL_TEXTURES = SIDE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "side":           {"type": "choice", "default": "rng helpful",
                       "valid": "5|7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "foreground":     {"type": "color", "default": "rng !{0,8}",
                       "valid": "1..7|9"},
    "texture":        {"type": "str", "default": "alias for side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SIDE_KINDS:
        side = int(tx[1])
    else:
        side = ctx.draw_choice("side", [5, 7])
    bg = ctx.draw_choice("background", [0, 8])
    color = ctx.draw_color("foreground", exclude={bg})
    margin = 2
    g = full_grid(side + margin * 2, side + margin * 2, bg)
    center = side // 2
    for r in range(side):
        g[margin + r][margin + center] = color
    for c in range(center, side):
        g[margin + center][margin + c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_icon":
        return g
    if name == "single_pixel":
        g[4][4] = 3
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 3
        return g
    return g

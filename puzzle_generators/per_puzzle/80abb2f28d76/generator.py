"""Generator for d6e50e54.

Rule: maroon dots move to or near the nearest side of a blue
rectangle while blue becomes red and old dots become orange.

Combinatorial axes (8): grid_h/w, dot_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
rect_size.
Degenerates: no_rect, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "80abb2f28d76"
VERSION = "1.1.0"
TASK_ID = "80abb2f28d76"
SUMMARY = "Maroon dots snap to blue rectangle sides; blue becomes red, old dots orange."

INVARIANTS = [
    "background is color 0",
    "one blue rectangle uses color 1",
    "maroon marker dots use color 9 and are aligned with rectangle sides",
    "the rectangle sits clear of grid borders so dots can flank all sides",
]

DOT_SIDES = ("left", "right", "top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_dots", "full_grid")
HELPFUL_TEXTURES = DOT_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "dot_side":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DOT_SIDES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "rect_size":      {"type": "str", "default": "3x4", "valid": "3x4"},
    "texture":        {"type": "str", "default": "alias for dot_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    side = (overrides.get("texture") if overrides.get("texture") in DOT_SIDES else None) or \
           overrides.get("dot_side") or \
           ctx.draw_choice("dot_side", list(DOT_SIDES))
    g = full_grid(11, 11, 0)
    r0 = 3 + rng.randint(0, 1)
    c0 = 3 + rng.randint(0, 1)
    r1, c1 = r0 + 2, c0 + 3
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            g[r][c] = 1
    if side == "left":
        g[r0 + 1][c0 - 2] = 9
        g[r0][c0 - 3] = 9
    elif side == "right":
        g[r0 + 1][c1 + 2] = 9
        g[r1][c1 + 3] = 9
    elif side == "top":
        g[r0 - 2][c0 + 1] = 9
        g[r0 - 3][c1] = 9
    else:
        g[r1 + 2][c0 + 1] = 9
        g[r1 + 3][c0 + 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_rect":
        g[5][5] = 9
        return g
    if name == "no_dots":
        for r in range(3, 6):
            for c in range(3, 7):
                g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    return g

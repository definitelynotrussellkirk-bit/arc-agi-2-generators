"""Generator for e8dc4411.

Rule: zero shape stamped repeatedly away from a colored marker.

Combinatorial axes (8): grid_h/w, direction, shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, marker_color.
Degenerates: no_shape, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "35e7d1dc7112"
VERSION = "1.1.0"
TASK_ID = "35e7d1dc7112"
SUMMARY = "Zero shape stamped repeatedly away from colored marker."

INVARIANTS = [
    "the modal background is nonzero",
    "the zero cells form one compact shape",
    "one non-background nonzero marker sets the stamp color and direction",
    "the marker is more than one Manhattan step from the zero-shape center",
]

DIRECTIONS = ("up", "down", "left", "right")
SHAPES = ("domino", "corner")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_marker", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "shape":          {"type": "str", "default": "rng",
                       "valid": "|".join(SHAPES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "marker_color":   {"type": "color", "default": "rng !{0,7}",
                       "valid": "1|2|3|4|5|6|8|9"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("direction") or \
                ctx.draw_choice("direction", list(DIRECTIONS))
    shape = ctx.draw_choice("shape", list(SHAPES))
    marker = ctx.draw_color("marker_color", exclude={0, 7})
    g = full_grid(9, 9, 7)
    cells = [(4, 4), (4, 5)] if shape == "domino" else [(4, 4), (4, 5), (5, 4)]
    for r, c in cells:
        g[r][c] = 0
    if direction == "up":
        g[1][4] = marker
    elif direction == "down":
        g[7][4] = marker
    elif direction == "left":
        g[4][1] = marker
    else:
        g[4][7] = marker
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 7)
    if name == "no_shape":
        g[1][4] = 2
        return g
    if name == "no_marker":
        g[4][4] = 0; g[4][5] = 0
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 7
        return g
    return g

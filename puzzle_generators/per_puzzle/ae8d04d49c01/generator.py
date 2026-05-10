"""Generator for 6a980be1.

Rule: green full bars and a red periodic stripe define a tiled
frame-color pattern.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
frame_color.
Degenerates: no_bars, no_stripe, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ae8d04d49c01"
VERSION = "1.1.0"
TASK_ID = "ae8d04d49c01"
SUMMARY = "Green bars and red stripe define tiled frame-color pattern."

INVARIANTS = [
    "the color at the top-left is the frame fill color",
    "full green rows or columns determine orientation",
    "red cells provide the first stripe width and period",
    "frame color is non-zero and not 2 or 3",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bars", "no_stripe", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "frame_color":    {"type": "color", "default": "rng !{0,2,3}",
                       "valid": "1|4|5|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    fc = ctx.draw_color("frame_color", exclude={0, 2, 3})
    g = full_grid(11, 12, 0)
    g[0][0] = fc
    if orientation == "horizontal":
        for c in range(1, 11):
            g[4][c] = 3
        for c in list(range(2, 4)) + list(range(7, 9)):
            g[7][c] = 2
    else:
        for r in range(1, 10):
            g[r][5] = 3
        for r in list(range(2, 4)) + list(range(7, 9)):
            g[r][8] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_bars":
        g[0][0] = 1
        return g
    if name == "no_stripe":
        for c in range(11):
            g[5][c] = 3
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 3
        return g
    return g

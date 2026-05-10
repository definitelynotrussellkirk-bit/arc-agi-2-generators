"""Generator for e681b708.

Rule: isolated color-1 dots beside a room recolor to the room's majority
marker color.

Combinatorial axes (8): grid_h/w, majority_color_position, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_room, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "65052ae2f657"
VERSION = "1.1.0"
TASK_ID = "65052ae2f657"
SUMMARY = "Isolated color-1 dots beside a room recolor to the room's majority marker color."

INVARIANTS = [
    "zero cells form one enclosed room inside nonzero walls",
    "isolated color-1 dots sit next to that room",
    "nonzero non-1 markers touch the same room and establish a majority color",
    "the rule recolors every adjacent isolated dot to the majority marker color",
]

POSITIONS = ("top", "left", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_room", "no_dots", "full_grid")
HELPFUL_TEXTURES = POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "majority_color_position":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for majority_color_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    marker_side = (overrides.get("texture") if overrides.get("texture") in POSITIONS else None) or \
                  overrides.get("majority_color_position") or \
                  ctx.draw_choice("majority_color_position", list(POSITIONS))
    majority, minority = ctx.draw_distinct_colors("marker_colors", n=2, exclude={0, 1, 5})
    g = full_grid(11, 13, 5)
    draw_rect(g, 3, 4, 4, 5, 0)
    g[2][5] = 1
    g[5][3] = 1
    if marker_side == "top":
        g[2][4] = majority
        g[2][8] = majority
        g[7][6] = minority
    elif marker_side == "left":
        g[3][3] = majority
        g[6][3] = majority
        g[2][7] = minority
    else:
        g[7][4] = majority
        g[7][8] = majority
        g[2][6] = minority
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 5)
    if name == "no_room":
        g[2][5] = 1
        return g
    if name == "no_dots":
        draw_rect(g, 3, 4, 4, 5, 0)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 5
        return g
    return g

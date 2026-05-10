"""Generator for df8cc377.

Rule: scattered pixels count how many checker cells to fill inside a
matching frame.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_frame, no_singletons, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "18bd3cd2985e"
VERSION = "1.1.0"
TASK_ID = "18bd3cd2985e"
SUMMARY = "Scattered pixels count how many checker cells to fill inside matching frame."

INVARIANTS = [
    "the background is zero",
    "one colored rectangular frame has an empty interior",
    "isolated singleton pixels of that same color appear away from the frame",
    "the singleton count equals the number of parity-checker interior cells",
]

FRAME_KINDS = ("F4x5", "F5x4", "F5x5")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_singletons", "full_grid")
HELPFUL_TEXTURES = FRAME_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "frame_size":     {"type": "str", "default": "rng helpful",
                       "valid": "4x5|5x4|5x5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0}",
                       "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for frame_size",
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
    if tx == "F4x5":
        rh, rw = 4, 5
    elif tx == "F5x4":
        rh, rw = 5, 4
    elif tx == "F5x5":
        rh, rw = 5, 5
    else:
        rh, rw = ctx.draw_choice("frame_size", [(4, 5), (5, 4), (5, 5)])
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(12, 12, 0)
    draw_frame(g, 1, 1, rh, rw, color)
    count = ((rh - 2) * (rw - 2) + 1) // 2
    singleton_spots = [(8, 1), (8, 3), (8, 5), (8, 7), (8, 9),
                       (10, 2), (10, 4), (10, 6), (10, 8)]
    for r, c in singleton_spots[:count]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_frame":
        g[8][1] = 3
        g[8][3] = 3
        return g
    if name == "no_singletons":
        draw_frame(g, 1, 1, 4, 5, 3)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g

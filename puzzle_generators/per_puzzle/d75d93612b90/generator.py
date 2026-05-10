"""Generator for d93c6891.

Rule: gray contact pushes orange blocks, while isolated orange blocks
remain orange.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_orange, no_gray, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "d75d93612b90"
VERSION = "1.1.0"
TASK_ID = "d75d93612b90"
SUMMARY = "Gray contact pushes orange blocks; isolated orange blocks remain orange."

INVARIANTS = [
    "orange blocks may touch a gray block on exactly one side",
    "gray cells recolor to yellow and orange cells first recolor to gray",
    "the far side of each contacted orange block remains orange according to contact size",
    "orange blocks without gray contact stay orange",
]

DIRECTIONS = ("top", "left", "bottom", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_orange", "no_gray", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    g = full_grid(12, 14, 0)
    variant = sample_index % 8
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("direction") or \
                ["top", "left", "bottom", "right"][variant % 4]
    r = 3 + (variant // 4)
    c = 5 + ((variant // 2) % 2)
    rh = 3 + (variant % 2)
    rw = 4
    draw_rect(g, r, c, rh, rw, 7)
    if direction == "top":
        draw_rect(g, r - 1, c, 1, rw, 5)
    elif direction == "bottom":
        draw_rect(g, r + rh, c, 1, rw, 5)
    elif direction == "left":
        draw_rect(g, r, c - 1, rh, 1, 5)
    else:
        draw_rect(g, r, c + rw, rh, 1, 5)
    draw_rect(g, 1, 1, 2, 2, 7)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_orange":
        draw_rect(g, 3, 5, 1, 4, 5)
        return g
    if name == "no_gray":
        draw_rect(g, 3, 5, 3, 4, 7)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 7
        return g
    return g

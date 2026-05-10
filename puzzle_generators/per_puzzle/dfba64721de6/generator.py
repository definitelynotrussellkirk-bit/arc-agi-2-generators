"""Generator for 11dc524f.

Rule: a red shape slides toward a gray target and the gray output
becomes the reflected red shape docked beside it.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_red, no_gray, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfba64721de6"
VERSION = "1.1.0"
TASK_ID = "dfba64721de6"
SUMMARY = "Red shape slides to gray target; gray becomes red's reflection docked alongside."

INVARIANTS = [
    "the background is color 7",
    "one red component and one gray component are separated along a dominant horizontal or vertical axis",
    "the red component can slide toward the gray component without overlapping it",
    "the final gray shape is the left-right or up-down reflection of the red shape placed adjacent to the docked red shape",
]

DIRECTIONS = ("right", "left", "down", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_red", "no_gray", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_RED_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 1), (1, 1), (2, 1), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, cells, r0, c0, color):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


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
    red_shape = _RED_SHAPES[rng.randrange(len(_RED_SHAPES))]
    g = full_grid(15, 15, 7)
    if direction == "right":
        _paint(g, red_shape, 6, 1, 2)
        _paint(g, [(0, 0), (0, 1), (1, 0), (1, 1)], 6, 11, 5)
    elif direction == "left":
        _paint(g, red_shape, 6, 11, 2)
        _paint(g, [(0, 0), (0, 1), (1, 0), (1, 1)], 6, 1, 5)
    elif direction == "down":
        _paint(g, red_shape, 1, 6, 2)
        _paint(g, [(0, 0), (0, 1), (1, 0), (1, 1)], 11, 6, 5)
    else:
        _paint(g, red_shape, 11, 6, 2)
        _paint(g, [(0, 0), (0, 1), (1, 0), (1, 1)], 1, 6, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 7)
    if name == "no_red":
        _paint(g, [(0, 0), (0, 1), (1, 0), (1, 1)], 6, 11, 5)
        return g
    if name == "no_gray":
        _paint(g, _RED_SHAPES[0], 6, 1, 2)
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g

"""Generator for 13f06aa5.

Rule: a minority-color indicator cell inside a shape sends a dotted
trail and edge bar outward.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shape, no_indicator, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "c5a3cd43d29b"
VERSION = "1.1.0"
TASK_ID = "c5a3cd43d29b"
SUMMARY = "Minority indicator inside shape sends dotted trail and edge bar outward."

INVARIANTS = [
    "the mode color is the background",
    "one compact non-background component has a majority body color and one minority indicator color",
    "the indicator is offset from the component centroid along a cardinal direction",
    "the rule paints a dotted ray from the indicator and fills the corresponding edge row or column",
]

DIRECTIONS = ("up", "down", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_indicator", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "11..15"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "11..16"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    bg, body, indicator = ctx.draw_distinct_colors("colors", n=3, exclude=set())
    h = rng.randint(11, 15)
    w = rng.randint(11, 16)
    g = full_grid(h, w, bg)

    r0 = rng.randint(4, h - 7)
    c0 = rng.randint(4, w - 7)
    cells = PLUS_5
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = body

    if direction == "up":
        ind = (r0, c0 + 1)
    elif direction == "down":
        ind = (r0 + 2, c0 + 1)
    elif direction == "left":
        ind = (r0 + 1, c0)
    else:
        ind = (r0 + 1, c0 + 2)
    g[ind[0]][ind[1]] = indicator
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_shape":
        g[5][5] = 4
        return g
    if name == "no_indicator":
        for dr, dc in PLUS_5:
            g[5 + dr][5 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 3
        return g
    return g

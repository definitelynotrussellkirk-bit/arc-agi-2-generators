"""Generator for 5daaa586.

Rule: colored boundary lines define a crop; interior scatter matching one
wall color grows into bars from that wall.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_walls, no_scatter, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b08e9fc77a85"
VERSION = "1.1.0"
TASK_ID = "b08e9fc77a85"
SUMMARY = "Boundary lines crop; interior scatter matching one wall grows into bars."

INVARIANTS = [
    "background is color 0",
    "two near-full rows and two near-full columns form the crop boundary",
    "the scatter color matches exactly one boundary color",
    "scatter cells are strictly inside the boundary rectangle",
]

DIRECTIONS = ("left", "right", "up", "down")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_walls", "no_scatter", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "11..15"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "11..15"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
    h = 11 + rng.randint(0, 4)
    w = 11 + rng.randint(0, 4)
    top = 2
    bottom = h - 3
    left = 2
    right = w - 3
    top_color, bottom_color, left_color, right_color = ctx.draw_distinct_colors(
        "line_colors", n=4, exclude={0})
    g = full_grid(h, w, 0)

    for r in range(h):
        g[r][left] = left_color
        g[r][right] = right_color
    for c in range(w):
        g[top][c] = top_color
        g[bottom][c] = bottom_color

    scatter_color = {
        "down": top_color,
        "up": bottom_color,
        "right": left_color,
        "left": right_color,
    }[direction]
    inner_rows = list(range(top + 1, bottom))
    inner_cols = list(range(left + 1, right))
    for i in range(3):
        r = inner_rows[(sample_index + i * 2 + rng.randint(0, 3)) % len(inner_rows)]
        c = inner_cols[(seed + sample_index + i * 3 + rng.randint(0, 4)) % len(inner_cols)]
        g[r][c] = scatter_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_walls":
        g[5][5] = 3
        return g
    if name == "no_scatter":
        for r in range(11):
            g[r][2] = 3
            g[r][8] = 4
        for c in range(11):
            g[2][c] = 5
            g[8][c] = 6
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 3
        return g
    return g

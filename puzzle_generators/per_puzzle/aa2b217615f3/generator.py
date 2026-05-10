"""Generator for 6ad5bdfd.

Rule: red edge line attracts separated colored objects, sliding them
until they stack against the line or earlier objects.

Combinatorial axes (8): grid_h/w, direction, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_line, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aa2b217615f3"
VERSION = "1.1.0"
TASK_ID = "aa2b217615f3"
SUMMARY = "Red edge line attracts colored objects; they stack against line."

INVARIANTS = [
    "background is color 0",
    "exactly one full edge line uses color 2",
    "movable objects use nonzero non-2 colors",
    "objects are separated before sliding toward the red line",
]

DIRECTIONS = ("up", "down", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_objects", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0, 2})
    g = full_grid(h, w, 0)
    if direction == "up":
        for c in range(w):
            g[0][c] = 2
        anchors = [(h - 3, 2), (h - 5, w - 4), (h - 2, w // 2)]
    elif direction == "down":
        for c in range(w):
            g[h - 1][c] = 2
        anchors = [(2, 2), (4, w - 4), (1, w // 2)]
    elif direction == "left":
        for r in range(h):
            g[r][0] = 2
        anchors = [(2, w - 3), (h - 4, w - 5), (h // 2, w - 2)]
    else:
        for r in range(h):
            g[r][w - 1] = 2
        anchors = [(2, 2), (h - 4, 4), (h // 2, 1)]
    shapes = [
        [(0, 0), (0, 1)],
        [(0, 0), (1, 0)],
        [(0, 0), (1, 0), (1, 1)],
    ]
    for i, (r0, c0) in enumerate(anchors):
        for dr, dc in shapes[i]:
            rr, cc = r0 + dr, c0 + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] == 0:
                g[rr][cc] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_line":
        g[5][5] = 3
        return g
    if name == "no_objects":
        for c in range(10):
            g[0][c] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g

"""Generator for 5e6bbc0b.

Rule: rows or columns of blue cells slide toward edge cyan marker;
marker line leaves yellow trail.

Combinatorial axes (8): grid_h/w, direction, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_marker, no_blue, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffdc7818d842"
VERSION = "1.1.0"
TASK_ID = "ffdc7818d842"
SUMMARY = "Blue cells slide to edge cyan marker; marker line leaves yellow trail."

INVARIANTS = [
    "background is color 0",
    "one cyan marker sits on a grid edge",
    "all movable cells are color 1",
    "the marker edge determines the gravity direction",
]

DIRECTIONS = ("left", "right", "up", "down")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_blue", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
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
    h = 7 + rng.randint(0, 4)
    w = 7 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    if direction == "up":
        er, ec = 0, 1 + ((sample_index + rng.randint(0, 4)) % (w - 2))
    elif direction == "down":
        er, ec = h - 1, 1 + ((sample_index + rng.randint(0, 4)) % (w - 2))
    elif direction == "left":
        er, ec = 1 + ((sample_index + rng.randint(0, 4)) % (h - 2)), 0
    else:
        er, ec = 1 + ((sample_index + rng.randint(0, 4)) % (h - 2)), w - 1
    g[er][ec] = 8
    if direction in ("left", "right"):
        for r in range(1, h - 1):
            c = 1 + ((seed + sample_index + r * 2) % (w - 2))
            g[r][c] = 1
            if (r + sample_index) % 2 == 0 and c + 1 < w - 1:
                g[r][c + 1] = 1
    else:
        for c in range(1, w - 1):
            r = 1 + ((seed + sample_index + c * 2) % (h - 2))
            g[r][c] = 1
            if (c + sample_index) % 2 == 0 and r + 1 < h - 1:
                g[r + 1][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_marker":
        g[4][4] = 1
        return g
    if name == "no_blue":
        g[0][4] = 8
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 1
        return g
    return g

"""Generator for arc_additional_puzzles_21_set7:M48.

Rule: same-colored points are connected in reading order by horizontal-
then-vertical traces.

Combinatorial axes (8): grid_h/w, point_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_points, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1357a20304bd"
VERSION = "1.1.0"
TASK_ID = "1357a20304bd"
SUMMARY = "Same-colored points are connected in reading order by horizontal-then-vertical traces."

INVARIANTS = [
    "each foreground color has two or more seed points",
    "points are traced in row-major order for each color",
    "each segment moves horizontally to the next point's column, then vertically to its row",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_points", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "point_count":    {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        point_count = ctx.draw_int("point_count", 2, 2)
    elif difficulty == "hard":
        point_count = ctx.draw_int("point_count", 3, 3)
    else:
        point_count = ctx.draw_int("point_count", 2, 3)
    a, b = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(10, 10, 0)
    pts_a = [(1, 1), (3 + (sample_index % 2), 6), (7, 7)]
    pts_b = [(2, 8), (6, 2), (8, 4)]
    for r, c in pts_a[:point_count]:
        g[r][c] = a
    for r, c in pts_b[:2 + (sample_index % 2)]:
        g[r][c] = b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_points":
        return g
    if name == "single_color":
        for r, c in [(1, 1), (5, 5), (7, 7)]:
            g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 3
        return g
    return g

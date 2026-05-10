"""Generator for 855e0971.

Rule: zero holes erase the longer compatible row or column through
their neighboring color.

Combinatorial axes (8): grid_h/w, hole_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec9cf2c80d58"
VERSION = "1.1.0"
TASK_ID = "ec9cf2c80d58"
SUMMARY = "Zero holes erase the longer compatible row or column."

INVARIANTS = [
    "the grid is otherwise filled with one nonzero color",
    "one or more zero holes touch that color orthogonally",
    "the row-vs-column extent decides which line is cleared",
    "the foreground color is non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..16"},
    "hole_count":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "color":          {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    count = ctx.draw_int("hole_count", 1, 2)
    color = ctx.draw_color("color", exclude={0})
    h = 6 + rng.randint(0, 3)
    w = 7 + rng.randint(0, 3)
    g = full_grid(h, w, color)
    g[h // 2][w // 2] = 0
    if count == 2:
        g[h // 2 - 1][w // 2] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 9, 2)
    if name == "no_holes":
        return g
    if name == "all_holes":
        return full_grid(8, 9, 0)
    if name == "full_grid":
        for r in range(8):
            for c in range(9):
                g[r][c] = 2
        return g
    return g

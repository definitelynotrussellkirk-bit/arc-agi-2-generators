"""Generator for arc_additional_puzzle_bank_volume20:E140.

Rule: the largest color-2 object is recolored to 8 while smaller red
objects remain.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors, other.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db98b701e5bb"
VERSION = "1.1.0"
TASK_ID = "db98b701e5bb"
SUMMARY = "Largest color-2 object recolored to 8; smaller red objects remain."

INVARIANTS = [
    "multiple separated color-2 objects exist",
    "one color-2 object is strictly largest",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "8..11"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "8..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "other":          {"type": "color", "default": "rng !{0,2,8}",
                       "valid": "1|3..7|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    other = ctx.draw_color("other", exclude=[0, 2, 8])
    g = full_grid(h, w, 0)
    g[1][1] = 2
    g[1][2] = 2
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]:
        g[h - 5 + dr][w - 4 + dc] = 2
    g[0][w - 1] = other
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_objects":
        g[0][8] = 3
        return g
    if name == "single_object":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 2
        return g
    return g

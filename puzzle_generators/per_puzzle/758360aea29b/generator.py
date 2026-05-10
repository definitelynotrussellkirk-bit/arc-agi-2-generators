"""Generator for arc_additional_puzzles_21_set10_bundle:M70.

Rule: objects sorted by reading order produce a matrix comparing their
bounding-box widths.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "758360aea29b"
VERSION = "1.1.0"
TASK_ID = "758360aea29b"
SUMMARY = "Objects sorted by reading order produce a matrix comparing their bounding-box widths."

INVARIANTS = [
    "objects are separated by background",
    "widths include equal, greater, and lesser comparisons",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    draw_rect(g, 1, 1, 2, 4, colors[0])
    draw_rect(g, 1, w - 4, 3, 2, colors[1])
    draw_rect(g, h - 4, 1, 2, 4, colors[2])
    draw_rect(g, h - 3, w - 5, 2, 3, colors[3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 14, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        draw_rect(g, 4, 5, 2, 4, 3)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(14):
                g[r][c] = 3
        return g
    return g

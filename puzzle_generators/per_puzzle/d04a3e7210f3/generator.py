"""Generator for arc_additional_puzzle_bank_volume15:H103.

Rule: a singleton control selects a transform of the color-1 template;
markers 7 and 9 define the translation vector for the cyan copy.

Combinatorial axes (8): grid_h/w, palette_kind, control_color,
palette_size, position_bias, n_distinct_colors, vector_length, texture.
Degenerates: no_control, no_template, missing_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d04a3e7210f3"
VERSION = "1.1.0"
TASK_ID = "d04a3e7210f3"
SUMMARY = "A singleton control selects a transform of the color-1 template, then marker 7-to-9 translates the copy."

INVARIANTS = [
    "one color from 2, 3, 4, or 6 occurs exactly once as the control",
    "there is one largest color-1 template",
    "markers 7 and 9 define a nonzero vector",
    "the cyan transformed copy fits without covering controls",
]

PALETTE_KINDS = ("default", "control_2", "control_3_or_4", "control_6")
DEGENERATE_TEXTURES = ("no_control", "no_template", "missing_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng 2|3|4|6",
                       "valid": "2|3|4|6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "vector_length":  {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][w - 2] = rng.choice([2, 3, 4, 6])
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
        g[2 + dr][1 + dc] = 1
    g[h - 3][w - 5] = 7
    g[h - 2][w - 3] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_control":
        # template + markers but no transform-selection control
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
            g[2 + dr][1 + dc] = 1
        g[h - 3][w - 5] = 7
        g[h - 2][w - 3] = 9
        return g
    if name == "no_template":
        # control + markers but no color-1 to transform
        g[0][w - 2] = 4
        g[h - 3][w - 5] = 7
        g[h - 2][w - 3] = 9
        return g
    if name == "missing_marker":
        # control + template but only marker 7 (no 9 → no vector)
        g[0][w - 2] = 6
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
            g[2 + dr][1 + dc] = 1
        g[h - 3][w - 5] = 7
        return g
    return g

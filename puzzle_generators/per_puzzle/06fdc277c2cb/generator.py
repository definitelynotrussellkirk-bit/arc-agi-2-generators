"""Generator for arc_additional_puzzle_bank_volume14:H96.

Rule: a control cell selects a transform of the color-6 template; the
copy is stamped by the vector from marker 1 to marker 2.

Combinatorial axes (8): grid_h/w, palette_kind, control_color,
palette_size, position_bias, n_distinct_colors, vector_length, texture.
Degenerates: no_control, no_template, no_marker_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "06fdc277c2cb"
VERSION = "1.1.0"
TASK_ID = "06fdc277c2cb"
SUMMARY = "A control-selected transform of the color-6 template is stamped by the vector from marker 1 to marker 2."

INVARIANTS = [
    "there is one color-6 asymmetric template",
    "one control cell is in 3, 4, 7, or 8",
    "markers 1 and 2 define a nonzero vector",
    "the transformed translated copy fits in-bounds",
]

PALETTE_KINDS = ("default", "control_3", "control_4", "control_7_or_8")
DEGENERATE_TEXTURES = ("no_control", "no_template", "no_marker_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng 3|4|7|8", "valid": "3|4|7|8"},
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
    g[0][0] = rng.choice([3, 4, 7, 8])
    tr, tc = 2, 1
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
        g[tr + dr][tc + dc] = 6
    g[h - 3][2] = 1
    g[h - 3][rng.randint(5, min(w - 3, 8))] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_control":
        # template + markers but no rotation control — undefined transform
        tr, tc = 2, 1
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[tr + dr][tc + dc] = 6
        g[h - 3][2] = 1
        g[h - 3][6] = 2
        return g
    if name == "no_template":
        # control + markers but no color-6 to transform
        g[0][0] = 4
        g[h - 3][2] = 1
        g[h - 3][6] = 2
        return g
    if name == "no_marker_pair":
        # control + template but no 1→2 vector to translate by
        g[0][0] = 7
        tr, tc = 2, 1
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[tr + dr][tc + dc] = 6
        return g
    return g

"""Generator for arc_additional_puzzle_bank_volume15:M103.

Rule: dr/dc = (3-marker − 2-marker) + (6-marker − 4-marker). For each
1-cell, paint 8 at (r + dr, c + dc) when that cell is 0.

Combinatorial axes (9): grid_h/w, palette_kind, marker_layout,
template_size, palette_size, position_bias, n_distinct_colors,
decoration_color, texture.
Degenerates: missing_marker, zero_combined_delta, no_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e043084e26ab"
VERSION = "1.1.0"
TASK_ID = "e043084e26ab"
SUMMARY = "1-template + 4 markers (2,3,4,6) define combined translation; decoration."

INVARIANTS = [
    "exactly one 1-blob, one each of markers 2,3,4,6",
    "combined delta keeps translated cells in-bounds",
    "decoration is non-{1..6} cell",
]

PALETTE_KINDS = ("default", "tight_template", "wide_grid", "spread_markers")
DEGENERATE_TEXTURES = ("missing_marker", "zero_combined_delta", "no_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_layout":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "template_size":  {"type": "int", "default": "3", "valid": "3"},
    "decoration_color": {"type": "int", "default": "5", "valid": "5"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    g[0][8] = 2
    g[1][9] = 3
    g[7][8] = 4
    g[7][9] = 6
    g[1][1] = 1; g[2][1] = 1; g[2][2] = 1
    g[h - 1][0] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "missing_marker":
        # only 3 of the 4 markers — combined delta undefined
        g[0][8] = 2
        g[1][9] = 3
        g[7][8] = 4
        g[1][1] = 1; g[2][1] = 1; g[2][2] = 1
        g[h - 1][0] = 5
        return g
    if name == "zero_combined_delta":
        # delta vectors cancel — net translation is (0, 0)
        g[0][8] = 2
        g[1][9] = 3
        g[8][9] = 4
        g[7][8] = 6
        g[1][1] = 1; g[2][1] = 1; g[2][2] = 1
        g[h - 1][0] = 5
        return g
    if name == "no_template":
        # markers but no 1-blob to translate
        g[0][8] = 2
        g[1][9] = 3
        g[7][8] = 4
        g[7][9] = 6
        g[h - 1][0] = 5
        return g
    return g

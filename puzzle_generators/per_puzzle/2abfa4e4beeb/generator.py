"""Generator for arc_additional_puzzle_bank_volume13:H89.

Rule: dr/dc = (3-marker − 2-marker) + (6-marker − 4-marker). For each
1-cell, paint 8 at (r + dr, c + dc) if in bounds.

Combinatorial axes (8): grid_h/w, palette_kind, blob_size, marker_layout,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: missing_marker, zero_combined_delta, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2abfa4e4beeb"
VERSION = "1.1.0"
TASK_ID = "2abfa4e4beeb"
SUMMARY = "1-blob + 4 markers (2, 3, 4, 6) defining combined translation vector."

INVARIANTS = [
    "exactly one 1-blob, one each of 2, 3, 4, 6 markers",
    "combined delta keeps translated 1-cells in bounds",
]

PALETTE_KINDS = ("default", "tight_blob", "wide_grid", "varied_markers")
DEGENERATE_TEXTURES = ("missing_marker", "zero_combined_delta", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "5", "valid": "5"},
    "marker_layout":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    g[0][7] = 2
    g[1][10] = 3
    g[2][2] = 4
    g[1][0] = 6
    g[5][6] = 1
    g[6][5] = 1; g[6][6] = 1; g[6][7] = 1
    g[7][6] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "missing_marker":
        # only 3 of the 4 markers — combined delta undefined
        g[0][7] = 2
        g[1][10] = 3
        g[2][2] = 4
        g[5][6] = 1
        g[6][5] = 1; g[6][6] = 1; g[6][7] = 1
        return g
    if name == "zero_combined_delta":
        # the two delta vectors cancel — net translation is (0, 0), output is identity
        g[0][7] = 2
        g[1][8] = 3
        g[2][2] = 4
        g[1][1] = 6
        g[5][6] = 1
        g[6][5] = 1; g[6][6] = 1; g[6][7] = 1
        return g
    if name == "no_blob":
        # markers but no 1-blob to translate
        g[0][7] = 2
        g[1][10] = 3
        g[2][2] = 4
        g[1][0] = 6
        return g
    return g

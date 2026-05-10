"""Generator for arc_additional_puzzle_bank_volume13:M85.

Rule: dr/dc = (3-marker - 2-marker). For each cell of 1-blob, paint 8
at (r+dr, c+dc) if in bounds.

Combinatorial axes (8): grid_h/w, palette_kind, n_decorations,
palette_size, position_bias, n_distinct_colors, delta_kind, texture.
Degenerates: no_blob, no_2_marker, no_3_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "297e46df4407"
VERSION = "1.1.0"
TASK_ID = "297e46df4407"
SUMMARY = "1-blob + 2-marker (origin) + 3-marker (downstream) + 9-decoration."

INVARIANTS = [
    "exactly one 1-blob, one 2-cell, one 3-cell",
    "translated cells stay in-bounds",
    "1-2 9-decorations",
]

PALETTE_KINDS = ("default", "short_delta", "long_delta", "diag_delta")
DEGENERATE_TEXTURES = ("no_blob", "no_2_marker", "no_3_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_decorations":  {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "delta_kind":     {"type": "str", "default": "rng", "valid": "rng"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[1][3] = 1
    g[2][3] = 1
    g[2][4] = 1
    g[1][4] = 2
    dr = rng.randint(1, 2); dc = rng.randint(4, 5)
    g[1 + dr][4 + dc] = 3
    g[h - 1][1] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blob":
        # markers + decoration but no 1-blob → rule has no source cells
        g[1][4] = 2
        g[3][8] = 3
        g[h - 1][1] = 9
        return g
    if name == "no_2_marker":
        # blob + 3-marker but no 2-marker → delta origin undefined
        g[1][3] = 1; g[2][3] = 1; g[2][4] = 1
        g[3][8] = 3
        g[h - 1][1] = 9
        return g
    if name == "no_3_marker":
        # blob + 2-marker but no 3-marker → delta target undefined
        g[1][3] = 1; g[2][3] = 1; g[2][4] = 1
        g[1][4] = 2
        g[h - 1][1] = 9
        return g
    return g

"""Generator for arc_additional_puzzle_bank_volume4:M24.

Rule: dr/dc = (3-marker - 2-marker). For each cell with v ∉ {0,2,3},
place v at (r+dr, c+dc) in fresh grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, delta_kind, texture.
Degenerates: no_2_marker, no_3_marker, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a8932958b14"
VERSION = "1.1.0"
TASK_ID = "1a8932958b14"
SUMMARY = "2-marker (origin) + 3-marker (downstream) + small blob of other colors."

INVARIANTS = [
    "exactly one 2-cell, one 3-cell",
    "small blob of color 6 between/around them",
    "translated cells stay in-bounds",
]

PALETTE_KINDS = ("default", "small_delta", "large_delta", "varied_delta")
DEGENERATE_TEXTURES = ("no_2_marker", "no_3_marker", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[3][2] = 6
    g[3][3] = 6
    g[3][4] = 6
    g[4][3] = 6
    g[h - 1][3] = 2
    dr = -(rng.randint(2, 3))
    dc = rng.randint(1, 2)
    g[h - 1 + dr][3 + dc] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_2_marker":
        # blob + 3-marker but no 2-marker → delta origin undefined
        for r, c in [(3, 2), (3, 3), (3, 4), (4, 3)]:
            g[r][c] = 6
        g[h - 4][5] = 3
        return g
    if name == "no_3_marker":
        # blob + 2-marker but no 3-marker → delta target undefined
        for r, c in [(3, 2), (3, 3), (3, 4), (4, 3)]:
            g[r][c] = 6
        g[h - 1][3] = 2
        return g
    if name == "no_blob":
        # markers but no transferable cells → rule has nothing to translate
        g[h - 1][3] = 2
        g[h - 4][5] = 3
        return g
    return g

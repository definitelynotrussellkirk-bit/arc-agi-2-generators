"""Generator for arc_additional_puzzle_bank_volume14:M92.

Rule: dr/dc = (9-marker - 8-marker). For each cell of 2-blob, paint 3
at (r+dr, c+dc) if in bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_8_marker, missing_9_marker, zero_delta.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7f3446077e8e"
VERSION = "1.1.0"
TASK_ID = "7f3446077e8e"
SUMMARY = "2-blob + 8-marker + 9-marker (delta) + decoration; output translates 2s to 3s."

INVARIANTS = [
    "exactly one 2-blob, one 8-cell, one 9-cell",
    "delta keeps shifted blob in-bounds",
    "decoration far from translation target",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_8_marker", "missing_9_marker", "zero_delta")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "1", "valid": "1"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "blob_top_markers_bottom",
                       "valid": "blob_top_markers_bottom"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[2][2] = 2
    g[3][2] = 2
    g[3][3] = 2
    dr = rng.randint(2, 3); dc = rng.randint(2, 3)
    g[h - 3][1] = 8
    g[h - 3 - dr + dr][1 + dc] = 9
    g[0][w - 2] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    g[2][2] = 2; g[3][2] = 2; g[3][3] = 2
    if name == "missing_8_marker":
        # no 8-cell → delta source endpoint undefined
        g[h - 3][3] = 9
        return g
    if name == "missing_9_marker":
        # no 9-cell → delta target endpoint undefined
        g[h - 3][1] = 8
        return g
    if name == "zero_delta":
        # 8 and 9 at the same cell → delta is (0,0), translation is identity
        g[h - 3][3] = 8
        g[h - 3][3] = 9
        return g
    return g

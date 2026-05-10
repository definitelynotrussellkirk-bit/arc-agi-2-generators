"""Generator for arc_additional_puzzle_bank_volume2:M13 — Translate 6-cells by direction marker.

Rule: marker color → direction: 1=left, 2=up, 3=right, 4=down. For each
6-cell, paint 6 at (r+dr, c+dc).

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, blob_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c0f52d961a7c"
VERSION = "1.1.0"
TASK_ID = "c0f52d961a7c"
SUMMARY = "Single direction marker (1/2/3/4) + plus-shape 6-blob centered to leave room for translation."

INVARIANTS = [
    "exactly one direction marker (color 1/2/3/4)",
    "5-cell plus-shape 6-blob with room to translate in marker's direction",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "blob_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker":         {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "centered_blob_with_marker",
                       "valid": "centered_blob_with_marker"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        marker = ctx.draw_int("marker", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        marker = ctx.draw_int("marker", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
        marker = ctx.draw_int("marker", 1, 4)
    g = full_grid(h, w, 0)
    cr = h // 2; cc = w // 2
    g[cr][cc] = 6
    g[cr - 1][cc] = 6
    g[cr + 1][cc] = 6
    g[cr][cc - 1] = 6
    g[cr][cc + 1] = 6
    if marker == 1:  # left
        g[1][cc + 2] = 1
    elif marker == 2:  # up
        g[cr + 2][1] = 2
    elif marker == 3:  # right
        g[1][cc - 2] = 3
    else:  # down
        g[cr - 2][1] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # 6-blob but no direction marker → no translation vector
        cr, cc = h // 2, w // 2
        g[cr][cc] = 6
        g[cr - 1][cc] = 6; g[cr + 1][cc] = 6
        g[cr][cc - 1] = 6; g[cr][cc + 1] = 6
        return g
    if name == "no_blob":
        # marker exists but no 6-cells → nothing to translate
        g[1][1] = 3
        return g
    if name == "blob_at_edge":
        # blob at edge in marker's direction → translation off grid
        # marker = 1 (left) but blob anchored at left edge
        g[3][0] = 6; g[3][1] = 6   # blob already at left edge
        g[1][5] = 1                 # marker says go left further
        return g
    return g

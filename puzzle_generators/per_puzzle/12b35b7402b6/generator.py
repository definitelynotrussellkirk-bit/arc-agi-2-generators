"""Generator for arc_puzzle_bank_21_set4:S4_M4 — marker count matches object size.

Rule: gray markers in the top row name the size of one blue object below.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_matching_size, tied_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "12b35b7402b6"
VERSION = "1.1.0"
TASK_ID = "12b35b7402b6"
SUMMARY = "Gray markers in the top row name the size of one blue object below."

INVARIANTS = [
    "background is 0",
    "the only gray cells are top-row count markers",
    "there is exactly one blue object whose cell count equals the marker count",
    "all blue objects are separated and below the top row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_matching_size", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_count":   {"type": "int", "default": "rng 2..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_gray_count_blue_bars",
                       "valid": "row0_gray_count_blue_bars"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        marker_count = ctx.draw_int("marker_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
        marker_count = ctx.draw_int("marker_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
        marker_count = ctx.draw_int("marker_count", 2, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(marker_count):
        g[0][c] = 5

    sizes = [marker_count, marker_count + 2, marker_count + 4]
    rng.shuffle(sizes)
    for i, size in enumerate(sizes):
        r = 2 + i * 2
        if r >= h:
            raise ValueError("grid too short for size bars")
        c0 = 1
        if c0 + size > w:
            raise ValueError("grid too narrow for size bars")
        for c in range(c0, c0 + size):
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 empty → marker count = 0, no target size
        for c in range(1, 4): g[2][c] = 1
        for c in range(1, 6): g[4][c] = 1
        return g
    if name == "no_matching_size":
        # markers say 3, but no blue object has size 3
        for c in range(3): g[0][c] = 5   # marker count = 3
        for c in range(1, 3): g[2][c] = 1   # size 2
        for c in range(1, 6): g[4][c] = 1   # size 5
        return g
    if name == "tied_match":
        # 2 blue objects with the matching size → ambiguous selection
        for c in range(3): g[0][c] = 5   # marker count = 3
        for c in range(1, 4): g[2][c] = 1   # size 3
        for c in range(6, 9): g[2][c] = 1   # size 3 (tied)
        return g
    return g

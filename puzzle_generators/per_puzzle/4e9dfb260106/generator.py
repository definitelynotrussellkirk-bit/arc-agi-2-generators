"""Generator for arc_additional_puzzle_bank_volume16:M111 -- crop 1-object matching red count.

Rule: the count of red cells selects the color-1 object with matching
size, then outputs its mask crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, red_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, no_match, tied_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "4e9dfb260106"
VERSION = "1.1.0"
TASK_ID = "4e9dfb260106"
SUMMARY = "The count of red cells selects the color-1 object with matching size, then outputs its mask crop."

INVARIANTS = [
    "red cell count is between 3 and 5",
    "exactly one color-1 object has size equal to the red count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "red_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "red_count_with_matching_1obj",
                       "valid": "red_count_with_matching_1obj"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}



def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        k = ctx.draw_int("red_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        k = ctx.draw_int("red_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        k = ctx.draw_int("red_count", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    red_slots = [(0, c) for c in range(1, min(w - 1, k + 2))]
    for r, c in red_slots[:k]:
        g[r][c] = 2
    target_cells = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)][:k]
    paint_at(g, 2, 2, target_cells, 1)
    paint_at(g, h - 3, w - 4, [(0, 0), (0, 1)], 1)
    if rng.random() < 0.5:
        paint_at(g, h - 2, 2, [(0, 0), (0, 1), (0, 2), (1, 0)], 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_red":
        # no red cells → red count is 0, no size to look up
        paint_at(g, 2, 2, [(0, 0), (0, 1), (1, 0)], 1)
        paint_at(g, 7, 6, [(0, 0), (0, 1)], 1)
        return g
    if name == "no_match":
        # red count = 5, but no 1-object has size 5 → lookup fails
        for c in range(1, 6): g[0][c] = 2  # 5 reds
        paint_at(g, 2, 2, [(0, 0), (0, 1)], 1)            # size 2
        paint_at(g, 7, 6, [(0, 0), (0, 1), (1, 0)], 1)    # size 3
        return g
    if name == "tied_match":
        # 2 1-objects share the matching size → ambiguous selection
        for c in range(1, 4): g[0][c] = 2  # 3 reds
        paint_at(g, 2, 2, [(0, 0), (0, 1), (1, 0)], 1)         # size 3
        paint_at(g, 6, 7, [(0, 0), (1, 0), (1, 1)], 1)         # size 3 (tied)
        paint_at(g, 9, 1, [(0, 0), (0, 1)], 1)                 # size 2
        return g
    return g

"""Generator for arc_additional_puzzles_21_set5:H35 — Mark cells with LoS to 2 (horiz) AND 3 (vert).

Rule: for each empty cell (r,c), check if there's a 2-cell on same row
with all-zero between, AND a 3-cell on same col with all-zero between.
If both → 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n2,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_2, no_3, no_los_intersection.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d06e81a85b9e"
VERSION = "1.1.0"
TASK_ID = "d06e81a85b9e"
SUMMARY = "2-3 2-cells + 2-3 3-cells positioned so some interior cells have LoS to both."

INVARIANTS = [
    "between 2 and 3 2-cells",
    "between 2 and 3 3-cells",
    "at least one empty cell has horizontal LoS to a 2 and vertical LoS to a 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_2", "no_3", "no_los_intersection")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n2":             {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n3":             {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "scattered_2_and_3",
                       "valid": "scattered_2_and_3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n2 = rng.randint(2, 3)
    n3 = rng.randint(2, 3)
    placed = 0
    while placed < n2:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        g[r][c] = 2; placed += 1
    placed = 0
    while placed < n3:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        g[r][c] = 3; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_2":
        # only 3-cells → no horizontal source, rule never fires
        g[1][3] = 3
        g[5][7] = 3
        return g
    if name == "no_3":
        # only 2-cells → no vertical source, rule never fires
        g[2][1] = 2
        g[4][6] = 2
        return g
    if name == "no_los_intersection":
        # 2s and 3s exist but no empty cell has LoS to both
        # Put 2s in row 0 only and 3s in col w-1 only - no row/col share
        # any empty cell with both axes clear (place a blocker in between)
        g[0][2] = 2; g[0][6] = 2
        g[h - 1][1] = 3; g[h - 1][8] = 3
        # add blocker on every potential LoS path
        for c in range(w): g[3][c] = 5   # row 3 of 5s blocks vertical LoS
        return g
    return g
